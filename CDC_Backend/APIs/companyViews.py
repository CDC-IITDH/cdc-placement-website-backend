from rest_framework.decorators import api_view

from .utils import *
from .serializers import *

logger = logging.getLogger('db')


@api_view(['POST'])
@precheck([COMPANY_NAME, ADDRESS, COMPANY_TYPE, NATURE_OF_BUSINESS, TYPE_OF_ORGANISATION, WEBSITE, COMPANY_DETAILS,
           IS_COMPANY_DETAILS_PDF, CONTACT_PERSON_NAME, PHONE_NUMBER, EMAIL, CITY, STATE, COUNTRY, PINCODE, DESIGNATION,
           DESCRIPTION,
           IS_DESCRIPTION_PDF, COMPENSATION_CTC, COMPENSATION_GROSS, COMPENSATION_TAKE_HOME, COMPENSATION_BONUS,
           IS_COMPENSATION_DETAILS_PDF, ALLOWED_BRANCH, RS_ELIGIBLE, SELECTION_PROCEDURE_ROUNDS,
           SELECTION_PROCEDURE_DETAILS,
           IS_SELECTION_PROCEDURE_DETAILS_PDF, TENTATIVE_DATE_OF_JOINING, TENTATIVE_NO_OF_OFFERS, OTHER_REQUIREMENTS,
           RECAPTCHA_VALUE, JOB_LOCATION
           ])
def addPlacement(request):
    logger.info("JNF filled by " + str(request.data['email']))
    logger.info(json.dumps(request.data))
    try:
        data = request.data
        files = request.FILES
        opening = Placement()
        if not verify_recaptcha(data[RECAPTCHA_VALUE]):
            raise Exception("Recaptcha Failed")

        opening.id = generateRandomString()
        # Add a company details in the opening
        opening.company_name = data[COMPANY_NAME]
        opening.address = data[ADDRESS]
        opening.company_type = data[COMPANY_TYPE]
        opening.nature_of_business = data[NATURE_OF_BUSINESS]
        opening.type_of_organisation = data[TYPE_OF_ORGANISATION]
        opening.website = data[WEBSITE]
        opening.company_details = data[COMPANY_DETAILS]
        opening.is_company_details_pdf = data[IS_COMPANY_DETAILS_PDF]
        if data[RS_ELIGIBLE] == 'Yes':
            opening.rs_eligible = True
        else:
            opening.rs_eligible = False

        if opening.is_company_details_pdf:
            company_details_pdf = []
            for file in files.getlist(COMPANY_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                company_details_pdf.append(saveFile(file, file_location))

            opening.company_details_pdf_names = company_details_pdf

        if data[IS_COMPANY_DETAILS_PDF] == "true" and len(opening.company_details_pdf_names) > 0:
            opening.is_company_details_pdf = True
        elif data[IS_COMPANY_DETAILS_PDF] == "false" and len(opening.company_details_pdf_names) == 0:
            opening.is_company_details_pdf = False
        else:
            raise ValueError('Invalid value for is_company_details_pdf')

        # Add a contact person details in the opening
        opening.contact_person_name = data[CONTACT_PERSON_NAME]
        # Check if Phone number is Integer
        if data[PHONE_NUMBER].isdigit():
            opening.phone_number = int(data[PHONE_NUMBER])
        else:
            raise ValueError('Phone number should be integer')

        opening.email = data[EMAIL]

        # Add a company location in the opening
        opening.city = data[CITY]
        opening.state = data[STATE]
        opening.country = data[COUNTRY]

        # Check if Pincode is Integer
        if data[PINCODE].isdigit():
            opening.pin_code = int(data[PINCODE])
        else:
            raise ValueError('Pincode should be integer')

        # If India then set city_type as Domestic else International
        if opening.country.upper() == 'INDIA':
            opening.city_type = 'Domestic'
        else:
            opening.city_type = 'International'

        # Add a designation details in the opening
        opening.designation = data[DESIGNATION]
        opening.description = data[DESCRIPTION]
        opening.job_location = data[JOB_LOCATION]
        opening.is_description_pdf = data[IS_DESCRIPTION_PDF]

        if opening.is_description_pdf:
            description_pdf = []
            for file in files.getlist(DESCRIPTION_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                description_pdf.append(saveFile(file, file_location))

            opening.description_pdf_names = description_pdf

            # Check if is_description_pdf is boolean
        if data[IS_DESCRIPTION_PDF] == "true" and len(opening.description_pdf_names) > 0:
            opening.is_description_pdf = True
        elif data[IS_DESCRIPTION_PDF] == "false" and len(opening.description_pdf_names) == 0:
            opening.is_description_pdf = False
        else:
            raise ValueError('Invalid value for is_description_pdf')

        # Add a compensation details in the opening
        # Check if compensation_ctc is integer
        if data[COMPENSATION_CTC].isdigit():
            opening.compensation_CTC = int(data[COMPENSATION_CTC])
        elif data[COMPENSATION_CTC] is None:
            opening.compensation_CTC = None
        else:
            raise ValueError('Compensation CTC must be an integer')

        # Check if compensation_gross is integer
        if data[COMPENSATION_GROSS].isdigit():
            opening.compensation_gross = int(data[COMPENSATION_GROSS])
        elif data[COMPENSATION_GROSS] is None:
            opening.compensation_gross = None
        else:
            raise ValueError('Compensation Gross must be an integer')

        # Check if compensation_take_home is integer
        if data[COMPENSATION_TAKE_HOME].isdigit():
            opening.compensation_take_home = int(data[COMPENSATION_TAKE_HOME])
        elif data[COMPENSATION_TAKE_HOME] is None:
            opening.compensation_take_home = None
        else:
            raise ValueError('Compensation Take Home must be an integer')

        # Check if compensation_bonus is integer
        if data[COMPENSATION_BONUS].isdigit():
            opening.compensation_bonus = int(data[COMPENSATION_BONUS])
        elif data[COMPENSATION_BONUS] is None:
            opening.compensation_bonus = None
        else:
            raise ValueError('Compensation Bonus must be an integer')

        opening.is_compensation_details_pdf = data[IS_COMPENSATION_DETAILS_PDF]

        if opening.is_compensation_details_pdf:
            compensation_details_pdf = []
            for file in files.getlist(COMPENSATION_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                compensation_details_pdf.append(saveFile(file, file_location))

            opening.compensation_details_pdf_names = compensation_details_pdf

        # Check if is_compensation_details_pdf is boolean
        if data[IS_COMPENSATION_DETAILS_PDF] == "true" and len(opening.compensation_details_pdf_names) > 0:
            opening.is_compensation_details_pdf = True
        elif data[IS_COMPENSATION_DETAILS_PDF] == "false" and len(opening.compensation_details_pdf_names) == 0:
            opening.is_compensation_details_pdf = False
        else:
            raise ValueError('Invalid value for is_compensation_details_pdf')

        opening.bond_details = data[BOND_DETAILS]

        # Check if selection_procedure_rounds is list
        if data[SELECTION_PROCEDURE_ROUNDS] is None:
            raise ValueError('Selection Procedure Rounds cannot be empty')
        else:
            try:
                opening.selection_procedure_rounds = json.loads(data[SELECTION_PROCEDURE_ROUNDS])
            except:
                raise ValueError('Selection Procedure Rounds must be a list')
        opening.selection_procedure_details = data[SELECTION_PROCEDURE_DETAILS]
        opening.is_selection_procedure_details_pdf = data[IS_SELECTION_PROCEDURE_DETAILS_PDF]

        if opening.is_selection_procedure_details_pdf == "true":
            selection_procedure_details_pdf = []
            for file in files.getlist(SELECTION_PROCEDURE_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                selection_procedure_details_pdf.append(saveFile(file, file_location))

            opening.selection_procedure_details_pdf_names = selection_procedure_details_pdf

        # Check if is_selection_procedure_details_pdf is boolean
        if data[IS_SELECTION_PROCEDURE_DETAILS_PDF] == "true" and len(
                opening.selection_procedure_details_pdf_names) > 0:
            opening.is_selection_procedure_details_pdf = True
        elif data[IS_SELECTION_PROCEDURE_DETAILS_PDF] == "false" and len(
                opening.selection_procedure_details_pdf_names) == 0:
            opening.is_selection_procedure_details_pdf = False
        else:
            raise ValueError('Invalid value for is_selection_procedure_pdf')

        stat, tier = getTier(opening.compensation_gross)
        if stat:
            opening.tier = tier
        else:
            raise ValueError('Invalid compensation gross')
        # Convert to date object
        opening.tentative_date_of_joining = datetime.datetime.strptime(data[TENTATIVE_DATE_OF_JOINING],
                                                                       '%d-%m-%Y').date()

        # Only Allowing Fourth Year for Placement
        opening.allowed_batch = [FOURTH_YEAR,]
        # Check if allowed_branch are valid
        if data[ALLOWED_BRANCH] is None:
            raise ValueError('Allowed Branch cannot be empty')
        elif set(json.loads(data[ALLOWED_BRANCH])).issubset(BRANCHES):
            opening.allowed_branch = json.loads(data[ALLOWED_BRANCH])
        else:
            raise ValueError('Allowed Branch must be a subset of ' + str(BRANCHES))

        # Check if tentative_no_of_offers is integer
        if data[TENTATIVE_NO_OF_OFFERS].isdigit():
            opening.tentative_no_of_offers = int(data[TENTATIVE_NO_OF_OFFERS])
        elif data[TENTATIVE_NO_OF_OFFERS] == 'null':
            opening.tentative_no_of_offers = None
        else:
            raise ValueError('Tentative No Of Offers must be an integer')

        opening.other_requirements = data[OTHER_REQUIREMENTS]

        opening.save()

        stat, link = generateOneTimeVerificationLink(opening.email, opening.id, "Placement")
        if not stat:
            raise RuntimeError("Error in generating one time verification link for placement")
        data = {
            "designation": opening.designation,
            "one_time_link": link,
            "opening_type": "Job"
        }

        sendEmail(opening.email, COMPANY_EMAIl_VERIFICATION_TEMPLATE_SUBJECT, data,
                  COMPANY_EMAIL_VERIFICATION_TEMPLATE)

        return Response({'action': "Add Placement", 'message': "Placement Added Successfully"},
                        status=status.HTTP_200_OK)

    except ValueError as e:
        store_all_files(request)
        exception_email(data)
        logger.warning("ValueError in addPlacement: " + str(e))
        logger.warning(traceback.format_exc())
        return Response({'action': "Add Placement", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        store_all_files(request)
        exception_email(data)
        logger.warning("Add New Placement: " + str(sys.exc_info()))
        logger.warning(traceback.format_exc())
        return Response({'action': "Add Placement", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@precheck([TOKEN])
def verifyEmail(request):
    try:
        data = request.data
        send_email_to_company = None
        token = data[TOKEN]
        # decode token
        decoded_token = jwt.decode(token, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithms=['HS256'])
        # get email, opening_id, opening_type from token
        email = decoded_token['email']
        opening_id = decoded_token['opening_id']
        opening_type = decoded_token['opening_type']
        # get opening based on opening_type and opening_id
        if opening_type == PLACEMENT:
            opening = get_object_or_404(Placement, id=opening_id)
            if email != opening.email:
                raise ValueError("Invalid Email")
            if not opening.email_verified:
                opening.email_verified = True
                send_email_to_company = True
            else:
                send_email_to_company = False
            opening.save()
        elif opening_type == INTERNSHIP:
            opening = get_object_or_404(Internship, id=opening_id)
            if email != opening.email:
                raise ValueError("Invalid Email")
            if not opening.email_verified:
                opening.email_verified = True
                send_email_to_company = True
            else:
                send_email_to_company = False
            opening.save()
        else:
            raise ValueError('Invalid opening type')

        if send_email_to_company:
            # Email sending part.
            send_email_for_opening(opening)

        return Response({'action': "Verify Email", 'message': "Email Verified Successfully"},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Verify Email", 'message': "Opening Not Found"},
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'action': "Verify Email", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Verify Email: " + str(sys.exc_info()))
        return Response({'action': "Verify Email", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@precheck([PLACEMENT_ID])
def autoFillJnf(request):
    try:
        data = request.GET
        placement_id = data.get(PLACEMENT_ID)
        opening = get_object_or_404(Placement, id=placement_id)
        serializer = AutofillSerializers(opening)
        return Response({'action': "Get AutoFill", 'message': 'Data Found', 'placement_data': serializer.data},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Get AutoFill", 'message': 'Placement Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.warning("Get AutoFill: " + traceback_str)
        return Response({'action': "Get AutoFill", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@precheck([INTERNSHIP_ID])
def autoFillInf(request):
    try:
        data = request.GET
        internship_id = data.get(INTERNSHIP_ID)
        opening = get_object_or_404(Internship, id=internship_id)
        serializer = AutofillSerializersInternship(opening)
        return Response({'action': "Get AutoFill ", 'message': 'Data Found', 'internship_data': serializer.data},
                        status=status.HTTP_200_OK)
    except Http404:
        return Response({'action': "Get AutoFill", 'message': 'Internship Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.warning("Get AutoFill: " + traceback_str)
        return Response({'action': "Get AutoFill", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

## Internships ## 


@api_view(['POST'])
@precheck([COMPANY_NAME, WEBSITE, IS_COMPANY_DETAILS_PDF, COMPANY_DETAILS, ADDRESS,
          CITY, STATE, COUNTRY, PINCODE, COMPANY_TYPE, NATURE_OF_BUSINESS, IS_DESCRIPTION_PDF,
          DESIGNATION, INTERNSHIP_LOCATION, DESCRIPTION, SEASON, START_DATE, END_DATE, WORK_TYPE,
          ALLOWED_BRANCH, SOPHOMORES_ELIIGIBLE, RS_ELIGIBLE, NUM_OFFERS, IS_STIPEND_DETAILS_PDF, STIPEND,
          FACILITIES, OTHER_FACILITIES, SELECTION_PROCEDURE_ROUNDS, SELECTION_PROCEDURE_DETAILS, IS_SELECTION_PROCEDURE_DETAILS_PDF,
          SELECTION_PROCEDURE_DETAILS, OTHER_REQUIREMENTS,
          CONTACT_PERSON_NAME, PHONE_NUMBER, EMAIL, RECAPTCHA_VALUE])
def addInternship(request):
    logger.info("INF filled by " + str(request.data['email']))
    logger.info(json.dumps(request.data))
    try:
        data = request.data
        files = request.FILES
        internship = Internship()
        if not verify_recaptcha(data[RECAPTCHA_VALUE]):
            raise Exception("Recaptcha Failed")
        
        internship.id = generateRandomString()
        # Add a company details in the internship
        internship.company_name = data[COMPANY_NAME]
        internship.website = data[WEBSITE]
        if data[IS_COMPANY_DETAILS_PDF] == "true":
            internship.is_company_details_pdf = True
        else:
            internship.is_company_details_pdf = False
        if internship.is_company_details_pdf:
            company_details_pdf = []
            for file in files.getlist(COMPANY_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + internship.id + '/'
                company_details_pdf.append(saveFile(file, file_location))
            internship.company_details_pdf_names = company_details_pdf

        internship.company_details = data[COMPANY_DETAILS]
        internship.address = data[ADDRESS]
        internship.city = data[CITY]
        internship.state = data[STATE]
        internship.country = data[COUNTRY]
        if internship.country.upper() == 'INDIA':
            internship.city_type = 'Domestic'
        else:
            internship.city_type = 'International'
        internship.pin_code = data[PINCODE]
        internship.company_type = data[COMPANY_TYPE]
        internship.nature_of_business = data[NATURE_OF_BUSINESS]

        if data[IS_DESCRIPTION_PDF] == "true":
            internship.is_description_pdf = True
        else:
            internship.is_description_pdf = False

        if internship.is_description_pdf:
            description_pdf = []
            for file in files.getlist(DESCRIPTION_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + internship.id + '/'
                description_pdf.append(saveFile(file, file_location))
            internship.description_pdf_names = description_pdf
        internship.designation = data[DESIGNATION]
        internship.location = data[INTERNSHIP_LOCATION]
        internship.description = data[DESCRIPTION]
        if data[SEASON] == "":
            raise ValueError('Season cannot be empty')
        elif set(json.loads(data[SEASON])).issubset(SEASONS):
            internship.season = json.loads(data[SEASON])
        else:
            raise ValueError('Season must be a subset of ' + str(SEASONS))
        internship.interning_period_from = datetime.datetime.strptime(data[START_DATE], '%d-%m-%Y').date()
        internship.interning_period_to = datetime.datetime.strptime(data[END_DATE], '%d-%m-%Y').date()

        if data[WORK_TYPE] == 'Work from home':
            internship.is_work_from_home = True
        else:
            internship.is_work_from_home = False
        
        if ALLOWED_BATCH in data[ALLOWED_BATCH] and data[ALLOWED_BATCH] is None or json.loads(data[ALLOWED_BATCH]) == "":
            raise ValueError('Allowed Batches cannot be empty')
        elif ALLOWED_BATCH in data[ALLOWED_BATCH] and set(json.loads(data[ALLOWED_BATCH])).issubset(BATCHES):
            internship.allowed_batch = json.loads(data[ALLOWED_BATCH])
        else:
            internship.allowed_batch = ['2021']
        
        if data[ALLOWED_BRANCH] is None or json.loads(data[ALLOWED_BRANCH]) == "":
            raise ValueError('Allowed Branch cannot be empty')
        elif set(json.loads(data[ALLOWED_BRANCH])).issubset(BRANCHES):
            internship.allowed_branch = json.loads(data[ALLOWED_BRANCH])
        else:
            raise ValueError('Allowed Branch must be a subset of ' + str(BRANCHES))

        if data[SOPHOMORES_ELIIGIBLE] == 'Yes':
            internship.sophomore_eligible = True
        else:
            internship.sophomore_eligible = False
        if data[RS_ELIGIBLE] == 'Yes':
            internship.rs_eligible = True
        else:
            internship.rs_eligible = False
        if data[NUM_OFFERS].isdigit():
            internship.tentative_no_of_offers = int(data[NUM_OFFERS])
        else:
            raise ValueError('Number of offers must be an integer')
        
        if data[IS_STIPEND_DETAILS_PDF] == "true":
            internship.is_stipend_description_pdf = True
        else:
            internship.is_stipend_description_pdf = False
            
        if internship.is_stipend_description_pdf:
            stipend_details_pdf = []
            for file in files.getlist(STIPEND_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + internship.id + '/'
                stipend_details_pdf.append(saveFile(file, file_location))
            internship.stipend_description_pdf_names = stipend_details_pdf

        if data[STIPEND].isdigit():
            internship.stipend = int(data[STIPEND])
        else:
            raise ValueError('Stipend must be an integer')
        if data[FACILITIES] != "" :
            if json.loads(data[FACILITIES]) == "":
                internship.facilities_provided = []
            elif set(json.loads(data[FACILITIES])).issubset(FACILITIES_CHOICES):
                internship.facilities_provided = json.loads(data[FACILITIES])
            else:
                raise ValueError('Facilities must be a subset of ' + str(FACILITIES_CHOICES))
        else:
            internship.facilities_provided = []

        internship.other_facilities = data[OTHER_FACILITIES]

        if data[SELECTION_PROCEDURE_ROUNDS] is None:
            raise ValueError('Selection Procedure Rounds cannot be empty')
        else:
            try:
                internship.selection_procedure_rounds = json.loads(data[SELECTION_PROCEDURE_ROUNDS])
            except:
                raise ValueError('Selection Procedure Rounds must be a list')
        
        internship.selection_procedure_details = data[SELECTION_PROCEDURE_DETAILS]

        if data[IS_SELECTION_PROCEDURE_DETAILS_PDF] == "true":
            internship.is_selection_procedure_details_pdf = True
        else:
            internship.is_selection_procedure_details_pdf = False

        if internship.is_selection_procedure_details_pdf:
            selection_procedure_details_pdf = []
            for file in files.getlist(SELECTION_PROCEDURE_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + internship.id + '/'
                selection_procedure_details_pdf.append(saveFile(file, file_location))
            internship.selection_procedure_details_pdf_names = selection_procedure_details_pdf
        
        internship.additional_facilities = data[OTHER_FACILITIES]
        #add additional info
        # Only Allowing Fourth Year for Placement
        
        

        internship.academic_requirements = data[OTHER_REQUIREMENTS]


        internship.contact_person_name = data[CONTACT_PERSON_NAME]
        internship.phone_number = data[PHONE_NUMBER]
        internship.email = data[EMAIL]
        internship.save()

        stat, link = generateOneTimeVerificationLink(internship.email, internship.id, "Internship")
        if not stat:
            raise RuntimeError("Error in generating one time verification link for internship")
        data = {
            "designation": internship.designation,
            "one_time_link": link,
            "opening_type": "Internship"
        }
    
        sendEmail(internship.email, COMPANY_EMAIl_VERIFICATION_TEMPLATE_SUBJECT, data,
                    COMPANY_EMAIL_VERIFICATION_TEMPLATE)
        
        return Response({'action': "Add Internship", 'message': "Internship Added Successfully"},
                        status=status.HTTP_200_OK)
    except ValueError as e:
        store_all_files(request)
        # exception_email(data)
        logger.warning("ValueError in addInternship: " + str(e))
        logger.warning(traceback.format_exc())
        return Response({'action': "Add Internship", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        store_all_files(request)
        # exception_email(data)
        logger.warning("Add New Internship: " + str(sys.exc_info()))
        logger.warning(traceback.format_exc())
        return Response({'action': "Add Internship", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)
