import csv

from rest_framework.decorators import api_view

from .serializers import *
from .utils import *


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, STUDENT_LIST])
def markStatus(request, id, email, user_type):
    try:
        data = request.data
        if OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE] #not to break the code
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            applications = InternshipApplication.objects.filter(internship_id=data[OPENING_ID])
        else:
            applications = PlacementApplication.objects.filter(placement_id=data[OPENING_ID])
        # Getting all application from db for this opening
        # applications = PlacementApplication.objects.filter(placement_id=data[OPENING_ID])
        for i in data[STUDENT_LIST]:
           # print(i[STUDENT_ID])   issue is using student id instead of roll no both may not be same                #remember this
            application = applications.filter(student__roll_no=i[STUDENT_ID])  # Filtering student's application
            if len(application) > 0:
                application = application[0]
                if not application.selected:
                    if i[STUDENT_SELECTED] == True:
                        application.selected = True
                    else:
                        application.selected = False
                else:
                    raise ValueError("Student already selected")

                email = str(application.student.roll_no) + "@iitdh.ac.in"  # Only allowing for IITDh emails
                if opening_type == "Internship":
                    subject = STUDENT_APPLICATION_STATUS_TEMPLATE_SUBJECT.format(
                        company_name=application.internship.company_name,id=application.id)
                    data = {
                        "company_name": application.internship.company_name,
                        "designation": application.internship.designation,
                        "student_name": application.student.name
                    }
                else:
                    subject = STUDENT_APPLICATION_STATUS_TEMPLATE_SUBJECT.format(
                        company_name=application.placement.company_name,
                        id=application.id)
                    data = {
                        "company_name": application.placement.company_name,
                        "designation": application.placement.designation,
                        "student_name": application.student.name
                    }
                if application.selected:  # Sending corresponding email to students
                    sendEmail(email, subject, data, STUDENT_APPLICATION_STATUS_SELECTED_TEMPLATE)
                else:
                    sendEmail(email, subject, data, STUDENT_APPLICATION_STATUS_NOT_SELECTED_TEMPLATE)
                application.chaged_by = get_object_or_404(User, id=id)
                application.save()
            else:
                raise ValueError("Student - " + str(i[STUDENT_ID]) + " didn't apply for this opening")
        return Response({'action': "Mark Status", 'message': "Marked Status"},
                        status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'action': "Mark Status", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Mark Status: " + str(sys.exc_info()))
        return Response({'action': "Mark Status", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized([ADMIN])
def getDashboard(request, id, email, user_type):
    try:
        placements = Placement.objects.all().order_by('-created_at')
        ongoing = placements.filter(deadline_datetime__gt=timezone.now(), offer_accepted=True, email_verified=True)
        previous = placements.exclude(deadline_datetime__gt=timezone.now()).filter(
            offer_accepted=True, email_verified=True)
        new = placements.filter(offer_accepted__isnull=True, email_verified=True)
        internships=Internship.objects.all().order_by('-created_at')
        ongoing_internships = internships.filter(deadline_datetime__gt=timezone.now(), offer_accepted=True, email_verified=True)
        previous_internships = internships.exclude(deadline_datetime__gt=timezone.now()).filter(
            offer_accepted=True, email_verified=True)
        new_internships = internships.filter(offer_accepted__isnull=True, email_verified=True)
        ongoing = PlacementSerializerForAdmin(ongoing, many=True).data
        previous = PlacementSerializerForAdmin(previous, many=True).data
        new = PlacementSerializerForAdmin(new, many=True).data
        ongoing_internships = InternshipSerializerForAdmin(ongoing_internships, many=True).data
        previous_internships = InternshipSerializerForAdmin(previous_internships, many=True).data
        new_internships = InternshipSerializerForAdmin(new_internships, many=True).data

        return Response(
            {'action': "Get Dashboard - Admin", 'message': "Data Found", "ongoing": ongoing, "previous": previous,
             "new": new, "ongoing_internships": ongoing_internships, "previous_internships": previous_internships,
             "new_internships": new_internships},
            status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Get Dashboard - Admin", 'message': 'Student Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Get Dashboard - Admin: " + str(sys.exc_info()))
        return Response({'action': "Get Dashboard - Admin", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, DEADLINE_DATETIME])
def updateDeadline(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        
        # Updating deadline date with correct format in datetime field
        opening.deadline_datetime = datetime.datetime.strptime(data[DEADLINE_DATETIME], '%Y-%m-%d %H:%M:%S %z')
        opening.changed_by = get_object_or_404(User, id=id)
        opening.save()
        return Response({'action': "Update Deadline", 'message': "Deadline Updated"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Update Deadline", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Update Deadline: " + str(sys.exc_info()))
        return Response({'action': "Update Deadline", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized([SUPER_ADMIN])
@precheck([OPENING_ID, OFFER_ACCEPTED])
def updateOfferAccepted(request, id, email, user_type):
    try:
        data = request.data
        offer_accepted = data[OFFER_ACCEPTED]
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if DEADLINE_DATETIME in data:
            deadline_datetime = datetime.datetime.strptime(data[DEADLINE_DATETIME], '%Y-%m-%d %H:%M:%S %z')
        else:
            deadline_datetime = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=2)
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        if opening.offer_accepted is None:
            opening.offer_accepted = offer_accepted == "true"
            opening.deadline_datetime = deadline_datetime
            opening.changed_by = get_object_or_404(User, id=id)
            opening.save()
            if opening.offer_accepted:
                send_opening_notifications(opening.id,opening_type)
        else:
            raise ValueError("Offer Status already updated")

        return Response({'action': "Update Offer Accepted", 'message': "Offer Accepted Updated"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Update Offer Accepted", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'action': "Update Offer Accepted", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Update Offer Accepted: " + str(sys.exc_info()))
        return Response({'action': "Update Offer Accepted", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, EMAIL_VERIFIED])
def updateEmailVerified(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        opening.email_verified = True if data[EMAIL_VERIFIED] == "true" else False
        opening.changed_by = get_object_or_404(User, id=id)
        opening.save()
        return Response({'action': "Update Email Verified", 'message': "Email Verified Updated"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Update Email Verified", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Update Email Verified: " + str(sys.exc_info()))
        return Response({'action': "Update Email Verified", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, FIELD])
def deleteAdditionalInfo(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        if data[FIELD] in opening.additional_info:
            opening.additional_info.remove(data[FIELD])
            opening.changed_by = get_object_or_404(User, id=id)
            opening.save()
            return Response({'action': "Delete Additional Info", 'message': "Additional Info Deleted"},
                            status=status.HTTP_200_OK)
        else:
            raise ValueError("Additional Info Not Found")
    except Http404:
        return Response({'action': "Delete Additional Info", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'action': "Delete Additional Info", 'message': "Additional Info not found"},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.warning("Delete Additional Info: " + str(e))
        return Response({'action': "Delete Additional Info", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, FIELD])
def addAdditionalInfo(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        if data[FIELD] not in opening.additional_info:
            opening.additional_info.append(data[FIELD])
            opening.save()
            return Response({'action': "Add Additional Info", 'message': "Additional Info Added"},
                            status=status.HTTP_200_OK)
        else:
            raise ValueError("Additional Info Found")

    except Http404:
        return Response({'action': "Add Additional Info", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'action': "Add Additional Info", 'message': "Additional Info already found"},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.warning("Add Additional Info: " + str(e))
        return Response({'action': "Add Additional Info", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID])
def getApplications(request, id, email, user_type):
    try:
        data = request.GET
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
            applications = InternshipApplication.objects.filter(internship=opening)
            serializer = InternshipApplicationSerializerForAdmin(applications, many=True)
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
            applications = PlacementApplication.objects.filter(placement=opening)
            serializer = PlacementApplicationSerializerForAdmin(applications, many=True)
        return Response({'action': "Get Applications", 'message': 'Data Found', 'applications': serializer.data},
                            status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Get Applications", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Get Applications: " + str(sys.exc_info()))
        return Response({'action': "Get Applications", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[APPLICATION_ID, STUDENT_ID, OPENING_ID, ADDITIONAL_INFO, RESUME_FILE_NAME])
def submitApplication(request, id, email, user_type):
    try:
        data = request.data
        if OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, pk=data[OPENING_ID])
        else:
            opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        student = get_object_or_404(Student, pk=data[STUDENT_ID])
       # opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        student_user = get_object_or_404(User, id=student.id)
        if data[APPLICATION_ID] == "":
            application = PlacementApplication() if opening_type == "Placement" else InternshipApplication()
            application.id = generateRandomString()
            if(opening_type == "Placement"):
                application.placement = opening
            else:
                application.internship = opening
            application.student = student
            if data[RESUME_FILE_NAME] in student.resumes:
                application.resume = data[RESUME_FILE_NAME]
            else:
                raise FileNotFoundError(RESUME_FILE_NAME + " Not Found")
            additional_info = {}
            for i in opening.additional_info:
                if i not in data[ADDITIONAL_INFO]:
                    raise AttributeError(i + " not found in Additional Info")
                else:
                    additional_info[i] = data[ADDITIONAL_INFO][i]
            application.additional_info = json.dumps(additional_info)
            data = {
                "name": student.name,
                "company_name": opening.company_name,
                "application_type": "Placement" if opening_type == "Placement" else "Internship",
                "additional_info": dict(json.loads(application.additional_info)),
            }
            subject = STUDENT_APPLICATION_SUBMITTED_TEMPLATE_SUBJECT.format(company_name=opening.company_name)
            application.changed_by = get_object_or_404(User, id=id)
            application.save()
            sendEmail(student_user.email, subject, data, STUDENT_APPLICATION_SUBMITTED_TEMPLATE)
            return Response({'action': "Add Student Application", 'message': "Application added"},
                            status=status.HTTP_200_OK)
        else:
            if opening_type == "Internship":
                application = get_object_or_404(InternshipApplication, id=data[APPLICATION_ID])
            else:
                application = get_object_or_404(PlacementApplication, id=data[APPLICATION_ID])
            if application:
                if data[RESUME_FILE_NAME] in student.resumes:
                    application.resume = data[RESUME_FILE_NAME]
                else:
                    raise FileNotFoundError(RESUME_FILE_NAME + " Not Found")
                application.resume = data[RESUME_FILE_NAME]
                additional_info = {}
                for i in opening.additional_info:
                    if i not in data[ADDITIONAL_INFO]:
                        raise AttributeError(i + " not found in Additional Info")
                    else:
                        additional_info[i] = data[ADDITIONAL_INFO][i]

                application.additional_info = json.dumps(additional_info)
                data = {
                    "name": student.name,
                    "company_name": opening.company_name,
                    "application_type": "Placement" if opening_type == "Placement" else "Internship",
                    "resume": application.resume[16:],
                    "additional_info_items": dict(json.loads(application.additional_info)),
                }
                subject = STUDENT_APPLICATION_UPDATED_TEMPLATE_SUBJECT.format(company_name=opening.company_name)
                application.changed_by = get_object_or_404(User, id=id)
                application.save()
                sendEmail(student_user.email, subject, data, STUDENT_APPLICATION_UPDATED_TEMPLATE)
                return Response({'action': "Add Student Application", 'message': "Application updated"},
                                status=status.HTTP_200_OK)
            else:
                return Response({'action': "Edit Student Application", 'message': "No Application Found"},
                                status=status.HTTP_400_BAD_REQUEST)

    except Http404 as e:
        return Response({'action': "Submit Application", 'message': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return Response({'action': "Submit Application", 'message': str(e)},
                        status=status.HTTP_403_FORBIDDEN)
    except FileNotFoundError as e:
        return Response({'action': "Submit Application", 'message': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    except AttributeError as e:
        return Response({'action': "Submit Application", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Submit Application: " + str(sys.exc_info()))
        return Response({'action': "Submit Application", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[OPENING_ID])
def generateCSV(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        if opening_type == "Internship":
            opening = get_object_or_404(Internship, id=data[OPENING_ID])
            applications = InternshipApplication.objects.filter(internship=opening)
        else:
            opening = get_object_or_404(Placement, id=data[OPENING_ID])
            applications = PlacementApplication.objects.filter(placement=opening)
        filename = generateRandomString()
        if not os.path.isdir(STORAGE_DESTINATION_APPLICATION_CSV):
            os.mkdir(STORAGE_DESTINATION_APPLICATION_CSV)
        destination_path = STORAGE_DESTINATION_APPLICATION_CSV + filename + ".csv"
        f = open(destination_path, 'w')
        writer = csv.writer(f)
        header_row = APPLICATION_CSV_COL_NAMES.copy()

        header_row.extend(opening.additional_info)
        writer.writerow(header_row)
        for apl in applications:
            row_details = []

            row_details.append(apl.applied_at)
            row_details.append(apl.student.roll_no)
            row_details.append(apl.student.name)
            row_details.append(str(apl.student.roll_no) + "@iitdh.ac.in")
            row_details.append(apl.student.phone_number)
            row_details.append(apl.student.branch)
            row_details.append(apl.student.batch)
            row_details.append(apl.student.cpi)
            link = LINK_TO_STORAGE_RESUME + urllib.parse.quote(str(apl.student.id)) + "/" + urllib.parse.quote(str(apl.resume))
            row_details.append(link)
            row_details.append(apl.selected)

            for i in opening.additional_info:
                row_details.append(json.loads(apl.additional_info)[i])

            writer.writerow(row_details)
        f.close()
        file_path = LINK_TO_APPLICATIONS_CSV + urllib.parse.quote_plus(filename + ".csv")
        return Response({'action': "Create csv", 'message': "CSV created", 'file': file_path},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Create csv: " + str(sys.exc_info()))
        return Response({'action': "Create csv", 'message': "Something Went Wrong"+str(sys.exc_info())},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[COMPANY_NAME, COMPENSATION_GROSS, OFFER_ACCEPTED, STUDENT_ID, DESIGNATION, TIER])
def addPPO(request, id, email, user_type):
    try:
        data = request.data
        PPO = PrePlacementOffer()
        PPO.company = data[COMPANY_NAME]
        PPO.compensation = int(data[COMPENSATION_GROSS])
        if data[OFFER_ACCEPTED] == "true":
            PPO.accepted = True
        elif data[OFFER_ACCEPTED] == "false":
            PPO.accepted = False
        else:
            PPO.accepted = None
        PPO.student = get_object_or_404(Student, id=data[STUDENT_ID])
        PPO.designation = data[DESIGNATION]
        PPO.tier = int(data[TIER])
        if COMPENSATION_DETAILS in data:
            PPO.compensation_details = data[COMPENSATION_DETAILS]
        PPO.changed_by = get_object_or_404(User, id=id)
        PPO.save()
        return Response({'action': "Add PPO", 'message': "PPO added"},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Add PPO: " + str(sys.exc_info()))
        return Response({'action': "Add PPO", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[STUDENT_ID, OPENING_ID])
def getStudentApplication(request, id, email, user_type):
    try:
        data = request.data
        if  OPENING_TYPE  in data:
            opening_type= data[OPENING_TYPE]
        else:
            opening_type= "Placement"
        student = get_object_or_404(Student, id=data[STUDENT_ID])
        student_serializer = StudentSerializer(student)
        student_details = {
            "name": student_serializer.data['name'],
            "batch": student.batch,
            "branch": student.branch,
            "resume_list": student_serializer.data['resume_list'],
        }
        # search for the application if there or not
        if opening_type == "Internship":
            application = InternshipApplication.objects.filter(student=student,
                                                               internship=get_object_or_404(Internship,
                                                                                           id=data[OPENING_ID]))
        else:
            application = PlacementApplication.objects.filter(student=student,
                                                          placement=get_object_or_404(Placement, id=data[OPENING_ID]))
        
        if application:
            if opening_type == "Internship":
                serializer = InternshipApplicationSerializer(application[0])
                application_info = {
                    "id": serializer.data['id'],
                    "additional_info": serializer.data['additional_info'],
                    "resume": serializer.data['resume_link'],
                }
            else:
                serializer = PlacementApplicationSerializer(application[0])
                application_info = {
                    "id": serializer.data['id'],
                    "additional_info": serializer.data['additional_info'],
                    "resume": serializer.data['resume_link'],
                }
            return Response(
                {'action': "Get Student Application", 'application_found': "true", "application_info": application_info,
                 "student_details": student_details}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'action': "Get Student Application", 'application_found': "false", "student_details": student_details},
                status=status.HTTP_404_NOT_FOUND)
    except Http404:
        return Response({'action': "Get Student Application", 'message': "Student not found."},
                        status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Get Student Application: " + str(sys.exc_info()))
        return Response({'action': "Get Student Application", 'message': "Something Went Wrong"},
                        status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@isAuthorized(allowed_users=[ADMIN])
def getStats(request, id, email, user_type):
    try:
        stats = []
        placement_ids = {}

        tier_count = {
            "CSE": {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "psu":0,
            },
            "EE": {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "psu":0,
            },
            "MMAE": {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "psu":0,

            },
            "Total": {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "psu":0,
            },
        }
        number_of_students_placed = {
            "CSE": 0,
            "EE": 0,
            "MMAE": 0,
            "Total": 0,
        }
        number_of_students_with_multiple_offers = 0
        number_of_students_with_no_offers = {
            "CSE": 0,
            "EE": 0,
            "MMAE": 0,
            "Total": 0,
        }
        max_CTC = {
            "CSE": 0,
            "EE": 0,
            "MMAE": 0
        }
        average_CTC = {
            "CSE": 0,
            "EE": 0,
            "MMAE": 0
        }
        count = {
            "CSE": 0,
            "EE": 0,
            "MMAE": 0
        }



        students = Student.objects.all().order_by("roll_no")
        for student in students.iterator():

            applications = PlacementApplication.objects.filter(student=student, selected=True)
            ppos = PrePlacementOffer.objects.filter(student=student, accepted=True)

            first_offer_data = None

            second_offer_data = None

            # get the first and second offer
            offers = []
            offers.extend(applications)
            offers.extend(ppos)

            if len(offers) == 0:
                number_of_students_with_no_offers[student.branch] += 1
                number_of_students_with_no_offers["Total"] += 1
            else:
                number_of_students_placed[student.branch] += 1
                number_of_students_placed["Total"] += 1
                if len(offers) > 1:
                    number_of_students_with_multiple_offers += 1



            for offer in offers:
                if type(offer) == PrePlacementOffer:
                    if first_offer_data is None:
                        first_offer_data = {
                            "id": offer.id,
                            "company": offer.company,
                            "compensation": offer.compensation,
                            "tier": offer.tier,
                            "type": "PPO",
                        }
                    elif second_offer_data is None:
                        second_offer_data = {
                            "id": offer.id,
                            "company": offer.company,
                            "compensation": offer.compensation,
                            "tier": offer.tier,
                            "type": "PPO",
                        }
                elif type(offer) == PlacementApplication:
                    if first_offer_data is None:
                        first_offer_data = {
                            "id": offer.placement.id,
                            "company": offer.placement.company_name,
                            "compensation": offer.placement.compensation_CTC,
                            "tier": offer.placement.tier,
                            "type": "Placement",
                        }
                    elif second_offer_data is None:
                        second_offer_data = {
                            "id": offer.placement.id,
                            "company": offer.placement.company_name,
                            "compensation": offer.placement.compensation_CTC,
                            "tier": offer.placement.tier,
                            "type": "Placement",
                        }

            data = {
                "id": student.id,
                "name": student.name,
                "roll_no": student.roll_no,
                "batch": student.batch,
                "branch": student.branch,
                "cpi": student.cpi,
                "first_offer": first_offer_data['company'] if first_offer_data is not None else None,
                "first_offer_tier": first_offer_data['tier'] if first_offer_data is not None else None,
                "first_offer_compensation": first_offer_data['compensation'] if first_offer_data is not None else None,

                "second_offer": second_offer_data['company'] if second_offer_data is not None else None,
                "second_offer_tier": second_offer_data['tier'] if second_offer_data is not None else None,
                "second_offer_compensation": second_offer_data['compensation'] if second_offer_data is not None else None,
            }
            if first_offer_data is not None:
                tier_count[student.branch][first_offer_data['tier']] += 1
                tier_count['Total'][first_offer_data['tier']] += 1
                max_CTC[student.branch] = max(max_CTC[student.branch], first_offer_data['compensation'])
                average_CTC[student.branch] += first_offer_data['compensation']
                count[student.branch] += 1

                if first_offer_data['type'] == "Placement":
                    placement_ids[first_offer_data['company']] = first_offer_data['id']

            if second_offer_data is not None:
                tier_count[student.branch][second_offer_data['tier']] += 1
                tier_count['Total'][second_offer_data['tier']] += 1
                max_CTC[student.branch] = max(max_CTC[student.branch], second_offer_data['compensation'])
                average_CTC[student.branch] += second_offer_data['compensation']
                count[student.branch] += 1

                if second_offer_data['type'] == "Placement":
                    placement_ids[second_offer_data['company']] = second_offer_data['id']

            stats.append(data)

        for branch in average_CTC:
            if count[branch] > 0:
                average_CTC[branch] /= count[branch]
                # round off to 2 decimal places
                average_CTC[branch] = round(average_CTC[branch], 2)
            else:
                average_CTC[branch] = 0
        return Response({'action': "Get Stats", 'message': "Stats fetched", 'stats': stats, 'placement_ids': placement_ids,
                         "tier_count": {br: tier_count[br].values() for br in tier_count},
                         "number_of_students_placed": number_of_students_placed,
                         "number_of_students_with_multiple_offers": number_of_students_with_multiple_offers,
                         "number_of_students_with_no_offers": number_of_students_with_no_offers,
                         "max_CTC": max_CTC,
                         "average_CTC": average_CTC,
                         },
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Get Stats: " + str(sys.exc_info()))
        print(sys.exc_info())
        return Response({'action': "Get Stats", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)
