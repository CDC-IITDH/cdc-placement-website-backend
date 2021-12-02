import urllib

from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    resume_list = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()

    def get_resume_list(self, obj):
        links = []
        for i in obj.resumes:
            ele = {}
            ele['link'] = LINK_TO_STORAGE_RESUME + urllib.parse.quote_plus(obj.id + "/" + i)
            ele['name'] = i
            links.append(ele)
        return links

    def get_offers(self, obj):
        selected_companies = PlacementApplication.objects.filter(student_id=obj.id, selected=True)
        companies = []

        for i in selected_companies:
            ele = {}
            ele['designation'] = i.placement.designation
            ele['company_name'] = i.placement.company_name
            ele['application_id'] = i.id
            companies.append(ele)

        return companies

    class Meta:
        model = Student
        exclude = ['resumes']

class PlacementSerializerForStudent(serializers.ModelSerializer):
    company_details_pdf_links = serializers.SerializerMethodField()
    description_pdf_links = serializers.SerializerMethodField()
    compensation_pdf_links = serializers.SerializerMethodField()
    selection_procedure_details_pdf_links = serializers.SerializerMethodField()


    def get_company_details_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.company_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_description_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.description_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_compensation_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.compensation_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_selection_procedure_details_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.selection_procedure_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links



    class Meta:
        model = Placement
        exclude = [CONTACT_PERSON_NAME, PHONE_NUMBER, EMAIL, COMPANY_DETAILS_PDF_NAMES, DESCRIPTION_PDF_NAMES,
                 COMPENSATION_DETAILS_PDF_NAMES, SELECTION_PROCEDURE_DETAILS_PDF_NAMES, OFFER_ACCEPTED, EMAIL_VERIFIED]
        depth = 1

class PlacementSerializerForAdmin(serializers.ModelSerializer):
    company_details_pdf_links = serializers.SerializerMethodField()
    description_pdf_links = serializers.SerializerMethodField()
    compensation_pdf_links = serializers.SerializerMethodField()
    selection_procedure_details_pdf_links = serializers.SerializerMethodField()


    def get_company_details_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.company_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_description_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.description_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_compensation_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.compensation_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links

    def get_selection_procedure_details_pdf_links(self, obj):
        links =[]
        for pdf_name in obj.selection_procedure_details_pdf_names:
            ele = {}
            link = LINK_TO_STORAGE_COMPANY_ATTACHMENT + urllib.parse.quote_plus(obj.id + "/" + pdf_name)
            ele['link'] = link
            ele['name'] = pdf_name
            links.append(ele)
        return links



    class Meta:
        model = Placement
        exclude = [COMPANY_DETAILS_PDF_NAMES, DESCRIPTION_PDF_NAMES,
                 COMPENSATION_DETAILS_PDF_NAMES, SELECTION_PROCEDURE_DETAILS_PDF_NAMES]
        depth = 1


class PlacementApplicationSerializer(serializers.ModelSerializer):
    placement = serializers.SerializerMethodField()
    resume_link = serializers.SerializerMethodField()

    def get_placement(self, obj):
        data = PlacementSerializerForStudent(obj.placement).data
        return data

    def get_resume_link(self, obj):
        link = LINK_TO_STORAGE_RESUME + urllib.parse.quote_plus(obj.id + "/" + obj.resume)
        return link

    class Meta:
        model = PlacementApplication
        exclude = [STUDENT, 'resume']
