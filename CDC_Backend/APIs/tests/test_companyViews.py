from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..models import *
import json
from ..utils import generateRandomString
import jwt

# initialize the APIClient app
client = APIClient()



class AddNewPlacementTest(APITestCase):
    """ Test module for adding a new placement """

    def setUp(self):
        self.valid_payload = {
            'company_name': 'Test Company 3', 'address': 'Test Address 3', 'company_type': 'Test Company Type 3',
            'nature_of_business': 'Test Nature of Business 3', 'type_of_organisation': 'Test Type of Organisation 3',
            'website': 'Test Website 3', 'company_details': 'Test Company Details 3', 'is_company_details_pdf': True,
            'contact_person_name': 'Test Contact Person Name 3', 'phone_number': 1234567890, 'email': 'test3@test.com',
            'city': 'Test City 3', 'state': 'Test State 3', 'country': 'Test Country 3', 'pin_code': 123456,
            'designation': 'Test Designation 3', 'description': 'Test Description 3', 'job_location': 'Test Job Location 3',
            'is_description_pdf': True, 'compensation_CTC': 300000, 'compensation_gross': 240000,
            'compensation_take_home': 180000, 'compensation_bonus': 60000, 'is_compensation_details_pdf': True,
            'allowed_branch': 'Test Allowed Branch 3', 'rs_eligible': True,
            'selection_procedure_rounds': 'Test Selection Procedure Rounds 3',
            'selection_procedure_details': 'Test Selection Procedure Details 3',
            'is_selection_procedure_details_pdf': True, 'tentative_date_of_joining': '2022-03-01',
            'tentative_no_of_offers': 30, 'other_requirements': 'Test Other Requirements 3'
        }
        self.invalid_payload = {
            'company_name': '', 'address': 'Test Address 4', 'company_type': 'Test Company Type 4',
            'nature_of_business': 'Test Nature of Business 4', 'type_of_organisation': 'Test Type of Organisation 4',
            'website': 'Test Website 4', 'company_details': 'Test Company Details 4', 'is_company_details_pdf': True,
            'contact_person_name': 'Test Contact Person Name 4', 'phone_number': 1234567890, 'email': 'test4@test.com',
            'city': 'Test City 4', 'state': 'Test State 4', 'country': 'Test Country 4', 'pin_code': 123456,
            'designation': 'Test Designation 4', 'description': 'Test Description 4', 'job_location': 'Test Job Location 4',
            'is_description_pdf': True, 'compensation_CTC': 400000, 'compensation_gross': 320000,
            'compensation_take_home': 240000, 'compensation_bonus': 80000, 'is_compensation_details_pdf': True,
            'allowed_branch': 'Test Allowed Branch 4', 'rs_eligible': True,
            'selection_procedure_rounds': 'Test Selection Procedure Rounds 4',
            'selection_procedure_details': 'Test Selection Procedure Details 4',
            'is_selection_procedure_details_pdf': True, 'tentative_date_of_joining': '2022-04-01',
            'tentative_no_of_offers': 40, 'other_requirements': 'Test Other Requirements 4'
        }
        self.placement1 = Placement.objects.create(
            company_name='ABC Corp', compensation_CTC=1000000, tier='1', id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test", phone_number=1234567890, email="test1@test.com", offer_accepted=True)
        self.internship1 = Internship.objects.create(
            company_name='ABC Corp', stipend=100000, id=generateRandomString(), allowed_branch=["CSE", "EE"], allowed_batch=["2020"], contact_person_name="test", phone_number=1234567890, email="test@gmail.com",  offer_accepted=True)
        self.token_placement1=jwt.encode({'opening_id': self.placement1.id,'opening_type':PLACEMENT,'email':"test1@test.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')

    # def test_create_valid_placement(self):
    #     response = client.post(
    #         reverse('addPlacement'),
    #         data=json.dumps(self.valid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_invalid_placement(self):
    #     response = client.post(
    #         reverse('addPlacement'),
    #         data=json.dumps(self.invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_autofill_jnf_success(self):
        response = client.get(
            reverse('Auto FIll JNF'),{"placement_id": self.placement1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Data Found")
        self.assertEqual(response.data["placement_data"]["company_name"], "ABC Corp")
        self.assertEqual(response.data["placement_data"]["compensation_CTC"], 1000000)
        self.assertEqual(response.data["placement_data"]["tier"], "1")
        self.assertEqual(response.data["placement_data"]["allowed_branch"], ["CSE", "EE"])
        self.assertEqual(response.data["placement_data"]["allowed_batch"], ["2020"])
        self.assertEqual(response.data["placement_data"]["contact_person_name"], "test")
        self.assertEqual(response.data["placement_data"]["phone_number"], 1234567890)
        self.assertEqual(response.data["placement_data"]["email"], "test1@test.com")
    
    def test_autofill_jnf_WithInvalidId(self):
        response = client.get(
            reverse('Auto FIll JNF'),{"placement_id": generateRandomString()}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Placement Not Found")

    def test_autofill_inf_success(self):
        response = client.get(
            reverse('Auto FIll INF'),{"internship_id": self.internship1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Data Found")
        self.assertEqual(response.data["internship_data"]["company_name"], "ABC Corp")
        self.assertEqual(response.data["internship_data"]["stipend"], 100000)
        self.assertEqual(response.data["internship_data"]["allowed_branch"], ["CSE", "EE"])
        self.assertEqual(response.data["internship_data"]["allowed_batch"], ["2020"])
        self.assertEqual(response.data["internship_data"]["contact_person_name"], "test")
        self.assertEqual(response.data["internship_data"]["phone_number"], 1234567890)
        self.assertEqual(response.data["internship_data"]["email"], "test@gmail.com")

    def test_autofill_inf_WithInvalidId(self):
        response = client.get(
            reverse('Auto FIll INF'),{"internship_id": generateRandomString()}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Internship Not Found")

    def test_verify_email_success_placement(self):
        response = client.post(
            reverse('Verify Email'),{"token": self.token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Email Verified Successfully")
    


    def test_verify_email_WithInvalidEmail_placement(self):
        token_placement1=jwt.encode({'opening_id': self.placement1.id,'opening_type':PLACEMENT,'email':"hai@hai.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid Email")
    


    def test_verify_email_WithInvalidOpeningId_Placement(self):
        token_placement1=jwt.encode({'opening_id': generateRandomString(),'opening_type':PLACEMENT,'email':"hai@hai.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Opening Not Found")

    def test_verify_email_WithInvalidOpeningType(self): 
        token_placement1=jwt.encode({'opening_id': self.placement1.id,'opening_type':"hai",'email':"hai@hai.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid opening type")
    def test_verify_email_WithInvalidToken(self):
        response = client.post(
            reverse('Verify Email'),{"token": generateRandomString()}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Something went wrong")
    def test_verify_email_success_Internship(self):
        token_placement1=jwt.encode({'opening_id': self.internship1.id,'opening_type':INTERNSHIP,'email':"test@gmail.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Email Verified Successfully")
    
    def test_verify_email_WithInvalidEmail_Internship(self):
        token_placement1=jwt.encode({'opening_id': self.internship1.id,'opening_type':INTERNSHIP,'email':"hai@hai.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid Email")

    def test_verify_email_WithInvalidOpeningId_Internship(self):
        token_placement1=jwt.encode({'opening_id': generateRandomString(),'opening_type':INTERNSHIP,'email':"hai@hai.com"}, os.environ.get("EMAIL_VERIFICATION_SECRET_KEY"), algorithm='HS256')
        response = client.post(
            reverse('Verify Email'),{"token": token_placement1}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Opening Not Found")



################################################################
#   1.Write Tests For AddPlacement Functions All cases         #
#                                                              #
#    2.Write Tests For AddInternship Function All cases        #                                                  
#                                                              #
################################################################
    def test_addPlacement_sucess(self):
        self.assertTrue(True)

    def test_addPlacement_failure(self):
        self.assertTrue(True)




    
