from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from ..models import *
from ..serializers import *
from ..utils import *
import json
import os
from rest_framework.test import APITestCase, APIClient


class AdminView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create(email=str(os.environ.get(
            "email")), id=generateRandomString(), user_type=[ADMIN])
        self.s_admin = User.objects.create(email=str(os.environ.get(
            "s_email")), id=generateRandomString(), user_type=["s_admin"])
        self.user1 = User.objects.create(
            email="200010032@iitdh.ac.in", id="200010032", user_type=[STUDENT])
        self.user2 = User.objects.create(
            email="200010038@iitdh.ac.in", id="200010038", user_type=[STUDENT])
        self.user3 = User.objects.create(
            email="200010054@iitdh.ac.in", id="200010054", user_type=[STUDENT])
        self.user4 = User.objects.create(
            email="200030058@iitdh.ac.in", id="200030058", user_type=[STUDENT])
        self.student1 = Student.objects.create(
            name='John Doe', roll_no='200010032', batch='2020', branch='CSE', cpi=9.5, id="200010032", can_apply=True, resumes=["8BSLybntULgrPPm_beehyv.pdf", "8BSLybntULgrPPm_kalera.pdf"], can_apply_internship=True)
        self.student2 = Student.objects.create(
            name='Jane Doe', roll_no='200010038', batch='2020', branch='EE', cpi=9.0, id="200010038", can_apply=True, resumes=["8BSLybntULgrPPm_beehyv.pdf"], can_apply_internship=True)
        self.student3 = Student.objects.create(
            name='Bob Smith', roll_no='200010054', batch='2020', branch='CSE', cpi=8.5, id="200010054", can_apply=True, resumes=["8BSLybntULgrPPm_beehyv.pdf"], can_apply_internship=True)
        self.student4 = Student.objects.create(
            name='Bob Marley', roll_no='200030058', batch='2020', branch='CSE', cpi=8.5, id="200030058", can_apply=True, resumes=["8BSLybntULgrPPm_beehyv.pdf"], can_apply_internship=True)

        self.placement1 = Placement.objects.create(
            company_name='ABC Corp', compensation_CTC=1000000, tier='1', id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test", phone_number="1234567890", email="test1@test.com", email_verified=True, offer_accepted=True)
        self.placement2 = Placement.objects.create(
            company_name='XYZ Corp', compensation_CTC=800000, tier='2', id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test1", phone_number="1234567890", email="test2@test.com", email_verified=True, offer_accepted=True)
        self.placement3 = Placement.objects.create(
            company_name='X Corp', compensation_CTC=800000, tier='2', id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test2", phone_number="1234567890", email="test3@test.com", email_verified=True)
        self.internship1 = Internship.objects.create(
            company_name='ABC Corp', stipend=100000, id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test", phone_number="1234567890", email="test@gmail.com", email_verified=True, offer_accepted=True)
        self.internship2 = Internship.objects.create(
            company_name='XYZ Corp', stipend=80000, id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test1", phone_number="1234567890", email="test1@gmail.com", email_verified=True, offer_accepted=True)
        self.internship3 = Internship.objects.create(
            company_name='X Corp', stipend=80000, id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test", phone_number="1234567890", email="test3@gmail.com", email_verified=True)
        self.ppo1 = PrePlacementOffer.objects.create(
            company='DEF Corp',  compensation=900000, tier='1', student=self.student1, designation="SDE")
        self.ppo2 = PrePlacementOffer.objects.create(
            company='GHI Corp', compensation=700000, tier='2', student=self.student3, designation="SDE")

        self.pa1 = PlacementApplication.objects.create(
            id=generateRandomString(),  student=self.student1, placement=self.placement1, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.pa2 = PlacementApplication.objects.create(
            id=generateRandomString(), student=self.student2, placement=self.placement2, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.pa3 = PlacementApplication.objects.create(
            id=generateRandomString(), student=self.student3, placement=self.placement1, resume="8BSLybntULgrPPm_beehyv.pdf")

        self.pa4 = PlacementApplication.objects.create(
            id=generateRandomString(), student=self.student1, placement=self.placement2, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.pa5 = PlacementApplication.objects.create(
            id=generateRandomString(), student=self.student2, placement=self.placement1, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.pa6 = PlacementApplication.objects.create(
            id=generateRandomString(), student=self.student3, placement=self.placement2, resume="8BSLybntULgrPPm_beehyv.pdf")

        self.ia1 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student1, internship=self.internship1, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.ia2 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student2, internship=self.internship2, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.ia3 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student3, internship=self.internship1, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.ia4 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student1, internship=self.internship2, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.ia5 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student2, internship=self.internship1, resume="8BSLybntULgrPPm_beehyv.pdf")
        self.ia6 = InternshipApplication.objects.create(
            id=generateRandomString(), student=self.student3, internship=self.internship2, resume="8BSLybntULgrPPm_beehyv.pdf")

        response = self.client.post(reverse('Refresh Token'), {
                                    'refresh_token': os.environ.get("refresh_token")}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data['id_token']

    # TODO: logic Issue Fix The Above Function
    # def test_get_stats(self):
    #     self.pa1.selected = True
    #     self.pa1.save()
    #     self.pa2.selected = True
    #     self.pa2.save()
    #     self.pa3.selected = True
    #     self.pa3.save()
    #     self.pa4.selected = True
    #     self.pa4.save()
    #     self.pa5.selected = True
    #     self.pa5.save()
    #     self.pa6.selected = True
    #     self.pa6.save()

    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    #     response = self.client.get(reverse('Get Stats'))
    #     stats = response.data['stats']
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(stats), 4)

    #     # Check if the stats are correct for student1

    #     student1_stats = next(
    #         (item for item in stats if item["id"] == self.student1.id), None)
    #     self.assertEqual(student1_stats['name'], self.student1.name)
    #     self.assertEqual(student1_stats['roll_no'], self.student1.roll_no)
    #     self.assertEqual(student1_stats['batch'], self.student1.batch)
    #     self.assertEqual(student1_stats['branch'], self.student1.branch)
    #     self.assertEqual(student1_stats['cpi'], self.student1.cpi)
    #     self.assertEqual(
    #         student1_stats['first_offer'], self.placement1.company_name)
    #     self.assertEqual(
    #         student1_stats['first_offer_tier'], self.placement1.tier)
    #     self.assertEqual(
    #         student1_stats['first_offer_compensation'], self.placement1.compensation_CTC)
    #     self.assertEqual(
    #         student1_stats['second_offer'], self.placement2.company_name)
    #     self.assertEqual(
    #         student1_stats['second_offer_tier'], self.placement2.tier)
    #     self.assertEqual(
    #         student1_stats['second_offer_compensation'], self.placement2.compensation_CTC)

    #     # Check if the stats are correct for student2
    #     student2_stats = next(
    #         (item for item in stats if item["id"] == self.student2.id), None)
    #     self.assertEqual(student2_stats['name'], self.student2.name)
    #     self.assertEqual(student2_stats['roll_no'], self.student2.roll_no)
    #     self.assertEqual(student2_stats['batch'], self.student2.batch)
    #     self.assertEqual(student2_stats['branch'], self.student2.branch)
    #     self.assertEqual(student2_stats['cpi'], self.student2.cpi)
    #     self.assertEqual(
    #         student2_stats['first_offer'], self.placement2.company_name)
    #     self.assertEqual(
    #         student2_stats['first_offer_tier'], self.placement2.tier)
    #     self.assertEqual(
    #         student2_stats['first_offer_compensation'], self.placement2.compensation_CTC)
    #     self.assertEqual(
    #         student2_stats['second_offer'], self.placement1.company_name)
    #     self.assertEqual(
    #         student2_stats['second_offer_tier'], self.placement1.tier)
    #     self.assertEqual(
    #         student2_stats['second_offer_compensation'], self.placement1.compensation_CTC)

    #     # Check if the stats are correct for student3
    #     student3_stats = next(
    #         (item for item in stats if item["id"] == self.student3.id), None)
    #     self.assertEqual(student3_stats['name'], self.student3.name)
    #     self.assertEqual(student3_stats['roll_no'], self.student3.roll_no)
    #     self.assertEqual(student3_stats['batch'], self.student3.batch)
    #     self.assertEqual(student3_stats['branch'], self.student3.branch)
    #     self.assertEqual(student3_stats['cpi'], self.student3.cpi)
    #     self.assertEqual(student3_stats['first_offer'], self.placement1.company_name)
    #     self.assertEqual(student3_stats['first_offer_tier'], self.placement1.tier)
    #     self.assertEqual(
    #         student3_stats['first_offer_compensation'], self.placement1.compensation_CTC)
    #     self.assertEqual(
    #         student3_stats['second_offer'], self.placement2.company_name)
    #     self.assertEqual(
    #         student3_stats['second_offer_tier'], self.placement2.tier)
    #     self.assertEqual(
    #         student3_stats['second_offer_compensation'], self.placement2.compensation_CTC)

    #     # check if the stats are correct for student4
    #     student4_stats = next(
    #         (item for item in stats if item["id"] == self.student4.id), None)
    #     self.assertEqual(student4_stats['name'], self.student4.name)
    #     self.assertEqual(student4_stats['roll_no'], self.student4.roll_no)
    #     self.assertEqual(student4_stats['batch'], self.student4.batch)
    #     self.assertEqual(student4_stats['branch'], self.student4.branch)
    #     self.assertEqual(student4_stats['cpi'], self.student4.cpi)
    #     self.assertEqual(student4_stats['first_offer'], None)
    #     self.assertEqual(student4_stats['first_offer_tier'], None)
    #     self.assertEqual(
    #         student4_stats['first_offer_compensation'], None)
    #     self.assertEqual(
    #         student4_stats['second_offer'], None)
    #     self.assertEqual(
    #         student4_stats['second_offer_tier'], None)
    #     self.assertEqual(
    #         student4_stats['second_offer_compensation'], None)


    def test_addPPO(self):  # done
        url = reverse("Add PPO")
        data = {
            "student_id": self.student2.id,
            "company_name": "ABC Corp",
            "compensation_gross": 1000000,
            "tier": "1",
            "designation": "SDE",
            "offer_accepted": ""
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'PPO added')
        self.assertEqual(PrePlacementOffer.objects.get(
            student=self.student2).company, data['company_name'])
        self.assertEqual(PrePlacementOffer.objects.get(
            student=self.student2).compensation, data['compensation_gross'])
        self.assertEqual(PrePlacementOffer.objects.get(
            student=self.student2).tier, data['tier'])
        self.assertEqual(PrePlacementOffer.objects.get(
            student=self.student2).designation, data['designation'])

    def test_getStudentApplication(self):  # done
        url = reverse("Get student application")
        data = {
            "student_id": self.student1.id,
            "opening_id": self.placement1.id,
            "opening_type": "Placement"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_info']["id"], self.pa1.id)
        self.assertEqual(
            response.data['application_info']["resume"]['link'][-26:], self.pa1.resume)
        self.assertEqual(
            response.data['application_info']["additional_info"], self.pa1.additional_info)
        self.assertEqual(response.data['application_found'], 'true')

    def test_getStudentApplication_notfound(self):
        url = reverse("Get student application")
        data = {
            "student_id": self.student4.id,
            "opening_id": self.placement1.id,
            "opening_type": "Placement"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['application_found'], 'false')
        self.assertEqual(
            response.data["student_details"]["name"], self.student4.name)

    def test_getStudentApplication_wrongStudent(self):
        url = reverse("Get student application")
        data = {
            "student_id": generateRandomString(),
            "opening_id": self.placement1.id,
            "opening_type": "Placement"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], 'Student not found.')

    def test_generateCSV(self):
        url = reverse("Generate CSV")  # done
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
       # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'CSV created')

    def test_submitApplication(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": [],
            "application_id": ""
        }
       # data["opening_id"] = generateRandomString()
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application added')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student4).count(), 1)
        ##############################################
        ### handle double creation of application  ###
        ##############################################
    def test_submitApplication_without_adinfo(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.placement1.additional_info = ["test"]
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": [],
            "application_id": ""
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'test not found in Additional Info')

    def test_submitApplication_with_adinfo(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.placement1.additional_info = ["test"]
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": {"test": "test"},
            "application_id": ""
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application added')
        self.assertEqual(PlacementApplication.objects.filter(
            student=self.student4).count(), 1)
        self.assertEqual(PlacementApplication.objects.get(
            student=self.student4, placement=self.placement1).additional_info, json.dumps(data['additional_info']))

    def test_submitApplication_with_wrong_resume(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv1.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')

    def test_submitApplication_with_wrongOpening(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Placement matches the given query.')

    def test_submitApplication_with_wrongStudent(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": generateRandomString(),
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Student matches the given query.')

    def test_submitApplicatioin_with_application(self):
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": [],
            "application_id": self.pa1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application updated')
        self.assertEqual(PlacementApplication.objects.get(
            student=self.student1, placement=self.placement1).resume, data['resume_file_name'])

    def test_submitApplication_with_application_without_adinfo(self):
        self.placement1.additional_info = ["test"]
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": [],
            "application_id": self.pa1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'test not found in Additional Info')

    def test_submitApplication_with_application_with_adinfo(self):
        self.placement1.additional_info = ["test"]
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": {"test": "test"},
            "application_id": self.pa1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application updated')
        self.assertEqual(PlacementApplication.objects.get(
            student=self.student1, placement=self.placement1).resume, data['resume_file_name'])
        self.assertEqual(PlacementApplication.objects.get(
            student=self.student1, placement=self.placement1).additional_info, json.dumps(data['additional_info']))

    def test_submitApplication_with_application_with_wrong_resume(self):
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera1.pdf",
            "application_id": self.pa1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')

    def test_submitApplication_with_application_with_wrongapplication(self):
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": generateRandomString(),
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No PlacementApplication matches the given query.')

    def test_submitApplication_with_application_with_wrongOpening(self):
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.pa1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Placement matches the given query.')

    def test_submitApplication_with_application_with_wrongStudent(self):
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": generateRandomString(),
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.pa1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Student matches the given query.')

    def test_submitApplication_with_application_without_corresponding_student(self):
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.pa1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')  # this is a malfunctioning test case


# -----------------------------done submit application placement


    def test_getApplications(self):  # done
        url = reverse("Get Applications")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Data Found')
        self.assertEqual(len(response.data['applications']), 3)
        applications_students = []
        applications_students.append(
            response.data['applications'][0]['student_details']["id"])
        applications_students.append(
            response.data['applications'][1]['student_details']["id"])
        applications_students.append(
            response.data['applications'][2]['student_details']["id"])
        self.assertIn(self.student1.id, applications_students)
        self.assertIn(self.student2.id, applications_students)
        self.assertIn(self.student3.id, applications_students)

    def test_getApplications_error(self):
        url = reverse("Get Applications")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString()
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

# done getApplications.........

# # -done
    def test_addAdditionalInfo(self):
        url = reverse("Add Additional Info")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Additional Info Added')
        self.assertIn(data['field'], Placement.objects.get(
            id=self.placement1.id).additional_info)

    def test_addAdditional_info_with_wrongOpening(self):
        url = reverse("Add Additional Info")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_addAdditional_info_existing(self):
        url = reverse("Add Additional Info")
        self.placement1.additional_info = ["Test Field"]
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "field": "Test Field"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'Additional Info already found')
        self.assertIn(data['field'], Placement.objects.get(
            id=self.placement1.id).additional_info)

# done add additional info
    def test_deleteAdditionalInfo(self):
        self.placement1.additional_info = ["Test Field"]
        self.placement1.save()
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Additional Info Deleted')
        self.assertNotIn(data['field'], Placement.objects.get(
            id=self.placement1.id).additional_info)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

    def test_deletetAdditional_info_with_wrongOpening(self):
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_deletetAdditional_info_with_wrongField(self):
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Additional Info not found')


# done delete

    def test_updateEmailVerified(self):  # done
        url = reverse("Update Email Verified")
        self.placement1.email_verified = False
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "email_verified": "true"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email Verified Updated')
        self.assertEqual(Placement.objects.get(
            id=self.placement1.id).email_verified, True)

    def test_updateEmailVerified_WrongOpening(self):
        url = reverse("Update Email Verified")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "email_verified": "true"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

# done update email verified

    def test_updateofferAccepted(self):  # done
        url = reverse("Update Offer Accepted")
        self.placement1.offer_accepted = None
        self.placement1.save()
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "offer_accepted": "true"
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Offer Accepted Updated')
        self.assertEqual(Placement.objects.get(
            id=self.placement1.id).offer_accepted, True)
        self.assertEqual(Placement.objects.get(
            id=self.placement1.id).deadline_datetime, timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=2))

    def test_offerAccepted_withDeadline(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement3.id,
            "offer_accepted": "true",
            "deadline_datetime": (timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Placement.objects.get(
            id=self.placement3.id).deadline_datetime, timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1))
        self.assertEqual(response.data['message'], 'Offer Accepted Updated')

    def test_offerAccepted_wrongOpening(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "offer_accepted": "true",
            "deadline_datetime": (timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_offerAccepted_rejectedOpening(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "offer_accepted": "true"
        }
        self.placement1.offer_accepted = False
        self.placement1.save()
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Offer Status already updated')

    def test_offerAccepted_acceptedOpening(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "offer_accepted": "true"
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Offer Status already updated')
# updated offerAccepted

    def test_updateDeadline(self):  # done
        url = reverse("Update Deadline")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "deadline_datetime": (timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.placement1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Deadline Updated')
        self.assertEqual(Placement.objects.get(
            id=self.placement1.id).deadline_datetime.strftime('%Y-%m-%d %H:%M:%S %z'), data['deadline_datetime'])

    def test_updateDeadline_with_wrongOpening(self):
        url = reverse("Update Deadline")
        data = {
            "opening_type": "Placement",
            "opening_id": generateRandomString(),
            "deadline_datetime": (timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

# updated update deadline

    def test_markStatus(self):  # done
        url = reverse("Mark Status")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_list": [{
                "student_id": self.student1.id,
                "student_selected": True
            }, {
                "student_id": self.student2.id,
                "student_selected": False
            }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Marked Status')
        i = 0
        for student in data['student_list']:
            self.assertEqual(PlacementApplication.objects.get(
                student=student['student_id'], placement=self.placement1).selected, data['student_list'][i]['student_selected'])
            i += 1

    def test_markStatus_Alreadyselected(self):
        url = reverse("Mark Status")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_list": [{
                "student_id": self.student1.id,
                "student_selected": True
            }]

        }
        self.pa1.selected = True
        self.pa1.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], "Student already selected")

    def test_markstatus_notApplied(self):
        url = reverse("Mark Status")
        data = {
            "opening_type": "Placement",
            "opening_id": self.placement1.id,
            "student_list": [{
                "student_id": self.student4.id,
                "student_selected": True
            }]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], "Student - " + str(self.student4.id) + " didn't apply for this opening")

 # done markStatus

    def test_get_dashboard(self):  # working
        url = reverse("Get Dashboard")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.internship2.deadline_datetime = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.internship2.save()
        self.placement2.deadline_datetime = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.placement2.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Data Found')
        self.assertEqual(len(response.data['ongoing']), 1)
        self.assertEqual(response.data['ongoing'][0]['id'], self.placement1.id)
        self.assertEqual(len(response.data['previous']), 1)
        self.assertEqual(response.data['previous']
                         [0]['id'], self.placement2.id)
        self.assertEqual(len(response.data['new']), 1)
        self.assertEqual(response.data['new'][0]['id'], self.placement3.id)
        self.assertEqual(len(response.data['ongoing_internships']), 1)
        self.assertEqual(
            response.data['ongoing_internships'][0]['id'], self.internship1.id)
        self.assertEqual(len(response.data['previous_internships']), 1)
        self.assertEqual(
            response.data['previous_internships'][0]['id'], self.internship2.id)
        self.assertEqual(len(response.data['new_internships']), 1)
        self.assertEqual(
            response.data['new_internships'][0]['id'], self.internship3.id)

#  # -------------------------------------------------checking for internships-------------------

    def test_getStudentApplication_internship(self):  # done
        url = reverse("Get student application")
        data = {
            "student_id": self.student1.id,
            "opening_id": self.internship1.id,
            "opening_type": "Internship"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_found'], 'true')
        self.assertEqual(response.data['application_info']["id"], self.ia1.id)
        self.assertEqual(
            response.data['application_info']["resume"]['link'][-26:], self.ia1.resume)
        self.assertEqual(
            response.data['application_info']["additional_info"], self.ia1.additional_info)

    def test_getStudentApplication_internship_notfound(self):
        url = reverse("Get student application")
        data = {
            "student_id": self.student4.id,
            "opening_id": self.internship1.id,
            "opening_type": "Internship"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['application_found'], 'false')
        self.assertEqual(
            response.data["student_details"]["name"], self.student4.name)

    def test_getStudentApplication_internship_wrongstudent(self):
        url = reverse("Get student application")
        data = {
            "student_id": generateRandomString(),
            "opening_id": self.internship1.id,
            "opening_type": "Internship"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(response.data['application_found'], 'false')
        self.assertEqual(response.data["message"], 'Student not found.')

    def test_generateCSV_internship(self):  # done
        url = reverse("Generate CSV")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getApplications_internship(self):  # done
        url = reverse("Get Applications")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Data Found')
        self.assertEqual(len(response.data['applications']), 3)
        applications_students = []
        applications_students.append(
            response.data['applications'][0]['student_details']["id"])
        applications_students.append(
            response.data['applications'][1]['student_details']["id"])
        applications_students.append(
            response.data['applications'][2]['student_details']["id"])
        self.assertIn(str(self.student1.id), applications_students)
        self.assertIn(str(self.student2.id), applications_students)
        self.assertIn(str(self.student3.id), applications_students)

    def test_getApplications_internship_error(self):
        url = reverse("Get Applications")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString()
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

# # -working
    def test_addAdditionalInfo_internship(self):
        url = reverse("Add Additional Info")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "field": "Test Field",
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Additional Info Added')
        self.assertIn(data['field'], Internship.objects.get(
            id=self.internship1.id).additional_info)

    def test_addAdditionalInfo_internship_existing(self):
        url = reverse("Add Additional Info")
        self.internship1.additional_info = ["Test Field"]
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "field": "Test Field"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'Additional Info already found')
        self.assertIn(data['field'], Internship.objects.get(
            id=self.internship1.id).additional_info)

    def test_addAdditionalInfo_internship_wrongOpening(self):
        url = reverse("Add Additional Info")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "field": "Test Field"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_deleteAdditionalInfo_internship(self):
        self.internship1.additional_info = ["Test Field"]
        self.internship1.save()
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Additional Info Deleted')
        self.assertNotIn(data['field'], Internship.objects.get(
            id=self.internship1.id).additional_info)

    def test_deleteAdditionalInfo_internship_With_wrongOpening(self):
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "field": "Test Field"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_deleteAdditionalInfo_internship_with_wrong_field(self):
        self.internship1.additional_info = ["Test Field"]
        self.internship1.save()
        url = reverse("Delete Additional Info")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "field": "Test Field1"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Additional Info not found')

    def test_updateEmailVerified_internship(self):  # done
        url = reverse("Update Email Verified")
        self.internship1.email_verified = False
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "email_verified": "true"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email Verified Updated')
        self.assertEqual(Internship.objects.get(
            id=self.internship1.id).email_verified, True)

    def test_updateEmailVerified_internship_wrongOpening(self):
        url = reverse("Update Email Verified")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "email_verified": "true"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_updateDeadline_internship(self):  # done
        url = reverse("Update Deadline")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "deadline_datetime": (timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.internship1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Deadline Updated')
        self.assertEqual(Internship.objects.get(
            id=self.internship1.id).deadline_datetime.strftime('%Y-%m-%d %H:%M:%S %z'), data['deadline_datetime'])

    def test_updateDeadline_with_wrongOpening(self):
        url = reverse("Update Deadline")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "deadline_datetime": (timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_updateofferAccepted_internship(self):  # done
        url = reverse("Update Offer Accepted")
        self.internship1.offer_accepted = None
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "offer_accepted": "true"
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Offer Accepted Updated')
        self.assertEqual(Internship.objects.get(
            id=self.internship1.id).offer_accepted, True)
        self.internship1.refresh_from_db()
        self.assertEqual(self.internship1.deadline_datetime, timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=2))

    def test_updateofferAccepted_withDeadline_internship(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship3.id,
            "offer_accepted": "true",
            "deadline_datetime": (timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.internship3.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Internship.objects.get(
            id=self.internship3.id).deadline_datetime, timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1))
        self.assertEqual(response.data['message'], 'Offer Accepted Updated')

    def test_updateofferAccepted_wrongOpening_internship(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "offer_accepted": "true",
            "deadline_datetime": (timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0)+timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S %z')
        }
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Opening Not Found')

    def test_updateofferAccepted_rejectedOpening_internship(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "offer_accepted": "true"
        }
        self.internship1.offer_accepted = False
        self.internship1.save()
        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.internship1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Offer Status already updated')

    def test_updateofferAccepted_acceptedOpening_internship(self):
        url = reverse("Update Offer Accepted")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "offer_accepted": "true"
        }

        self.admin.user_type = ["s_admin"]
        self.admin.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.internship1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Offer Status already updated')

    def test_markStatus_internship(self):  # done
        url = reverse("Mark Status")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_list": [{
                "student_id": self.student1.id,
                "student_selected": True
            }, {
                "student_id": self.student2.id,
                "student_selected": False
            }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Marked Status')
        i = 0
        for student in data['student_list']:
            self.assertEqual(InternshipApplication.objects.get(
                student=student['student_id'], internship=self.internship1).selected, data['student_list'][i]['student_selected'])
            i += 1

    def test_markStatus_Internship_alreadySelected(self):
        url = reverse("Mark Status")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_list": [{
                "student_id": self.student1.id,
                "student_selected": True
            }]
        }
        self.ia1.selected = True
        self.ia1.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], "Student already selected")

    def test_mark_status_Internship_notApplied(self):
        url = reverse("Mark Status")
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_list": [{
                "student_id": self.student4.id,
                "student_selected": True
            }]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], "Student - " + str(self.student4.id) + " didn't apply for this opening")


# # ---------------------------------------------------------------------------


    def test_submitApplication_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": [],
            "application_id": ""
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application added')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student4).count(), 1)

         ##############################################
        ### handle double creation of application  ###
        ##############################################

    def test_submitApplication_without_adinfo_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.internship1.additional_info = ["test"]
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": [],
            "application_id": ""
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'test not found in Additional Info')

    def test_submitApplication_with_adinfo_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.internship1.additional_info = ["test"]
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "additional_info": {"test": "test"},
            "application_id": ""
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application added')
        self.assertEqual(InternshipApplication.objects.filter(
            student=self.student4).count(), 1)
        self.assertEqual(InternshipApplication.objects.get(
            student=self.student4, internship=self.internship1).additional_info, json.dumps(data['additional_info']))

    def test_submitApplication_with_wrong_resume_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv1.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')

    def test_submitApplication_with_wrongOpening_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Internship matches the given query.')

    def test_submitApplication_with_wrongStudent_internship(self):
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": generateRandomString(),
            "resume_file_name": "8BSLybntULgrPPm_beehyv.pdf",
            "application_id": "",
            "additional_info": []
        }
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Student matches the given query.')

    def test_submitApplicatioin_with_application_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": [],
            "application_id": self.ia1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application updated')
        self.assertEqual(InternshipApplication.objects.get(
            student=self.student1, internship=self.internship1).resume, data['resume_file_name'])

    def test_submitApplication_with_application_without_adinfo_internship(self):
        self.internship1.additional_info = ["test"]
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": [],
            "application_id": self.ia1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'test not found in Additional Info')

    def test_submitApplication_with_application_with_adinfo_internship(self):
        self.internship1.additional_info = ["test"]
        self.internship1.save()
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "additional_info": {"test": "test"},
            "application_id": self.ia1.id
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Application updated')
        self.assertEqual(InternshipApplication.objects.get(
            student=self.student1, internship=self.internship1).resume, data['resume_file_name'])
        self.assertEqual(InternshipApplication.objects.get(
            student=self.student1, internship=self.internship1).additional_info, json.dumps(data['additional_info']))

    def test_submitApplication_with_application_with_wrong_resume_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera1.pdf",
            "application_id": self.ia1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')

    def test_submitApplication_with_application_with_wrongapplication_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": generateRandomString(),
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No InternshipApplication matches the given query.')

    def test_submitApplication_with_application_with_wrongOpening_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": generateRandomString(),
            "student_id": self.student1.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.ia1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Internship matches the given query.')

    def test_submitApplication_with_application_with_wrongStudent_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": generateRandomString(),
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.ia1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'No Student matches the given query.')

    def test_submitApplication_with_application_without_corresponding_student_internship(self):
        data = {
            "opening_type": "Internship",
            "opening_id": self.internship1.id,
            "student_id": self.student4.id,
            "resume_file_name": "8BSLybntULgrPPm_kalera.pdf",
            "application_id": self.ia1.id,
            "additional_info": []
        }
        url = reverse("Submit Application")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data=json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'], 'resume_file_name Not Found')  # this is a malfunctioning test case
