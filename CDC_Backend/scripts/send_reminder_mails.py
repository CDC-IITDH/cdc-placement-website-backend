from APIs.models import Placement, Student, PlacementApplication, User
from APIs.utils import sendEmail, PlacementApplicationConditions
from APIs.constants import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
import pytz

REPEAT_AFTER = 10 * 60


def send_reminder_mails():
    placements = Placement.objects.all()
    students = Student.objects.all()

    for placement in placements.iterator():
        print("Processing placement: ", placement)
        # if placement is approved and email is verified
        if not (placement.offer_accepted and placement.email_verified):
            continue

        # if placement is not expired
        if placement.deadline_datetime < timezone.now():
            continue

        # send the reminder mail if the deadline is within 24 hours +- ReapetAfter
        if timezone.now() - timezone.timedelta(
                seconds=REPEAT_AFTER) <= placement.deadline_datetime - timezone.timedelta(days=1) < timezone.now() + \
                timezone.timedelta(seconds=REPEAT_AFTER):
            for student in students:
                try:
                    # if Application not found then send email
                    if not PlacementApplication.objects.filter(placement=placement, student=student).exists():
                        if student.branch in placement.allowed_branch:
                            if student.degree == 'bTech' or placement.rs_eligible is True:
                                if PlacementApplicationConditions(student, placement)[0]:
                                    student_user = get_object_or_404(User, id=student.id)
                                    # change timezone to IST
                                    deadline_datetime = placement.deadline_datetime.astimezone(pytz.timezone('Asia/Kolkata'))
                                    data = {
                                        "company_name": placement.company_name,
                                        "opening_type": 'Placement',
                                        "deadline": deadline_datetime.strftime("%A, %-d %B %Y, %-I:%M %p"),
                                        "link": PLACEMENT_OPENING_URL.format(id=placement.id)
                                    }
                                    print("Sending mail to " + student_user.email, "placement id: ", placement.id)
                                    sendEmail(student_user.email,
                                              REMINDER_STUDENTS_OPENING_TEMPLATE_SUBJECT.format(
                                                  company_name=placement.company_name),
                                              data, REMINDER_STUDENTS_OPENING_TEMPLATE)

                except Exception as e:
                    print(e)
                    continue


def run():
    while True:
        print("Sleeping for", REPEAT_AFTER, "seconds")
        time.sleep(REPEAT_AFTER)
        print("Running send_reminder_mails()")
        send_reminder_mails()

