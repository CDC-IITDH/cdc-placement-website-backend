from django.db import models

# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from .constants import *

#import models from other apps
from APIs.models import User,Student

# Create your models here.
class Internship(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15) #unique id for each internship
    # Company Details
    company_name = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT)
    address = models.CharField(blank=False, max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT)
    company_type = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT)
    nature_of_business = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    type_of_organisation = models.CharField(max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="", blank=False)
    website = models.CharField(blank=True, max_length=INF_TEXT_MAX_CHARACTER_COUNT)
    company_details = models.CharField(max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True, blank=True)
    company_details_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=INF_TEXT_MAX_CHARACTER_COUNT), size=5,
        default=list, blank=True)
    is_company_details_pdf = models.BooleanField(blank=False, default=False)
    #Company Address
    city = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    state = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    country = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    pin_code = models.IntegerField(blank=False, default=None, null=True)
    # selection process
    selection_procedure_rounds = ArrayField(
        models.CharField(null=True, default=None, max_length=INF_TEXT_MAX_CHARACTER_COUNT), size=10,
        default=list, blank=True)
    selection_procedure_details = models.CharField(blank=True, max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT)
    selection_procedure_details_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=INF_TEXT_MAX_CHARACTER_COUNT),
        size=5, default=list, blank=True)
    is_selection_procedure_details_pdf = models.BooleanField(blank=False, default=False)
    #Internship Details
    description_pdf_names = ArrayField(
        models.CharField(null=True, default=None, max_length=INF_TEXT_MAX_CHARACTER_COUNT), size=5, default=list,
        blank=True)
    is_description_pdf = models.BooleanField(blank=False, default=False)
    description = models.CharField(blank=False, max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True)
    interning_period_from = models.DateField(blank=False, default=None, null=True)
    interning_period_to = models.DateField(blank=False, default=None, null=True)
    season = models.CharField(blank=False, max_length=10, choices=SEASON_CHOICES, default=None)
    is_work_from_home = models.BooleanField(blank=False, default=False)
    sophomore_eligible = models.BooleanField(blank=False, default=False)
    tentative_no_of_offers = models.IntegerField(blank=False, default=None, null=True)
    stipend_description_pdf_names=ArrayField(
        models.CharField(null=True, default=None, max_length=INF_TEXT_MAX_CHARACTER_COUNT), size=5, default=list,
        blank=True)
    is_stipend_description_pdf = models.BooleanField(blank=False, default=False)
    stipend=models.IntegerField(blank=False, default=None, null=True)
    facilities_provided=ArrayField(
        models.CharField(choices=FACILITIES_PROVIDED, blank=False, max_length=20),
        size=TOTAL_FACILITIES,
        default=list
    )
    additional_facilities = models.CharField(blank=True, max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True)
    academic_requirements = models.CharField(blank=True, max_length=INF_TEXTAREA_MAX_CHARACTER_COUNT, default=None, null=True)
    #contact details of company person
    contact_person_name = models.CharField(blank=False, max_length=INF_TEXT_MAX_CHARACTER_COUNT)
    phone_number = models.PositiveBigIntegerField(blank=False)
    email = models.EmailField(blank=False)
    contact_person_designation = models.CharField(blank=False, max_length=INF_SMALLTEXT_MAX_CHARACTER_COUNT, default="")
    telephone_number = models.PositiveBigIntegerField(blank=True, default=None, null=True)
    email_verified = models.BooleanField(blank=False, default=False)
    #history
    created_at = models.DateTimeField(blank=False, default=None, null=True)
    updated_at = models.DateTimeField(blank=False, default=None, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords(user_model=User)

    
    def format(self):
        if self.company_name is not None:
            self.company_name = self.company_name.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.company_type is not None:
            self.company_type = self.company_type.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.company_details is not None:
            self.company_details = self.company_details.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.address is not None:
            self.address = self.address.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.nature_of_business is not None:
            self.nature_of_business = self.nature_of_business.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.type_of_organisation is not None:
            self.type_of_organisation = self.type_of_organisation.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.website is not None:
            self.website = self.website.strip()[:INF_TEXT_MAX_CHARACTER_COUNT]
        if self.contact_person_name is not None:
            self.contact_person_name = self.contact_person_name.strip()[:INF_TEXT_MAX_CHARACTER_COUNT]
        if self.city is not None:
            self.city = self.city.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.state is not None:
            self.state = self.state.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.country is not None:
            self.country = self.country.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.city_type is not None:
            self.city_type = self.city_type.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        if self.selection_procedure_details is not None:
            self.selection_procedure_details = self.selection_procedure_details.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.description is not None:
            self.description = self.description.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.additional_facilities is not None:
            self.additional_facilities = self.additional_facilities.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.academic_requirements is not None:
            self.academic_requirements = self.academic_requirements.strip()[:INF_TEXTAREA_MAX_CHARACTER_COUNT]
        if self.contact_person_designation is not None:
            self.contact_person_designation = self.contact_person_designation.strip()[:INF_SMALLTEXT_MAX_CHARACTER_COUNT]
        
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        if isinstance(value, User):
            self.changed_by = value
        else:
            self.changed_by = None
            
    def save(self, *args, **kwargs):
        ''' On save, add timestamps '''
        if not self.created_at:
            self.created_at = timezone.now()
        self.format()
        self.updated_at = timezone.now()
        return super(Internship, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.company_name + " - " + self.id    
            
    
    
class Season(models.Model):
    
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.season + " Season  - " + self.student.id
    
class InternshipApplication(models.Model):
    id = models.CharField(blank=False, primary_key=True, max_length=15) #unique id for each internship
    internship=models.ForeignKey(Internship,blank=False, on_delete=models.CASCADE, default=None)
    student=models.ForeignKey(Student,blank=False, on_delete=models.CASCADE, default=None)
    resume = models.CharField(max_length=INF_TEXT_MAX_CHARACTER_COUNT, blank=False, null=True, default=None)
    additional_info = models.JSONField(blank=True, null=True, default=None)
    selected = models.BooleanField(null=True, default=None, blank=True)
    offer_accepted = models.BooleanField(null=True, default=None, blank=True) # True if offer accepted, False if rejected, None if not yet decided
    applied_at = models.DateTimeField(blank=False, default=None, null=True)
    updated_at = models.DateTimeField(blank=False, default=None, null=True)
    changed_by = models.ForeignKey(User, blank=False, on_delete=models.RESTRICT, default=None, null=True)
    history = HistoricalRecords(user_model=User)
    
    def save(self, *args, **kwargs):
        ''' On save, add timestamps '''
        if not self.applied_at:
            self.applied_at = timezone.now()
        self.updated_at = timezone.now()
        
        return super(InternshipApplication, self).save(*args, **kwargs)
    
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        if isinstance(value, User):
            self.changed_by = value
        else:
            self.changed_by = None
            
    class Meta:
        verbose_name_plural = "Internship Applications"
        unique_together = ('internship', 'student')
        
    def __str__(self):
        return self.internship.company_name + " - " + self.student.name
    