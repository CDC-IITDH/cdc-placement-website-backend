from django.shortcuts import render,redirect
from .models import PlacementApplication
from django.http import HttpResponse
from .utils import *

import csv

@api_view(['POST'])
@isAuthorized(allowed_users=[ADMIN])
@precheck(required_data=[COL_NAMES, OPENING_ID])
def generateCSV(request, id, email, user_type):
    try:
        data = request.data
        applications=PlacementApplication.objects.filter(placement_id = data[OPENING_ID])
        f = open('../Storage/', 'w')
        writer = csv.writer(f)
        writer.writerow(COL_NAMES)
        for apl in applications:
            row_details=[]
            for col in COL_NAMES:
                if col== ROLL_NO:
                    row_details.append(apl.student.roll_no)
                if col== NAME:
                    row_details.append(apl.student.name)
                if col== BATCH:
                    row_details.append(apl.student.batch)
                if col== BRANCH:
                    row_details.append(apl.student.branch)
                if col== PHONE_NUMBER:
                    row_details.append(apl.student.phone_number)
                if col== CPI:
                    row_details.append(apl.student.cpi)
                if col== RESUME:
                    row_details.append(apl.student.resume)
            writer.writerow(apl)
    except:
        logger.warning("Delete Resume: " + str(sys.exc_info()))
        return Response({'action': "Delete Resume", 'message': "Error Occurred {0}".format(
            str(sys.exc_info()))},
                        status=status.HTTP_400_BAD_REQUEST)
