from datetime import datetime

from .utils import *
from rest_framework.decorators import api_view

from .serializers import *


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, STUDENT_LIST])
def markStatus(request, id, email, user_type):
    try:
        data = request.data
        # Getting all application from db for this opening
        applications = PlacementApplication.objects.filter(placement_id=data[OPENING_ID])
        for i in data[STUDENT_LIST]:
            application = applications.filter(student_id=i[STUDENT_ID])  # Filtering student's application
            if len(application) > 0:
                application = application[0]
                application.selected = True if i[STUDENT_SELECTED] == "true" else False

                email = str(application.student.roll_no) + "@iitdh.ac.in"  # Only allowing for IITDh emails
                subject = STUDENT_APPLICATION_STATUS_TEMPLATE_SUBJECT.format(company_name=application.placement.company_name,
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
        ongoing = placements.filter(deadline_datetime__gt=datetime.now())
        previous = placements.exclude(deadline_datetime__gt=datetime.now())
        ongoing = PlacementSerializerForAdmin(ongoing, many=True).data
        previous = PlacementSerializerForAdmin(previous, many=True).data

        return Response(
            {'action': "Get Dashboard - Admin", 'message': "Data Found", "ongoing": ongoing, "previous": previous},
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
        opening.deadline_datetime = datetime.strptime(data[DEADLINE_DATETIME], '%Y-%m-%d %H:%M:%S %z')
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
        opening = get_object_or_404(Placement, pk=data[OPENING_ID])
        opening.offer_accepted = True if data[OFFER_ACCEPTED] == "true" else False
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
    except:
        logger.warning("Update Additional Info: " + str(sys.exc_info()))
        return Response({'action': "Update Additional Info", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)