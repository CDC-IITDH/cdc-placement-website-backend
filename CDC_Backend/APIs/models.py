from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from .constants import *


# from .utils import *


class User(models.Model):
    email = models.EmailField(primary_key=True, blank=False, max_length=JNF_TEXT_MAX_CHARACTER_COUNT)
    id = models.CharField(blank=False, max_length=25)
    user_type = ArrayField(models.CharField(blank=False, max_length=10), size=4, default=list, blank=False)
    last_login_time = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "User"
        unique_together = ('email', 'id')


class Student(models.Model):
    id = models.CharField(blank=False, max_length=15, primary_key=True)
    roll_no = models.IntegerField(blank=False)
    name = models.CharField(blank=False, max_length=JNF_TEXT_MAX_CHARACTER_COUNT)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES, blank=False)
    branch = models.CharField(choices=BRANCH_CHOICES, blank=False, max_length=10)
    phone_number = models.PositiveBigIntegerField(blank=True, default=None, null=True)
    resumes = ArrayField(models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT), size=10,
                         default=list, blank=True)
    cpi = models.DecimalField(decimal_places=2, max_digits=4)
    can_apply = models.BooleanField(default=True, verbose_name='Registered')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.roll_no)


class Admin(models.Model):
    id = models.CharField(blank=False, max_length=15, primary_key=True)
    name = models.CharField(blank=False, max_length=JNF_TEXT_MAX_CHARACTER_COUNT)
    history = HistoricalRecords()


def two_day_after_today():
    return timezone.now() + timezone.timedelta(days=2)


class Placement(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15)
    # Company Details
    company_name = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT)
    address = models.CharField(blank=False, max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT)
    company_type = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT)
    nature_of_business = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    type_of_organisation = models.CharField(max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="", blank=False)
    website = models.CharField(blank=True, max_length=JNF_TEXT_MAX_CHARACTER_COUNT)
    company_details = models.CharField(max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True)
    company_details_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT), size=5,
        default=list, blank=True)
    is_company_details_pdf = models.BooleanField(blank=False, default=False)
    contact_person_name = models.CharField(blank=False, max_length=JNF_TEXT_MAX_CHARACTER_COUNT)
    phone_number = models.PositiveBigIntegerField(blank=False)
    email = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    city = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    state = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    country = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    pin_code = models.IntegerField(blank=False, default=None, null=True)
    city_type = models.CharField(blank=False, max_length=15, choices=OFFER_CITY_TYPE)
    # Job Details
    designation = models.CharField(blank=False, max_length=JNF_TEXT_MAX_CHARACTER_COUNT, default=None, null=True)
    description = models.CharField(blank=False, max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True)
    job_location = models.CharField(blank=False, max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    description_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT), size=5, default=list,
        blank=True)
    is_description_pdf = models.BooleanField(blank=False, default=False)
    compensation_CTC = models.IntegerField(blank=False, default=None, null=True)  # Job - Per Year
    compensation_gross = models.IntegerField(blank=False, default=None, null=True)
    compensation_take_home = models.IntegerField(blank=False, default=None, null=True)
    compensation_bonus = models.IntegerField(blank=True, default=None, null=True)
    compensation_details_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT), size=5,
        default=list, blank=True)
    is_compensation_details_pdf = models.BooleanField(blank=False, default=False)
    bond_details = models.CharField(blank=True, max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT)
    selection_procedure_rounds = ArrayField(
        models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT), size=10,
        default=list, blank=True)
    selection_procedure_details = models.CharField(blank=True, max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT)
    selection_procedure_details_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=JNF_TEXT_MAX_CHARACTER_COUNT),
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
    rs_eligible = models.BooleanField(blank=False, default=False)
    other_requirements = models.CharField(blank=True, max_length=JNF_TEXTAREA_MAX_CHARACTER_COUNT, default="")
    additional_info = ArrayField(models.CharField(blank=True, max_length=JNF_TEXTMEDIUM_MAX_CHARACTER_COUNT), size=15,
                                 default=list, blank=True)
    email_verified = models.BooleanField(blank=False, default=False)
    offer_accepted = models.BooleanField(blank=False, default=None, null=True)
    deadline_datetime = models.DateTimeField(blank=False, verbose_name="Deadline Date", default=two_day_after_today)
    created_at = models.DateTimeField(blank=False, default=None, null=True)
    updated_at = models.DateTimeField(blank=False, default=None, null=True)
    history = HistoricalRecords()

    def format(self):
        if self.company_name is not None:
            self.company_name = self.company_name.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.company_type is not None:
            self.company_type = self.company_type.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.company_details is not None:
            self.company_details = self.company_details.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.address is not None:
            self.address = self.address.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.nature_of_business is not None:
            self.nature_of_business = self.nature_of_business.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.type_of_organisation is not None:
            self.type_of_organisation = self.type_of_organisation.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.website is not None:
            self.website = self.website.strip()[:JNF_TEXT_MAX_CHARACTER_COUNT]
        if self.contact_person_name is not None:
            self.contact_person_name = self.contact_person_name.strip()[:JNF_TEXT_MAX_CHARACTER_COUNT]
        if self.email is not None:
            self.email = self.email.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.city is not None:
            self.city = self.city.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.state is not None:
            self.state = self.state.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.country is not None:
            self.country = self.country.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.city_type is not None:
            self.city_type = self.city_type.strip()[:JNF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.designation is not None:
            self.designation = self.designation.strip()[:JNF_TEXT_MAX_CHARACTER_COUNT]
        if self.description is not None:
            self.description = self.description.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.job_location is not None:
            self.job_location = self.job_location.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.selection_procedure_details is not None:
            self.selection_procedure_details = self.selection_procedure_details.strip()[
                                               :JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.bond_details is not None:
            self.bond_details = self.bond_details.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.other_requirements is not None:
            self.other_requirements = self.other_requirements.strip()[:JNF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.additional_info is not None:
            self.additional_info = [info.strip()[:JNF_TEXTMEDIUM_MAX_CHARACTER_COUNT] for info in list(self.additional_info)]

    def save(self, *args, **kwargs):
        ''' On save, add timestamps '''
        if not self.created_at:
            self.created_at = timezone.now()
        self.format()
        self.updated_at = timezone.now()
        return super(Placement, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name + " - " + self.id


class PlacementApplication(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15)
    placement = models.ForeignKey(Placement, blank=False, on_delete=models.RESTRICT, default=None, null=True)
    student = models.ForeignKey(Student, blank=False, on_delete=models.CASCADE)
    resume = models.CharField(max_length=JNF_TEXT_MAX_CHARACTER_COUNT, blank=False, null=True, default=None)
    additional_info = models.JSONField(blank=True, null=True, default=None)
    selected = models.BooleanField(null=True, default=None, blank=True)
    applied_at = models.DateTimeField(blank=False, default=None, null=True)
    updated_at = models.DateTimeField(blank=False, default=None, null=True)
    history = HistoricalRecords()

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
    company = models.CharField(max_length=JNF_SMALLTEXT_MAX_CHARACTER_COUNT, blank=False, default="",
                               verbose_name="Company Name")
    compensation = models.IntegerField(blank=False)  # Job - Per Year
    compensation_details = models.CharField(blank=True, max_length=200)
    tier = models.CharField(blank=False, choices=TIERS, max_length=10)
    designation = models.CharField(blank=False, max_length=25, default=None, null=True)
    accepted = models.BooleanField(default=None, null=True)
    history = HistoricalRecords()
