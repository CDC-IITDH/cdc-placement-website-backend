from .utils import *
from rest_framework.decorators import api_view

from .serializers import *


@api_view(['POST'])
@isAuthorized([ADMIN])
@precheck([OPENING_ID, STUDENT_LIST])
def markStatus(request, id, email, user_type):
    try:
        data = request.data
        applications = PlacementApplication.objects.filter(placement_id=data[OPENING_ID])  # Getting All
        # application from db for this opening
        for i in data[STUDENT_LIST]:
            application = applications.filter(student_id=i[STUDENT_ID])  # Filtering student's application
            if len(application) > 0:
                application = application[0]
                application.selected = i[STUDENT_STATUS]
                application.save()
                email = application.student.roll_no + "@iitdh.ac.in"  # Only allowing for IITDh emails
                subject = STUDENT_APPLICATION_STATUS_TEMPLATE_SUBJECT.format(company_name=application.placement.name,
                                                                             id=application.id)
                data = {
                    "company_name": application.placement.name,
                    "designation": application.placement.designation,
                    "student_name": application.student.name
                }
                if application.selected:  # Sending corresponding email to students
                    sendEmail(email, subject, data, STUDENT_APPLICATION_STATUS_SELECTED_TEMPLATE)
                    # This one needs to be created
                else:
                    sendEmail(email, subject, data, STUDENT_APPLICATION_STATUS_NOT_SELECTED_TEMPLATE)
                    # This one needs to be created
            else:
                raise ValueError("Student - " + i[STUDENT_ID] + " didn't apply for this opening")
        return Response({'action': "Mark Status", 'message': "Marked Status"},
                        status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'action': "Mark Status", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Mark Status: " + str(sys.exc_info()))
        return Response({'action': "Mark Status", 'message': "Error Occurred!"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@isAuthorized([ADMIN])
def getDashboard(request, id, email, user_type):
    try:

        placements = Placement.objects.all()
        ongoing = placements.filter(status=STATUS_ACCEPTING_APPLICATIONS)
        previous = placements.exclude(status = STATUS_ACCEPTING_APPLICATIONS)
        ongoing = PlacementSerializer(ongoing, many=True).data
        previous = PlacementSerializer(previous, many=True).data

        return Response(
            {'action': "Placement and Internships", 'message': "Data Found", "ongoing": ongoing, "previous": previous},
            status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Placements and Internships", 'message': 'Student Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except:
        logger.warning("Placements and Internships: " + str(sys.exc_info()))
        return Response({'action': "Placements and Internships", 'message': "Error Occurred"},
                        status=status.HTTP_400_BAD_REQUEST)
