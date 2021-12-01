import logging
import os
import random
import string
import sys
from os import path, remove

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.response import Response
import background_task

from .models import *

logger = logging.getLogger('db')


def precheck(required_data=None):
    if required_data is None:
        required_data = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                request_data = None
                if request.method == 'GET':
                    request_data = request.GET
                elif request.method == 'POST':
                    request_data = request.data
                    if not len(request_data):
                        request_data = request.POST
                print(request_data)
                if len(request_data):
                    for i in required_data:
                        if i not in request_data:
                            return Response({'action': "Pre check", 'message': str(i) + " Not Found"},
                                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'action': "Pre check", 'message': "Message Data not Found"},
                                    status=status.HTTP_400_BAD_REQUEST)

                return view_func(request, *args, **kwargs)
            except:
                return Response({'action': "Pre check", 'message': "Error Occurred " + str(sys.exc_info())},
                                status=status.HTTP_400_BAD_REQUEST)

        return wrapper_func

    return decorator


def isAuthorized(allowed_users=None):
    if allowed_users is None:
        allowed_users = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                headers = request.META
                if 'HTTP_AUTHORIZATION' in headers:
                    token_id = headers['HTTP_AUTHORIZATION'][7:]
                    idinfo = id_token.verify_oauth2_token(token_id, requests.Request(), CLIENT_ID)
                    email = idinfo[EMAIL]
                    print(email)
                    user = get_object_or_404(User, email=email)
                    if user:

                        if len(set(user.user_type).intersection(set(allowed_users))) or allowed_users == '*':
                            return view_func(request, user.id, user.email, user.user_type, *args, **kwargs)
                        else:
                            raise PermissionError("Access Denied. You are not allowed to use this service")
                else:
                    raise PermissionError("Authorization Header Not Found")

            except PermissionError as e:
                print(e)
                return Response({'action': "Is Authorized?", 'message': str(e)},
                                status=status.HTTP_401_UNAUTHORIZED)
            except Http404:
                print('http404')
                return Response({'action': "Is Authorized?", 'message': "User Not Found. Contact CDC for more details"},
                                status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                logger.warning("Problem with Google Oauth2.0 " + str(e))
                return Response({'action': "Is Authorized?", 'message': str(e)},
                                status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({'action': "Is Authorized?", 'message': "Error Occurred {0}".format(
                    str(sys.exc_info()[1]))},
                                status=status.HTTP_400_BAD_REQUEST)

        return wrapper_func

    return decorator


def generateRandomString():
    try:
        N = 15
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        return res
    except:
        return False


def saveFile(file, location):
    prefix = generateRandomString()
    file_name = prefix + "_" + file.name

    if not path.isdir(location):
        os.mkdir(location)

    destination_path = location + str(file_name)
    if path.exists(destination_path):
        remove(destination_path)

    with open(destination_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_name

@background_task.background(schedule=60)
def sendEmail(email_to, subject, data, template):
    try:
        html_content = render_to_string(template, data)  # render with dynamic value
        text_content = strip_tags(html_content)

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [str(email_to), ]

        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        logger.error("Send Email: " + str(sys.exc_info()))
        print(str(sys.exc_info()[1]))
        return False


def PlacementApplicationConditions(student, placement):
    try:
        selected_companies = PlacementApplication.objects.filter(student=student, selected=True)
        selected_companies_PSU = [i for i in selected_companies if i.placement.tier == 'psu']
        PPO = PrePlacementOffer.objects.filter(internship_application__student=student, accepted=True)

        if len(selected_companies) + len(PPO) >= 2:
            raise PermissionError("Max Applications Reached for the Season")

        if len(selected_companies_PSU) > 0:
            raise PermissionError('Selected for PSU Can\'t apply anymore')

        if placement.tier == 'psu':
            return True, "Conditions Satisfied"

        for i in selected_companies:
            print(int(i.placement.tier) < int(placement.tier), int(i.placement.tier), int(placement.tier))
            if int(i.placement.tier) < int(placement.tier):
                return False, "Can't apply for this tier"

        return True, "Conditions Satisfied"

    except PermissionError as e:
        return False, e
    except:
        print(sys.exc_info())
        logger.warning("Utils - PlacementApplicationConditions: " + str(sys.exc_info()))
        return False, "_"

def getTier(compensation_gross, is_psu=False):
    try:
        if is_psu:
            return True, 'psu'
        if compensation_gross < 0:
            raise ValueError("Negative Compensation")
        elif compensation_gross < 600000:     # Tier 7 If less than 600,000
            return True, "7"
        # Tier 6 If less than 800,000 and greater than or equal to 600,000
        elif compensation_gross < 800000:
            return True, "6"
        # Tier 5 If less than 1,000,000 and greater than or equal to 800,000
        elif compensation_gross < 1000000:
            return True, "5"
        # Tier 4 If less than 1,200,000 and greater than or equal to 1,000,000
        elif compensation_gross < 1200000:
            return True, "4"
        # Tier 3 If less than 1,500,000 and greater than or equal to 1,200,000
        elif compensation_gross < 1500000:
            return True, "3"
        # Tier 2 If less than 1,800,000 and greater than or equal to 1,500,000
        elif compensation_gross < 1800000:
            return True, "2"
        # Tier 1 If greater than or equal to 1,800,000
        elif compensation_gross >= 1800000:
            return True, "1"
        else:
            raise ValueError("Invalid Compensation")

    except ValueError as e:
        logger.warning("Utils - getTier: " + str(sys.exc_info()))
        return False, e
    except:
        print(sys.exc_info())
        logger.warning("Utils - getTier: " + str(sys.exc_info()))
        return False, "_"



def two_day_after_today():
    return timezone.now() + timezone.timedelta(days=2)