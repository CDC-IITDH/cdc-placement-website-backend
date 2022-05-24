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
        # Getting all application from db for this opening
        applications = PlacementApplication.objects.filter(placement_id=data[OPENING_ID])
        for i in data[STUDENT_LIST]:
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
                application.save()
            else:
                raise ValueError("Student - " + i[STUDENT_ID] + " didn't apply for this opening")
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
        ongoing = PlacementSerializerForAdmin(ongoing, many=True).data
        previous = PlacementSerializerForAdmin(previous, many=True).data
        new = PlacementSerializerForAdmin(new, many=True).data

        return Response(
            {'action': "Get Dashboard - Admin", 'message': "Data Found", "ongoing": ongoing, "previous": previous,
             "new": new},
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
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        # Updating deadline date with correct format in datetime field
        opening.deadline_datetime = datetime.datetime.strptime(data[DEADLINE_DATETIME], '%Y-%m-%d %H:%M:%S %z')
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
@isAuthorized([ADMIN])
@precheck([OPENING_ID, OFFER_ACCEPTED])
def updateOfferAccepted(request, id, email, user_type):
    try:
        data = request.data
        print(data)
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        opening.offer_accepted = True if data[OFFER_ACCEPTED] == True else False
        print(opening.offer_accepted)
        opening.save()
        return Response({'action': "Update Offer Accepted", 'message': "Offer Accepted Updated"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Update Offer Accepted", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
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
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        opening.email_verified = True if data[EMAIL_VERIFIED] == "true" else False
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
@precheck([OPENING_ID, ADDITIONAL_INFO])
def updateAdditionalInfo(request, id, email, user_type):
    try:
        data = request.data
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        if data[ADDITIONAL_INFO] == "":
            opening.additional_info = []
        elif isinstance(data[ADDITIONAL_INFO], list):
            opening.additional_info = data[ADDITIONAL_INFO]
        else:
            raise ValueError("Additional Info must be a list")
        opening.save()
        return Response({'action': "Update Additional Info", 'message': "Additional Info Updated"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Update Additional Info", 'message': 'Opening Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'action': "Update Additional Info", 'message': "Additional Info must be a list"},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.warning("Update Additional Info: " + str(e))
        return Response({'action': "Update Additional Info", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID])
def getApplications(request, id, email, user_type):
    try:
        data = request.GET
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
        student = get_object_or_404(Student, pk=data[STUDENT_ID])
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])

        if data[APPLICATION_ID] == "":
            application = PlacementApplication()
            application.id = generateRandomString()
            application.placement = opening
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
            application.save()
            return Response({'action': "Add Student Application", 'message': "Application added"},
                            status=status.HTTP_200_OK)
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
                application.save()
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
        placement = get_object_or_404(Placement, id=data[OPENING_ID])
        applications = PlacementApplication.objects.filter(placement=placement)
        filename = generateRandomString()
        if not os.path.isdir(STORAGE_DESTINATION_APPLICATION_CSV):
            os.mkdir(STORAGE_DESTINATION_APPLICATION_CSV)
        destination_path = STORAGE_DESTINATION_APPLICATION_CSV + filename + ".csv"
        f = open(destination_path, 'w')
        writer = csv.writer(f)
        header_row = APPLICATION_CSV_COL_NAMES.copy()

        header_row.extend(placement.additional_info)
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
            link = LINK_TO_STORAGE_RESUME + urllib.parse.quote(apl.student.id) + "/" + urllib.parse.quote(apl.resume)
            row_details.append(link)
            row_details.append(apl.selected)

            for i in placement.additional_info:
                row_details.append(json.loads(apl.additional_info)[i])

            writer.writerow(row_details)
        f.close()
        file_path = LINK_TO_APPLICATIONS_CSV + urllib.parse.quote_plus(filename + ".csv")
        return Response({'action': "Create csv", 'message': "CSV created", 'file': file_path},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Create csv: " + str(sys.exc_info()))
        print(sys.exc_info())
        return Response({'action': "Create csv", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[COMPANY_NAME, COMPENSATION_GROSS, OFFER_ACCEPTED, STUDENT_ID, DESIGNATION, TIER])
def addPPO(request, id, email, user_type):
    try:
        data = request.data
        PPO = PrePlacementOffer()
        PPO.company = data[COMPANY_NAME]
        PPO.compensation = data[COMPENSATION_GROSS]
        if data[OFFER_ACCEPTED] == "true":
            PPO.accepted = True
        elif data[OFFER_ACCEPTED] == "false":
            PPO.accepted = False
        else:
            PPO.accepted = None
        PPO.student = get_object_or_404(Student, id=data[STUDENT_ID])
        PPO.designation = data[DESIGNATION]
        PPO.tier = data[TIER]
        if COMPENSATION_DETAILS in data:
            PPO.compensation_details = data[COMPENSATION_DETAILS]
        PPO.save()
        return Response({'action': "Add PPO", 'message': "PPO added"},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Add PPO: " + str(sys.exc_info()))
        print(sys.exc_info())
        return Response({'action': "Add PPO", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[STUDENT_ID, OPENING_ID])
def getStudentApplication(request, id, email, user_type):
    try:
        data = request.data
        student = get_object_or_404(Student, id=data[STUDENT_ID])
        student_serializer = StudentSerializer(student)
        student_details = {
            "name": student_serializer.data['name'],
            "batch": student.batch,
            "branch": student.branch,
            "resume_list": student_serializer.data['resume_list'],
        }
        # search for the application if there or not
        application = PlacementApplication.objects.filter(student=student,
                                                          placement=get_object_or_404(Placement, id=data[OPENING_ID]))
        logger.info("Get Student Application: " + str(application))
        if application:
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
