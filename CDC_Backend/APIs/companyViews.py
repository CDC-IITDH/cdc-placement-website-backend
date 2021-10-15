import json
from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework.decorators import api_view

from .utils import *

logger = logging.getLogger('db')


@api_view(['POST'])
@precheck([OPENING_DESIGNATION, OPENING_DESCRIPTION, OPENING_TYPE, OPENING_CITY, OPENING_CITY_TYPE,
           OPENING_COMPENSATION, OPENING_COMPENSATION_DETAILS, OPENING_ALLOWED_BATCH, OPENING_ALLOWED_BRANCH,
           OPENING_ROUNDS, OPENING_CO_OP, OPENING_START_DATE, OPENING_ADDITIONAL_INFO,
           OPENING_DURATION, OPENING_ROUND_DETAILS])
def addOpening(request):
    try:
        data = request.data
        if data[OPENING_TYPE] == "Placement":
            opening = Placement()
        else:
            raise ValueError("Invalid Opening Type")

        opening.id = generateRandomString()
        # Create Company object here for every Opening


        #  Some new code above

        if data[OPENING_DESIGNATION] != "":
            opening.designation = data[OPENING_DESIGNATION]
        else:
            raise ValueError(OPENING_DESIGNATION + " Not Found")

        opening.description = data[OPENING_DESCRIPTION]

        if data[OPENING_START_DATE] != "":
            opening.description = data[OPENING_START_DATE]
        else:
            raise ValueError(OPENING_START_DATE + " Not Found")
        if data[OPENING_START_DATE] != "":
            opening.start_date = datetime.strptime(data[OPENING_START_DATE], '%d-%m-%Y')
        else:
            raise ValueError(OPENING_START_DATE + " Not Found")
        if data[OPENING_CITY] != "":
            opening.city = data[OPENING_CITY]
        else:
            raise ValueError(OPENING_CITY + " Not Found")
        if data[OPENING_CITY_TYPE] != "":
            opening.city_type = data[OPENING_CITY_TYPE]
        else:
            raise ValueError(OPENING_CITY_TYPE + " Not Found")
        if data[OPENING_COMPENSATION] != "":
            opening.compensation = data[OPENING_COMPENSATION]
        else:
            raise ValueError(OPENING_COMPENSATION + " Not Found")

        opening.compensation_details = data[OPENING_COMPENSATION_DETAILS]

        if data[OPENING_ALLOWED_BATCH] != "":
            if set(json.loads(data[OPENING_ALLOWED_BATCH])).issubset(BATCHES):
                opening.allowed_batch = json.loads(data[OPENING_ALLOWED_BATCH])
            else:
                raise ValueError(OPENING_ALLOWED_BATCH + " is Invalid")
        else:
            raise ValueError(OPENING_ALLOWED_BATCH + " Not Found")
        if data[OPENING_ALLOWED_BRANCH] != "":
            if set(json.loads(data[OPENING_ALLOWED_BRANCH])).issubset(BRANCHES):
                opening.allowed_branch = json.loads(data[OPENING_ALLOWED_BRANCH])
            else:
                raise ValueError(OPENING_ALLOWED_BATCH + " is Invalid")
        else:
            raise ValueError(OPENING_ALLOWED_BRANCH + " Not Found")

        opening.rounds = json.loads(data[OPENING_ROUNDS])

        opening.additional_info = json.loads(data[OPENING_ADDITIONAL_INFO])

        opening.status = STATUS_ACCEPTING_APPLICATIONS

        opening.rounds_details = json.loads(data[OPENING_ROUND_DETAILS])

        opening.created_at = make_aware(datetime.now())
        files = request.FILES.getlist(OPENING_ATTACHMENTS)
        attachments = []
        for file in files:
            attachments.append(saveFile(file, STORAGE_DESTINATION_COMPANY_ATTACHMENTS))

        opening.attachments = attachments
        opening.save()
        data = {
            "designation": opening.designation,
            "opening_type": data[OPENING_TYPE],
            "opening_link": "google.com",           # Some Changes here too
            "company_name": opening.company.name
        }

        # Needs some edits here

        email = 'This is temporary'

        # Delete the above var when done

        stat = sendEmail(email, COMPANY_OPENING_SUBMITTED_TEMPLATE_SUBJECT.format(id=opening.id), data,
                         COMPANY_OPENING_SUBMITTED_TEMPLATE)
        if stat is not True:
            logger.warning("Add New Opening: Unable to send email - " + stat)

        return Response({'action': "Add Opening", 'message': "Opening Added"},
                        status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'action': "Add Opening", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Add New Opening: " + str(sys.exc_info()))
        return Response({'action': "Add Opening", 'message': "Error Occurred {0}".format(
            str(sys.exc_info()[1]))},
                        status=status.HTTP_400_BAD_REQUEST)
