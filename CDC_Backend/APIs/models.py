from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from .constants import *


# from .utils import *


class User(models.Model):
    email = models.CharField(primary_key=True, blank=False, max_length=50)
    id = models.CharField(blank=False, max_length=25)
    user_type = ArrayField(models.CharField(blank=False, max_length=10), size=4, default=list, blank=False)
    last_login_time = models.DateTimeField(default=timezone.now)


class Student(models.Model):
    id = models.CharField(blank=False, max_length=15, primary_key=True)
    roll_no = models.IntegerField(blank=False)
    name = models.CharField(blank=False, max_length=50)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES, blank=False)
    branch = models.CharField(choices=BRANCH_CHOICES, blank=False, max_length=10)
    phone_number = models.PositiveBigIntegerField(blank=True, default=None, null=True)
    resumes = ArrayField(models.CharField(null=True, default=None, max_length=100), size=10, default=list, blank=True)
    cpi = models.DecimalField(decimal_places=2, max_digits=4)
    can_apply = models.BooleanField(default=True, verbose_name='Registered')

    def __str__(self):
        return str(self.roll_no)


class Admin(models.Model):
    id = models.CharField(blank=False, max_length=15, primary_key=True)
    name = models.CharField(blank=False, max_length=50)


def two_day_after_today():
    return timezone.now() + timezone.timedelta(days=2)


class Placement(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15)
    # Company Details
    company_name = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=500)
    company_type = models.CharField(blank=False, max_length=50)
    nature_of_business = models.CharField(blank=False, max_length=50, default="")
    website = models.CharField(blank=True, max_length=50)
    company_details = models.CharField(max_length=500, default=None, null=True)
    company_details_pdf_names = ArrayField(models.CharField(null=True, default=None, max_length=100), size=5,
                                           default=list, blank=True)
    is_company_details_pdf = models.BooleanField(blank=False, default=False)
    contact_person_name = models.CharField(blank=False, max_length=50)
    phone_number = models.PositiveBigIntegerField(blank=False)
    email = models.CharField(blank=False, max_length=50, default="")
    city = models.CharField(blank=False, max_length=100, default="")
    state = models.CharField(blank=False, max_length=100, default="")
    country = models.CharField(blank=False, max_length=100, default="")
    pin_code = models.IntegerField(blank=False, default=None, null=True)
    city_type = models.CharField(blank=False, max_length=15, choices=OFFER_CITY_TYPE)
    # Job Details
    designation = models.CharField(blank=False, max_length=50, default=None, null=True)
    description = models.CharField(blank=False, max_length=500, default=None, null=True)
    description_pdf_names = ArrayField(models.CharField(null=True, default=None, max_length=100), size=5, default=list,
                                       blank=True)
    is_description_pdf = models.BooleanField(blank=False, default=False)
    compensation_CTC = models.IntegerField(blank=False, default=None, null=True)  # Job - Per Year
    compensation_gross = models.IntegerField(blank=False, default=None, null=True)
    compensation_take_home = models.IntegerField(blank=False, default=None, null=True)
    compensation_bonus = models.IntegerField(blank=True, default=None, null=True)
    compensation_details = models.CharField(blank=True, max_length=500, default=None, null=True)
    compensation_details_pdf_names = ArrayField(models.CharField(null=True, default=None, max_length=100), size=5,
                                                default=list, blank=True)
    is_compensation_details_pdf = models.BooleanField(blank=False, default=False)
    bond_details = models.CharField(blank=True, max_length=500)
    selection_procedure_rounds = ArrayField(models.CharField(null=True, default=None, max_length=100), size=10,
                                            default=list, blank=True)
    selection_procedure_details = models.CharField(blank=True, max_length=500)
    selection_procedure_details_pdf_names = ArrayField(models.CharField(null=True, default=None, max_length=100),
                                                       size=5, default=list, blank=True)
    is_selection_procedure_details_pdf = models.BooleanField(blank=False, default=False)
    tier = models.CharField(blank=False, choices=TIERS, max_length=10, default=None, null=True)
    tentative_date_of_joining = models.DateField(blank=False, verbose_name="Tentative Date", default=timezone.now)
    allowed_batch = ArrayField(
        models.CharField(max_length=10, choices=BATCH_CHOICES),
        size=TOTAL_BATCHES,
        default=list
    )

    allowed_branch = ArrayField(
        models.CharField(choices=BRANCH_CHOICES, blank=False, max_length=10),
        size=TOTAL_BRANCHES,
        default=list
    )
    tentative_no_of_offers = models.IntegerField(blank=False, default=None, null=True)
    other_requirements = models.CharField(blank=True, max_length=200, default="")
    additional_info = ArrayField(models.CharField(blank=True, max_length=200), size=15, default=list, blank=True)
    email_verified = models.BooleanField(blank=False, default=False)
    offer_accepted = models.BooleanField(blank=False, default=None, null=True)
    deadline_datetime = models.DateTimeField(blank=False, verbose_name="Deadline Date", default=two_day_after_today)
    created_at = models.DateTimeField(blank=False, default=None, null=True)

    def save(self, *args, **kwargs):
        ''' On save, add timestamps '''
        if not self.created_at:
            self.created_at = timezone.now()

        return super(Placement, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name + " - " + self.id


class PlacementApplication(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15)
    placement = models.ForeignKey(Placement, blank=False, on_delete=models.RESTRICT, default=None, null=True)
    student = models.ForeignKey(Student, blank=False, on_delete=models.CASCADE)
    resume = models.CharField(max_length=100, blank=False, null=True, default=None)
    additional_info = models.JSONField(blank=True, null=True, default=None)
    selected = models.BooleanField(null=True, default=None, blank=True)
    applied_at = models.DateTimeField(blank=False, default=None, null=True)
    updated_at = models.DateTimeField(blank=False, default=None, null=True)

    def save(self, *args, **kwargs):
        ''' On save, add timestamps '''
        if not self.applied_at:
            self.applied_at = timezone.now()
        self.updated_at = timezone.now()

        return super(PlacementApplication, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Placement Applications"
        unique_together = ('placement_id', 'student_id')

    def __str__(self):
        return self.placement.company_name + " - " + self.student.name


class PrePlacementOffer(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    company = models.CharField(max_length=50, blank=False, default="", verbose_name="Company Name")
    compensation = models.IntegerField(blank=False)  # Job - Per Year
    compensation_details = models.CharField(blank=True, max_length=200)
    tier = models.CharField(blank=False, choices=TIERS, max_length=10)
    designation = models.CharField(blank=False, max_length=25, default=None, null=True)
    accepted = models.BooleanField(default=None, null=True)
