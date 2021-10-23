import json
from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework.decorators import api_view

from .utils import *

logger = logging.getLogger('db')


@api_view(['POST'])
@precheck([DESIGNATION, DESCRIPTION, OPENING_TYPE, CITY, CITY_TYPE,
           COMPENSATION, COMPENSATION_DETAILS, ALLOWED_BATCH, ALLOWED_BRANCH,
           ROUNDS, CO_OP, START_DATE, ADDITIONAL_INFO,
           DURATION, ROUND_DETAILS])
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

        if data[DESIGNATION] != "":
            opening.designation = data[DESIGNATION]
        else:
            raise ValueError(DESIGNATION + " Not Found")

        opening.description = data[DESCRIPTION]

        if data[START_DATE] != "":
            opening.description = data[START_DATE]
        else:
            raise ValueError(START_DATE + " Not Found")
        if data[START_DATE] != "":
            opening.start_date = datetime.strptime(data[START_DATE], '%d-%m-%Y')
        else:
            raise ValueError(START_DATE + " Not Found")
        if data[CITY] != "":
            opening.city = data[CITY]
        else:
            raise ValueError(CITY + " Not Found")
        if data[CITY_TYPE] != "":
            opening.city_type = data[CITY_TYPE]
        else:
            raise ValueError(CITY_TYPE + " Not Found")
        if data[COMPENSATION] != "":
            opening.compensation = data[COMPENSATION]
        else:
            raise ValueError(COMPENSATION + " Not Found")

        opening.compensation_details = data[COMPENSATION_DETAILS]

        if data[ALLOWED_BATCH] != "":
            if set(json.loads(data[ALLOWED_BATCH])).issubset(BATCHES):
                opening.allowed_batch = json.loads(data[ALLOWED_BATCH])
            else:
                raise ValueError(ALLOWED_BATCH + " is Invalid")
        else:
            raise ValueError(ALLOWED_BATCH + " Not Found")
        if data[ALLOWED_BRANCH] != "":
            if set(json.loads(data[ALLOWED_BRANCH])).issubset(BRANCHES):
                opening.allowed_branch = json.loads(data[ALLOWED_BRANCH])
            else:
                raise ValueError(ALLOWED_BATCH + " is Invalid")
        else:
            raise ValueError(ALLOWED_BRANCH + " Not Found")

        opening.rounds = json.loads(data[ROUNDS])

        opening.additional_info = json.loads(data[ADDITIONAL_INFO])

        opening.status = STATUS_ACCEPTING_APPLICATIONS

        opening.rounds_details = json.loads(data[ROUND_DETAILS])

        opening.created_at = make_aware(datetime.now())
        files = request.FILES.getlist(ATTACHMENTS)
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
