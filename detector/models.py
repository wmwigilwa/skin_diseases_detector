from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
import pycountry

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def get_country_name(self):
        try:
            country_obj = pycountry.countries.get(alpha_2=self.country)
            return country_obj.name
        except:
            return ''
        
    def __str__(self):
        return self.phone_number
    
#Diseases table
class Disease(models.Model):
    disease_name = models.CharField(max_length=100, blank=True)
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    
    def __str__(self):
        return self.disease_name
    

