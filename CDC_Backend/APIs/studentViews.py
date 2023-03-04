from rest_framework.decorators import api_view

from .serializers import *
from .utils import *

logger = logging.getLogger('db')


@api_view(['POST'])
@precheck(required_data=[AUTH_CODE])
@get_token()
@isAuthorized(allowed_users='*')
def login(request, id, email, user_type, token, refresh_token):
    try:
        return Response({'action': "Login", 'message': "Verified", "user_type": user_type, "id_token": token, "refresh_token": refresh_token},
                        status=status.HTTP_200_OK)
    except:
        return Response({'action': "Login", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@precheck(required_data=[REFRESH_TOKEN])
def refresh(request):
    refresh_token = request.data[REFRESH_TOKEN]
    data = {
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'refresh_token'
        }
    response = rq.post(OAUTH2_API_ENDPOINT, data=data)
    if response.status_code == 200:
        id_info = id_token.verify_oauth2_token(response.json()['id_token'], requests.Request(), CLIENT_ID)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_types = User.objects.filter(email=id_info['email']).values_list('user_type', flat=True)
        return Response({'action': "Refresh Token", 'message': "Token Refreshed", "id_token": response.json()['id_token'], "user_type": user_types[0]},
                        status=status.HTTP_200_OK)
    else:
        logger.error("refresh_token"+str(response))
        return Response({'action': "Refresh Token", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@isAuthorized(allowed_users=[STUDENT])
def studentProfile(request, id, email, user_type):
    try:
        studentDetails = get_object_or_404(Student, id=id)

        data = StudentSerializer(studentDetails).data
        return Response({'action': "Student Profile", 'message': "Details Found", "details": data},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Student Profile: " + str(sys.exc_info()))
        return Response({'action': "Student Profile", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[STUDENT])
def addResume(request, id, email, user_type):
    destination_path = ""
    try:
        student = get_object_or_404(Student, id=id)
        files = request.FILES

        if len(student.resumes) >= MAX_RESUMES_PER_STUDENT:
            raise PermissionError('Max Number of Resumes limit reached')

        file = files['file']
        destination_path = STORAGE_DESTINATION_RESUMES + str(student.roll_no) + "/"
        file_name = saveFile(file, destination_path)
        student.resumes.append(file_name)
        student.changed_by = get_object_or_404(User, id=id)
        student.save()
        return Response({'action': "Upload Resume", 'message': "Resume Added"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Upload Resume", 'message': 'Student Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except PermissionError:
        return Response({'action': "Upload Resume", 'message': 'Max Number of Resumes limit reached'},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        if path.exists(destination_path):
            logger.error("Upload Resume: Error in Saving Resume")
            remove(destination_path)
        else:
            logger.warning("Upload Resume: " + str(sys.exc_info()))
        return Response({'action': "Upload Resume", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized(allowed_users=[STUDENT])
def getDashboard(request, id, email, user_type):
    try:
        studentDetails = get_object_or_404(Student, id=id)

        placements = Placement.objects.filter(allowed_batch__contains=[studentDetails.batch],
                                              allowed_branch__contains=[studentDetails.branch],
                                              deadline_datetime__gte=datetime.datetime.now(),
                                              offer_accepted=True, email_verified=True).order_by('deadline_datetime')
        filtered_placements = placement_eligibility_filters(studentDetails, placements)

        placementsdata = PlacementSerializerForStudent(filtered_placements, many=True).data

        placementApplications = PlacementApplication.objects.filter(student_id=id)
        placementApplications = PlacementApplicationSerializer(placementApplications, many=True).data
        return Response(
            {'action': "Get Dashboard - Student", 'message': "Data Found", "placements": placementsdata,
             'placementApplication': placementApplications},
            status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Get Dashboard - Student", 'message': 'Student Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Get Dashboard -Student: " + str(sys.exc_info()))

        return Response({'action': "Get Dashboard - Student", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[STUDENT])
@precheck(required_data=[RESUME_FILE_NAME])
def deleteResume(request, id, email, user_type):
    try:
        student = get_object_or_404(Student, id=id)
        file_name = request.data[RESUME_FILE_NAME]
        if file_name not in student.resumes:
            return Response({'action': "Delete Resume", 'message': "Resume Not Found"},
                            status=status.HTTP_404_NOT_FOUND)

        destination_path = STORAGE_DESTINATION_RESUMES + id + "/" + str(file_name)
        if path.exists(destination_path):
            # remove(destination_path)
            student.resumes.remove(file_name)
            student.changed_by = get_object_or_404(User, id=id)
            student.save()
            return Response({'action': "Delete Resume", 'message': "Resume Deleted"},
                            status=status.HTTP_200_OK)
        else:
            raise FileNotFoundError("File Not Found")
    except Http404:
        return Response({'action': "Delete Resume", 'message': 'Student Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except FileNotFoundError as e:
        return Response({'action': "Delete Resume", 'message': 'File Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Delete Resume: " + str(sys.exc_info()))
        return Response({'action': "Delete Resume", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@isAuthorized(allowed_users=[STUDENT])
@precheck(required_data=[OPENING_TYPE, OPENING_ID, RESUME_FILE_NAME,
                         ])
def submitApplication(request, id, email, user_type):
    try:
        data = request.data
        student = get_object_or_404(Student, id=id)
        if not student.can_apply:
            return Response({'action': "Submit Application", 'message': "Student Can't Apply"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Only Allowing Applications for Placements
        if data[OPENING_TYPE] == PLACEMENT:
            if not len(PlacementApplication.objects.filter(
                    student_id=id, placement_id=data[OPENING_ID])):
                application = PlacementApplication()
                opening = get_object_or_404(Placement, id=data[OPENING_ID],
                                            allowed_batch__contains=[student.batch],
                                            allowed_branch__contains=[student.branch],
                                            deadline_datetime__gte=datetime.datetime.now().date()
                                            )
                if not opening.offer_accepted or not opening.email_verified:
                    raise PermissionError("Placement Not Approved")

                cond_stat, cond_msg = PlacementApplicationConditions(student, opening)
                if not cond_stat:
                    raise PermissionError(cond_msg)
                application.placement = opening
            else:
                raise PermissionError("Application is already Submitted")
        else:
            raise ValueError(OPENING_TYPE + " is Invalid")

        if data[RESUME_FILE_NAME] in student.resumes:
            application.resume = data[RESUME_FILE_NAME]
        else:
            raise FileNotFoundError(RESUME_FILE_NAME + " Not Found")

        application.student = student
        application.id = generateRandomString()
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
            "application_type": data[OPENING_TYPE],
            "additional_info": dict(json.loads(application.additional_info)),
        }
        subject = STUDENT_APPLICATION_SUBMITTED_TEMPLATE_SUBJECT.format(company_name=opening.company_name)
        sendEmail(email, subject, data, STUDENT_APPLICATION_SUBMITTED_TEMPLATE)
        application.changed_by = get_object_or_404(User, id=id)
        application.save()
        return Response({'action': "Submit Application", 'message': "Application Submitted"},
                        status=status.HTTP_200_OK)
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
@isAuthorized(allowed_users=[STUDENT])
@precheck(required_data=[APPLICATION_ID])
def deleteApplication(request, id, email, user_type):
    try:
        data = request.data
        application = get_object_or_404(PlacementApplication, id=data[APPLICATION_ID],
                                        student_id=id)
        if application.placement.deadline_datetime < timezone.now():
            raise PermissionError("Deadline Passed")

        application.delete()
        return Response({'action': "Delete Application", 'message': "Application Deleted"},
                        status=status.HTTP_200_OK)
    except Http404 as e:
        return Response({'action': "Delete Application", 'message': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return Response({'action': "Delete Application", 'message': str(e)},
                        status=status.HTTP_403_FORBIDDEN)
    except:
        logger.warning("Delete Application: " + str(sys.exc_info()))

        return Response({'action': "Delete Application", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized(allowed_users='*')
def getContributorStats(request, id, email, user_type):
    try:
        contributors = Contributor.objects.all()
        serialized_data = ContributorSerializer(contributors, many=True).data
        return Response({'action': "Get Contributor Stats", 'message': "Contributor Stats Fetched",
                            'data': serialized_data},
                        status=status.HTTP_200_OK)
    except:
        logger.warning("Get Contributor Stats: " + str(sys.exc_info()))

        return Response({'action': "Get Contributor Stats", 'message': "Something Went Wrong"},
                        status=status.HTTP_400_BAD_REQUEST)