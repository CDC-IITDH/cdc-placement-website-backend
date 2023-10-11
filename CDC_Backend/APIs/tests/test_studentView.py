# Create your tests here.
from ..models import *
from ..serializers import *
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..utils import *
import json
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class StudentViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email=str(os.environ.get("email_id")),
            id=str(os.environ.get("roll_no")),
            user_type=[STUDENT])
        self.assertEqual(
            self.user.email, User.objects.get(id=self.user.id).email)
        self.student = Student.objects.create(
            name="Test Student", id=self.user.id, resumes=["8BSLybntULgrPPm_beehyv.pdf"], roll_no=str(os.environ.get("roll_no")), branch="CSE", batch="2020",  phone_number=1234567890,  changed_by=self.user,  can_apply=True,
            can_apply_internship=True, degree="bTech", cpi=7.95,
        )
        self.assertEqual(self.student.name,
                         Student.objects.get(id=self.student.id).name)
        self.internship = Internship.objects.create(
            company_name="Test Company", id=generateRandomString(),  website="https://testwebsite.com",  address="Test Address",   company_type="Test Company Type",   offer_accepted=True,   season=["Summer"],   allowed_branch=["CSE"],
            allowed_batch=["2020"],  contact_person_name="Test Contact Person",  phone_number="1234567890",  email="test@test.com",  email_verified=True,  stipend=10000,
        )

        self.placement = Placement.objects.create(
            company_name="Test Company", id=generateRandomString(), website="https://testwebsite.com", address="Test Address", company_type="Test Company Type",  offer_accepted=True,   tier="6", allowed_branch=["CSE"], allowed_batch=["2020"],
            contact_person_name="Test Contact Person", phone_number="1234567890", email="test@test.com",  email_verified=True,

        )

        self.assertEqual(self.placement.company_name, Placement.objects.get(
            id=self.placement.id).company_name)

        self.internship_application = InternshipApplication.objects.create(
            id=generateRandomString(), internship=self.internship, student=self.student, resume="8BSLybntULgrPPm_beehyv.pdf", selected=True

        )

        self.assertEqual(self.internship_application.internship.company_name, InternshipApplication.objects.get(
            id=self.internship_application.id).internship.company_name)
        self.placement_application = PlacementApplication.objects.create(
            id=generateRandomString(), placement=self.placement, student=self.student, resume="8BSLybntULgrPPm_beehyv.pdf", selected=True

        )

        self.assertEqual(self.placement_application.placement.company_name, PlacementApplication.objects.get(
            id=self.placement_application.id).placement.company_name)
        self.issue = Issues.objects.create(
            student=self.student, title="Test Issue", description="Test Issue Description", opening_id=self.internship.id,
            opening_type=INTERNSHIP
        )

        # get token from google OAuth API
        response = self.client.post(reverse('Refresh Token'), {
                                    'refresh_token': os.environ.get("refresh_token")}, format='json')
        self.student_token = response.data['id_token']

    def test_student_accept_offer_internship(self):
        url = reverse('Student Accept Offer')
        data = {
            'opening_id': self.internship.id,
            'offer_accepted': True,
            'opening_type': INTERNSHIP
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Updated Offer Status')
        self.assertEqual(InternshipApplication.objects.get(
            id=self.internship_application.id).offer_accepted, True)

    def test_student_accept_offer_internship_notFound(self):
        url = reverse('Student Accept Offer')
        data = {
            'opening_id': self.internship.id,
            'offer_accepted': True,
            'opening_type': INTERNSHIP
        }
        self.internship_application.selected = False
        self.internship_application.offer_accepted = False
        self.internship_application.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Offer Not Found')
        self.assertEqual(InternshipApplication.objects.get(
            id=self.internship_application.id).offer_accepted, False)

    def test_delete_application_internship(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.internship_application.id,
            'opening_type': INTERNSHIP
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Deleted')
        self.assertEqual(InternshipApplication.objects.filter(
            id=self.internship_application.id).count(), 0)

    def test_delete_application_internship_deadlinePassed(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.internship_application.id,
            'opening_type': INTERNSHIP
        }
        self.internship.deadline_datetime = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.internship.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Deadline Passed')
        self.assertEqual(InternshipApplication.objects.filter(
            id=self.internship_application.id).count(), 1)

    def test_delete_application_internship_notFound(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.internship_application.id,
            'opening_type': INTERNSHIP
        }
        self.internship_application.delete()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No InternshipApplication matches the given query.')
        self.assertEqual(InternshipApplication.objects.filter(
            id=self.internship_application.id).count(), 0)

    # def test_add_application_internship(self):
    #     url = reverse('Delete Application')
    #     data = {
    #         'application_id': self.internship_application.id,
    #         'opening_type': INTERNSHIP
    #     }
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer ' + self.student_token)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Application Deleted')
    #     self.assertEqual(InternshipApplication.objects.filter(
    #         id=self.internship_application.id).count(), 0)
    #     # deleted existing application
    #     url = reverse('Add Application')
    #     data = {
    #         OPENING_ID: self.internship.id,
    #         OPENING_TYPE: INTERNSHIP,
    #         RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
    #         ADDITIONAL_INFO: []
    #     }
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer ' + self.student_token)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Application Submitted')
    #     self.assertEqual(InternshipApplication.objects.filter(
    #         student=self.student).count(), 1)
    #     self.internship_application = InternshipApplication.objects.filter(
    #         student=self.student)
    #     # self.internship.deadline_datetime = timezone.now().replace(
    #     #     hour=0, minute=0, second=0, microsecond=0)
    #     # self.internship.save()

    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data['message'],
    #                      'Application is already Submitted')
    #     self.assertEqual(InternshipApplication.objects.filter(
    #         student=self.student).count(), 1)
    #     self.internship_application.delete()
    #     data[OPENING_ID] = generateRandomString()
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['message'],
    #                      'No Internship matches the given query.')
    #     self.assertEqual(InternshipApplication.objects.filter(
    #         student=self.student).count(), 0)

    def test_student_accept_offer_placement(self):
        url = reverse('Student Accept Offer')
        data = {
            'opening_id': self.placement.id,
            'offer_accepted': True,
            'opening_type': PLACEMENT
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Updated Offer Status')
        self.assertEqual(PlacementApplication.objects.get(
            id=self.placement_application.id).offer_accepted, True)

    def test_student_accept_offer_placement_offerNotFound(self):
        url = reverse('Student Accept Offer')
        data = {
            'opening_id': self.placement.id,
            'offer_accepted': True,
            'opening_type': PLACEMENT
        }
        self.placement_application.selected = False
        self.placement_application.offer_accepted = False
        self.placement_application.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Offer Not Found')
        self.assertEqual(PlacementApplication.objects.filter(
            id=self.placement_application.id, selected=True).count(), 0)
        self.assertEqual(PlacementApplication.objects.get(
            id=self.placement_application.id).offer_accepted, False)

    def test_delete_application_placement(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.placement_application.id,
            'opening_type': PLACEMENT
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Deleted')
        self.assertEqual(PlacementApplication.objects.filter(
            id=self.placement_application.id).count(), 0)

    def test_delete_application_placement_notFound(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.placement_application.id,
            'opening_type': PLACEMENT
        }
        self.placement_application.delete()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No PlacementApplication matches the given query.')
        self.assertEqual(PlacementApplication.objects.filter(
            id=self.placement_application.id).count(), 0)

    def test_delete_application_placement_deadlinePassed(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.placement_application.id,
            'opening_type': PLACEMENT
        }
        self.placement.deadline_datetime = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.placement.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Deadline Passed')
        self.assertEqual(PlacementApplication.objects.filter(
            id=self.placement_application.id).count(), 1)

    def test_add_application_placement(self):
        self.placement.additional_info = ["Test"]
        self.placement_application.delete()
        # deleted existing application
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: [{"Test": "Test"}]
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Submitted')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student).count(), 1)

    def test_add_application_placement_deadlinePassed(self):
        self.placement.deadline_datetime = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(minutes=5)
        self.placement.save()
        # deleted existing application
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         'No Placement matches the given query.')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_alreadyApplied(self):
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Application is already Submitted')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 1)

    def test_add_application_placement_notFound(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }

        data[OPENING_ID] = generateRandomString()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         'No Placement matches the given query.')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student).count(), 0)

    def test_add_application_placement_notApproved(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.placement.offer_accepted = False
        self.placement.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Placement Not Approved')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_notEmailVerified(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.placement.email_verified = False
        self.placement.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Placement Not Approved')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_notRegistered(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.student.can_apply = False
        self.student.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Student Can't Apply")
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_InvalidOpeningtype(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: "Invalid",
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Something Went Wrong")
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_InvalidResume(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: 'Invalid',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         "resume_file_name Not Found")
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_add_application_placement_MissingAdditionalInfo(self):
        self.placement_application.delete()
        url = reverse('Add Application')
        self.placement.additional_info = ["Test"]
        self.placement.save()
        data = {

            OPENING_ID: self.placement.id,
            OPENING_TYPE: PLACEMENT,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Something Went Wrong")
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student, placement=self.placement).count(), 0)

    def test_getdashboard(self):
        url = reverse('Dashboard')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Data Found')
        internships = Internship.objects.filter(allowed_batch__contains=[self.student.batch],
                                                allowed_branch__contains=[
            self.student.branch],
            deadline_datetime__gte=datetime.datetime.now(),
            offer_accepted=True, email_verified=True)
        placements = Placement.objects.filter(allowed_batch__contains=[self.student.batch],
                                              allowed_branch__contains=[
                                                  self.student.branch],
                                              deadline_datetime__gte=datetime.datetime.now(),
                                              offer_accepted=True, email_verified=True)

        filtered_internships = internship_eligibility_filters(
            self.student, internships)
        filtered_placements = placement_eligibility_filters(
            self.student, placements)
        self.assertEqual(
            len(response.data['internships']), len(filtered_internships))
        self.assertEqual(
            len(response.data['placements']), len(filtered_placements))
        self.assertEqual(len(response.data['placementApplication']), 1)
        self.assertEqual(len(response.data['internshipApplication']), 1)
        self.assertEqual(response.data['placementApplication'][0]
                         ['placement']['company_name'], self.placement.company_name)
        self.assertEqual(response.data['internshipApplication'][0]
                         ['internship']['company_name'], self.internship.company_name)

    # def test_get_contributor_stats(self):
    #     url = reverse('get_contributor_stats', kwargs={'id': self.student.id})
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.contributor_token)
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Contributor Stats Fetched')
    #     self.assertEqual(len(response.data['data']), 1)
    #     self.assertEqual(response.data['data'][0]['name'], self.contributor.name)
    #     self.assertEqual(response.data['data'][0]['email'], self.contributor.email)
    #     self.assertEqual(response.data['data'][0]['contribution_count'], self.contributor.contribution_count)

    def test_add_issue(self):
        url = reverse('Add Issue')
        data = {
            'Title': 'Test Issue 2',
            'Description': 'Test Issue Description 2',
            'opening_id': self.placement.id,
            'opening_type': PLACEMENT
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Issue Added')
        self.assertEqual(Issues.objects.filter(
            student=self.student).count(), 2)
        self.assertEqual(Issues.objects.filter(
            opening_id=self.placement.id).count(), 1)
        self.assertEqual(Issues.objects.filter(
            opening_type=PLACEMENT).count(), 1)

    def test_add_application_internship(self):
        self.internship.additional_info = ["Test"]
        self.internship_application.delete()
        # deleted existing application
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: [{"Test": "Test"}]
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Submitted')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student).count(), 1)

    def test_add_application_internship_deadlinePassed(self):
        # now minus 5 minutes
        self.internship.deadline_datetime = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(minutes=5)
        
        self.internship.save()
        # deleted existing application
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         'No Internship matches the given query.')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_alreadyApplied(self):
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Application is already Submitted')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 1)

    def test_add_application_internship_notFound(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }

        data[OPENING_ID] = generateRandomString()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         'No Internship matches the given query.')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student).count(), 0)

    def test_add_application_internship_notApproved(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.internship.offer_accepted = False
        self.internship.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Internship Not Approved')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_notEmailVerified(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.internship.email_verified = False
        self.internship.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'Internship Not Approved')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_notRegistered(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.student.can_apply_internship = False
        self.student.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Student Can't Apply")
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_InvalidOpeningtype(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: "Invalid",
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Something Went Wrong")
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_InvalidResume(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: 'Invalid',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         "resume_file_name Not Found")
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_add_application_internship_MissingAdditionalInfo(self):
        self.internship_application.delete()
        url = reverse('Add Application')
        self.internship.additional_info = ["Test"]
        self.internship.save()
        data = {

            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf',
            ADDITIONAL_INFO: []
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "Something Went Wrong")
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student, internship=self.internship).count(), 0)

    def test_getStudentProfile(self):
        url = reverse('Student Profile')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Details Found')
        self.assertEqual(response.data['details']['id'], self.student.id)
        self.assertEqual(response.data['details']['roll_no'],
                         self.student.roll_no)
        self.assertEqual(response.data['details']['name'], self.student.name)
        self.assertEqual(response.data['details']['batch'], self.student.batch)
        self.assertEqual(response.data['details']['branch'],
                         self.student.branch)
        self.assertEqual(response.data['details']['phone_number'],
                         self.student.phone_number)
        self.assertEqual(response.data['details']
                         ['cpi'], str(self.student.cpi))
        for i in range(len(response.data['details']['resume_list'])):
            self.assertIn(
                response.data['details']['resume_list'][i]['name'], self.student.resumes)
        for i in range(len(response.data['details']['offers'])):
            self.assertIn(response.data['details']['offers'][i]
                          ['application_id'], self.placement_application.id)

    def test_addResume_success(self):
        pdf = SimpleUploadedFile(
            'kalera.pdf', b'content', content_type='application/pdf')
        url = reverse('Upload Resume')
        files = {'file': pdf}
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, files, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Resume Added')

    def test_add_resume_max_limit_reached(self):
        pdf = SimpleUploadedFile(
            'kalera.pdf', b'content', content_type='application/pdf')
        url = reverse('Upload Resume')
        files = {'file': pdf}
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        self.student.resumes = ['resume1.pdf', 'resume2.pdf', 'resume3.pdf']
        self.student.save()
        response = self.client.post(url, files, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                         'action': 'Upload Resume', 'message': 'Max Number of Resumes limit reached'})
        self.student.refresh_from_db()
        self.assertEqual(len(self.student.resumes), 3)

    def test_deleteResume_success(self):
        destination_path = STORAGE_DESTINATION_RESUMES + \
            self.student.id+'/'+"8BSLybntULgrPPm_beehyv.pdf"
        # check it whats this above without this test giving error
        with open(destination_path, 'w') as f:
            f.write('test')
            f.close()
        # create a file here

        url = reverse('Delete Resume')
        data = {
            'resume_file_name': '8BSLybntULgrPPm_beehyv.pdf'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Resume Deleted')
        self.student.refresh_from_db()
        self.assertEqual(self.student.resumes, [])
        remove(destination_path)

    def test_deleteResume_invalidResume(self):
        url = reverse('Delete Resume')
        data = {
            'resume_file_name': 'Invalid'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         'Resume Not Found')
        self.student.refresh_from_db()
        self.assertEqual(self.student.resumes, ['8BSLybntULgrPPm_beehyv.pdf'])

    def test_deleteResume_missingResumeinStorage(self):
        url = reverse('Delete Resume')
        data = {
            'resume_file_name': '8BSLybntULgrPPm_beehyv.pdf'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'File Not Found')
