BRANCH_CHOICES = [
    ["CSE", "CSE"],
    ["EE", "EE"],
    ["ME", "ME"],
    ['EP', 'EP'],
]
BRANCHES = [
    "CSE",
    "EE",
    "ME",
    "EP"
]
BATCH_CHOICES = [
    ["2021", "2021"],
    ["2020", "2020"],
    ["2019", "2019"],
    ["2018", "2018"]
]

OFFER_CITY_TYPE = [
    ['Domestic', 'Domestic'],
    ['International', 'International']
]

TIERS = [
    ['psu', 'PSU'],
    ['1', 'Tier 1'],
    ['2', 'Tier 2'],
    ['3', 'Tier 3'],
    ['4', 'Tier 4'],
    ['5', 'Tier 5'],
    ['6', 'Tier 6']
]

TOTAL_BRANCHES = 4  # Total No of Branches
TOTAL_BATCHES = 4  # Total No of Batches

# To be Configured Properly
CLIENT_ID = "956830229554-290mirc16pdhd5j7ph7v7ukibo4t1qcp.apps.googleusercontent.com"  # Google Login Client ID

# To be Configured Properly
PLACEMENT_OPENING_URL = "http://localhost:3000/student/dashboard/placements/{id}"  # On frontend, this is the URL to be opened
LINK_TO_STORAGE_COMPANY_ATTACHMENT = "http://localhost/storage/Company_Attachments/"
LINK_TO_STORAGE_RESUME = "http://localhost/storage/Resumes/"
LINK_TO_APPLICATIONS_CSV = "http://localhost/storage/Application_CSV/"
LINK_TO_EMAIl_VERIFICATION_API = "http://localhost:3000/company/verifyEmail?token={token}"

EMAIL = "email"

STUDENT = 'student'
ADMIN = 'admin'
COMPANY = ''
TIER = 'tier'
# To be Configured Properly
FOURTH_YEAR = '2019'
MAX_OFFERS_PER_STUDENT = 2
EMAIL_VERIFICATION_TOKEN_TTL = 48  # in hours
JNF_TEXT_MAX_CHARACTER_COUNT = 100
JNF_TEXTMEDIUM_MAX_CHARACTER_COUNT = 200
JNF_TEXTAREA_MAX_CHARACTER_COUNT = 1000
JNF_SMALLTEXT_MAX_CHARACTER_COUNT = 50

STORAGE_DESTINATION_RESUMES = "./Storage/Resumes/"
STORAGE_DESTINATION_COMPANY_ATTACHMENTS = './Storage/Company_Attachments/'
STORAGE_DESTINATION_APPLICATION_CSV = './Storage/Application_CSV/'

TOKEN = 'token'
RESUME_FILE_NAME = 'resume_file_name'

APPLICATION_ID = "application_id"
OPENING_ID = "opening_id"
ADDITIONAL_INFO = "additional_info"
FIELD = "field"

STATUS_ACCEPTING_APPLICATIONS = "Accepting Applications"

PLACEMENT = "Placement"

COMPANY_NAME = "company_name"
ADDRESS = "address"
COMPANY_TYPE = "company_type"
NATURE_OF_BUSINESS = "nature_of_business"
TYPE_OF_ORGANISATION = "type_of_organisation"
WEBSITE = 'website'
COMPANY_DETAILS = "company_details"
COMPANY_DETAILS_PDF = "company_details_pdf"
IS_COMPANY_DETAILS_PDF = "is_company_details_pdf"
COMPANY_DETAILS_PDF_NAMES = "company_details_pdf_names"
PHONE_NUMBER = 'phone_number'
CONTACT_PERSON_NAME = 'contact_person_name'
CITY = 'city'
STATE = 'state'
COUNTRY = 'country'
PINCODE = 'pincode'

DESIGNATION = 'designation'
DESCRIPTION = 'description'
DESCRIPTION_PDF = 'description_pdf'
DESCRIPTION_PDF_NAMES = 'description_pdf_names'
IS_DESCRIPTION_PDF = 'is_description_pdf'
OPENING_TYPE = 'opening_type'
JOB_LOCATION = 'job_location'
COMPENSATION_CTC = 'compensation_ctc'
COMPENSATION_GROSS = 'compensation_gross'
COMPENSATION_TAKE_HOME = 'compensation_take_home'
COMPENSATION_BONUS = 'compensation_bonus'
COMPENSATION_DETAILS = 'compensation_details'
COMPENSATION_DETAILS_PDF = 'compensation_details_pdf'
COMPENSATION_DETAILS_PDF_NAMES = 'compensation_details_pdf_names'
IS_COMPENSATION_DETAILS_PDF = 'is_compensation_details_pdf'
ALLOWED_BATCH = 'allowed_batch'
ALLOWED_BRANCH = 'allowed_branch'
RS_ELIGIBLE = 'rs_eligible'
BOND_DETAILS = 'bond_details'
SELECTION_PROCEDURE_ROUNDS = 'selection_procedure_rounds'
SELECTION_PROCEDURE_DETAILS = 'selection_procedure_details'
SELECTION_PROCEDURE_DETAILS_PDF = 'selection_procedure_details_pdf'
SELECTION_PROCEDURE_DETAILS_PDF_NAMES = 'selection_procedure_details_pdf_names'
IS_SELECTION_PROCEDURE_DETAILS_PDF = 'is_selection_procedure_details_pdf'
TENTATIVE_DATE_OF_JOINING = 'tentative_date_of_joining'
TENTATIVE_NO_OF_OFFERS = 'tentative_no_of_offers'
OTHER_REQUIREMENTS = 'other_requirements'
DEADLINE_DATETIME = 'deadline_datetime'
OFFER_ACCEPTED = 'offer_accepted'
EMAIL_VERIFIED = 'email_verified'
RECAPTCHA_VALUE = 'recaptchakey'

STUDENT_LIST = "student_list"
STUDENT_ID = "student_id"
STUDENT_SELECTED = "student_selected"

EXCLUDE_IN_PDF = ['id', 'is_company_details_pdf', 'offer_accepted', 'is_description_pdf',
                  'is_compensation_details_pdf', 'is_selection_procedure_details_pdf',
                  'email_verified', 'created_at']
SPECIAL_FORMAT_IN_PDF = ['website', 'company_details_pdf_names', 'description_pdf_names',
                         'compensation_details_pdf_names',
                         'selection_procedure_details_pdf_names']

COMPANY_OPENING_SUBMITTED_TEMPLATE_SUBJECT = "Notification Submitted - {id} - Career Development Cell, IIT Dharwad"
STUDENT_APPLICATION_STATUS_TEMPLATE_SUBJECT = 'Application Status - {company_name} - {id}'
STUDENT_APPLICATION_SUBMITTED_TEMPLATE_SUBJECT = 'CDC - Application Submitted - {company_name}'
STUDENT_APPLICATION_UPDATED_TEMPLATE_SUBJECT = 'CDC - Application Updated - {company_name}'
COMPANY_EMAIl_VERIFICATION_TEMPLATE_SUBJECT = 'Email Verification - Career Development Cell, IIT Dharwad'
NOTIFY_STUDENTS_OPENING_TEMPLATE_SUBJECT = 'Placement Opportunity at {company_name}'

STUDENT_APPLICATION_SUBMITTED_TEMPLATE = 'student_application_submitted.html'
COMPANY_OPENING_SUBMITTED_TEMPLATE = 'company_opening_submitted.html'
STUDENT_APPLICATION_STATUS_SELECTED_TEMPLATE = 'student_application_status_selected.html'
STUDENT_APPLICATION_STATUS_NOT_SELECTED_TEMPLATE = 'student_application_status_not_selected.html'
STUDENT_APPLICATION_UPDATED_TEMPLATE = 'student_application_updated.html'
COMPANY_EMAIL_VERIFICATION_TEMPLATE = 'company_email_verification.html'
COMPANY_JNF_RESPONSE_TEMPLATE = 'company_jnf_response.html'
NOTIFY_STUDENTS_OPENING_TEMPLATE = 'notify_students_new_opening.html'

APPLICATION_CSV_COL_NAMES = ['Applied At', 'Roll No.', 'Name', 'Email', 'Phone Number', 'Branch', 'Batch', 'CPI',
                             'Resume', 'Selected', ]

PDF_FILES_SERVING_ENDPOINT = 'http://localhost/storage/Company_Attachments/'  # TODO: Change this to actual URL
