from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        # exclude = ['id']


class PlacementSerializer(serializers.ModelSerializer):
    company_details = serializers.SerializerMethodField()

    def get_company_details(self, obj):
        data = {
            "id": obj.company.id,
            "name": obj.company.name,
            "address": obj.company.address,
            "companyType": obj.company.companyType,
            "website": obj.company.website,
        }
        return data


    class Meta:
        model = Placement
        exclude=[COMPANY]
        depth = 1


class PlacementApplicationSerializer(serializers.ModelSerializer):
    application_status = serializers.SerializerMethodField()
    company_details = serializers.SerializerMethodField()


    def get_application_status(self, obj):
        if obj.status is None:
            return obj.placement.status
        else:
            return obj.status


    def get_company_details(self, obj):
        data = {
            "id": obj.placement.company.id,
            "name": obj.placement.company.name,
            "address": obj.placement.company.address,
            "companyType": obj.placement.company.companyType,
            "website": obj.placement.company.website,
        }
        return data

    class Meta:
        model = PlacementApplication
        exclude = ['status', 'student']
