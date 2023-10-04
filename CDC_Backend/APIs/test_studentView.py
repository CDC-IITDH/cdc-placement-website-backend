# Create your tests here.
from .models import *
from .serializers import *
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .utils import *
import json
from django.utils import timezone



class StudentViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user= User.objects.create(
            email=str(os.environ.get("email")),
            id=generateRandomString(),
            user_type=[STUDENT])
        self.assertEqual(self.user.email, User.objects.get(id=self.user.id).email)
        self.student = Student.objects.create(
            name="Test Student",
            id=self.user.id,
            resumes=["8BSLybntULgrPPm_beehyv.pdf"],
           #email="test@student.com",
            #password="testpassword",
            roll_no="200010052",
            branch="CSE",
            batch="2020",
            phone_number="1234567890",
           # resume_link="https://testresume.com"
            changed_by=self.user,
            can_apply=True,
            can_apply_internship=True,
            degree="bTech",
            cpi=7.95,
        )
        self.assertEqual(self.student.name, Student.objects.get(id=self.student.id).name)
        # self.user=User.objects.filter(email="200010052@iitdh.ac.in").first()
        # self.student = Student.objects.filter(id=self.user.id).first()
        self.internship = Internship.objects.create(
            company_name="Test Company",
            id=generateRandomString(),
            website="https://testwebsite.com",
            address="Test Address",
            company_type="Test Company Type",
            offer_accepted=True,
            season=["Summer"],
            allowed_branch=["CSE"],
            allowed_batch=["2020"],
            contact_person_name="Test Contact Person",
            phone_number="1234567890",
            email="test@test.com",
            email_verified=True,
            deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1),
           # location="Test Location",
            stipend=10000,
           # apply_link="https://testapplylink.com"
        )
       # self.assertEqual(self.internship.company_name, Internship.objects.get(self.internship.id).company_name)
        # self.internship1 =Internship.objects.create(
        #     company_name="Test Company1",
        #     id=generateRandomString(),
        #     website="https://testwebsite1.com",
        #     address="Test Address1",
        #     company_type="Test Company Type1",
        #     offer_accepted=True,
        #     season=["Summer"],
        #     allowed_branch=["CSE"],
        #     allowed_batch=["2020"],
        #     contact_person_name="Test Contact Person1",
        #     phone_number="1234567890",
        #     email="test@test1.com",
        #     email_verified=True,
        #     deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1),
        #     stipend=10000,

        # )
        self.placement = Placement.objects.create(
            company_name="Test Company",
            id=generateRandomString(),
            website="https://testwebsite.com",
            address="Test Address",
            company_type="Test Company Type",
            offer_accepted=True,
            tier="6",
           # season="Summer",
            allowed_branch=["CSE"],
            allowed_batch=["2020"],
            contact_person_name="Test Contact Person",
            phone_number="1234567890",
            email="test@test.com",
            email_verified=True,
            deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1),
        )
        # self.placement1 = Placement.objects.create(
        #     company_name="Test Company1",
        #     id=generateRandomString(),
        #     website="https://testwebsite1.com",
        #     address="Test Address1",
        #     company_type="Test Company Type1",
        #     offer_accepted=True,
        #     tier="7",
        #     # season="Summer",
        #     allowed_branch=["CSE"],
        #     allowed_batch=["2020"],
        #     contact_person_name="Test Contact Person1",
        #     phone_number="1234567890",
        #     email="test@test1.com",
        #     email_verified=True,
        #     deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1),
        # )
        #self.assertEqual(self.placement.tier,"1")
        self.assertEqual(self.placement.company_name, Placement.objects.get(id=self.placement.id).company_name)
        self.internship_application = InternshipApplication.objects.create(
            id=generateRandomString(),
            internship=self.internship,
            student=self.student,
            resume="8BSLybntULgrPPm_beehyv.pdf",
            selected=True
           # status="Applied"
        )
        # self.internship_application1=InternshipApplication.objects.create(
        #     id=generateRandomString(),
        #     internship=self.internship1,
        #     student=self.student,
        #     resume="8BSLybntULgrPPm_beehyv.pdf"
        #     )
        self.assertEqual(self.internship_application.internship.company_name, InternshipApplication.objects.get(id=self.internship_application.id).internship.company_name)
        self.placement_application = PlacementApplication.objects.create(
            id=generateRandomString(),
            placement=self.placement,
            student=self.student,
            resume="8BSLybntULgrPPm_beehyv.pdf",
            selected=True
           # status="Applied"
        )
        # self.placement_application1 = PlacementApplication.objects.create(
        #     id=generateRandomString(),
        #     placement=self.placement1,
        #     student=self.student,
        #     resume="8BSLybntULgrPPm_beehyv.pdf",
        #    # selected=True
        #    # status="Applied"
        # )
        self.assertEqual(self.placement_application.placement.company_name, PlacementApplication.objects.get(id=self.placement_application.id).placement.company_name)
        self.issue = Issues.objects.create(
            student=self.student,
            title="Test Issue",
            description="Test Issue Description",
            opening_id=self.internship.id,
            opening_type=INTERNSHIP
        )
        #get token from google OAuth API
        response=self.client.post(reverse('Refresh Token'), {'refresh_token': os.environ.get("refresh_token")}, format='json')
        self.student_token=response.data['id_token']
       # self.student_token = get_access_token_id(os.environ.get("refresh_token"))

        #self.contributor_token = get_token(self.contributor.email, "testpassword", CONTRIBUTOR)
    
    def test_student_accept_offer_internship(self):
        url = reverse('Student Accept Offer')
        data={
            'opening_id':self.internship.id,
            'offer_accepted':True,
            'opening_type':INTERNSHIP
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Updated Offer Status')
        self.assertEqual(InternshipApplication.objects.get(id=self.internship_application.id).offer_accepted, True)
        self.internship_application.selected=False
        self.internship_application.offer_accepted=False
        self.internship_application.save()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Offer Not Found')
        self.assertEqual(InternshipApplication.objects.get(id=self.internship_application.id).offer_accepted, False)
        

    def test_delete_application_internship(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.internship_application.id,
            'opening_type': INTERNSHIP
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Deleted')
        self.assertEqual(InternshipApplication.objects.filter(id=self.internship_application.id).count(), 0)
        self.internship.deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.internship.save()
        self.internship_application=InternshipApplication.objects.create(id=generateRandomString(),
            internship=self.internship,
            student=self.student,
            resume="8BSLybntULgrPPm_beehyv.pdf",
            selected=True)
        data['application_id']=self.internship_application.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Deadline Passed')
        self.assertEqual(InternshipApplication.objects.filter(id=self.internship_application.id).count(), 1)
        

    def test_add_application_internship(self):
        url = reverse('Delete Application')
        data = {
            'application_id': self.internship_application.id,
            'opening_type': INTERNSHIP
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Deleted')
        self.assertEqual(InternshipApplication.objects.filter(id=self.internship_application.id).count(), 0)
        #deleted existing application
        url = reverse('Add Application')
        data = {
            OPENING_ID: self.internship.id,
            OPENING_TYPE: INTERNSHIP,
            RESUME_FILE_NAME: '8BSLybntULgrPPm_beehyv.pdf'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application Submitted')
        self.assertEqual(InternshipApplication.objects.filter(student=self.student).count(), 1)
        self.internship_application=InternshipApplication.objects.filter(student=self.student)
        self.internship.deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.internship.save()
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],'Application is already Submitted')
        self.assertEqual(InternshipApplication.objects.filter(student=self.student).count(), 1)
        self.internship_application.delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],'No Internship matches the given query.')
        self.assertEqual(InternshipApplication.objects.filter(student=self.student).count(), 0)
        

    def test_student_accept_offer_placement(self):
        url=reverse('Student Accept Offer')
        data={
            'opening_id':self.placement.id,
            'offer_accepted':True,
            'opening_type':PLACEMENT
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Updated Offer Status')
        self.assertEqual(PlacementApplication.objects.get(id=self.placement_application.id).offer_accepted,True)
        self.placement_application.selected=False
        self.placement_application.offer_accepted=False
        self.placement_application.save()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Offer Not Found')
        self.assertEqual(PlacementApplication.objects.get(id=self.placement_application.id).offer_accepted, False)
        
    def test_delete_application_placement(self):
        url=reverse('Delete Application')
        data={
            'application_id':self.placement_application.id,
            'opening_type':PLACEMENT
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Application Deleted')
        self.assertEqual(PlacementApplication.objects.filter(id=self.placement_application.id).count(),0)
        self.placement.deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.placement.save()
        self.placement_application=PlacementApplication.objects.create(id=generateRandomString(),
            placement=self.placement,
            student=self.student,
            resume="8BSLybntULgrPPm_beehyv.pdf",
            selected=True)
        data['application_id']=self.placement_application.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Deadline Passed')
        self.assertEqual(PlacementApplication.objects.filter(id=self.placement_application.id).count(), 1)
    def test_add_application_placement(self):
        url=reverse('Delete Application')
        data={
            'application_id':self.placement_application.id,
            'opening_type':PLACEMENT
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Application Deleted')
        self.assertEqual(PlacementApplication.objects.filter(id=self.placement_application.id).count(),0)
        #deleted existing application
        url=reverse('Add Application')
        data={
            OPENING_ID:self.placement.id,
            OPENING_TYPE:PLACEMENT,
            RESUME_FILE_NAME:'8BSLybntULgrPPm_beehyv.pdf'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Application Submitted')
        self.assertEqual(PlacementApplication.objects.filter(student=self.student).count(),1)
        self.placement.deadline_datetime=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.placement.save()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Application is already Submitted')
        self.assertEqual(PlacementApplication.objects.filter(student=self.student).count(), 1)
        self.placement_application=PlacementApplication.objects.filter(student=self.student)
        self.placement_application.delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'No Placement matches the given query.')
        self.assertEqual(PlacementApplication.objects.filter(student=self.student).count(), 0)



    def test_dashboard(self):
        url=reverse('Dashboard')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response=self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Data Found')
        internships=Internship.objects.filter(allowed_batch__contains=[self.student.batch],
                                              allowed_branch__contains=[self.student.branch],
                                              deadline_datetime__gte=datetime.datetime.now(),
                                              offer_accepted=True, email_verified=True)
        placements=Placement.objects.filter(allowed_batch__contains=[self.student.batch],
                                                allowed_branch__contains=[self.student.branch],
                                                deadline_datetime__gte=datetime.datetime.now(),
                                                offer_accepted=True, email_verified=True)
      #  self.assertEqual(len(response.data['internships']),len(internships))
      #  self.assertEqual(PlacementApplicationConditions(self.student,self.placement)[1],"hai")
      #  self.assertEqual(len(response.data['placements']),len(placements))
        filtered_internships=internship_eligibility_filters(self.student,internships)
        filtered_placements=placement_eligibility_filters(self.student,placements)
        self.assertEqual(len(response.data['internships']),len(filtered_internships))
        self.assertEqual(len(response.data['placements']),len(filtered_placements))
        self.assertEqual(len(response.data['placementApplication']),1)
        self.assertEqual(len(response.data['internshipApplication']),1)
        self.assertEqual(response.data['placementApplication'][0]['placement']['company_name'],self.placement.company_name)
        self.assertEqual(response.data['internshipApplication'][0]['internship']['company_name'],self.internship.company_name)









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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.student_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Issue Added')
        self.assertEqual(Issues.objects.filter(student=self.student).count(), 2)
        self.assertEqual(Issues.objects.filter(opening_id=self.placement.id).count(), 1)
        self.assertEqual(Issues.objects.filter(opening_type=PLACEMENT).count(), 1)
    