"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def fields(model):
    return [ f.name for f in model._meta.fields + model._meta.many_to_many ]

class Company(models.Model):
    name=models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='')
    sub_type = models.CharField(max_length=255, default='')
    fte=models.FloatField(default=0)
    rev=models.FloatField(default=0)

class Project(models.Model):
    name = models.CharField(max_length=255, default='')
    desc = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='')
    company = models.ForeignKey(Company)

class Project_User(models.Model):
    user = models.ForeignKey(User)
    project =models.ForeignKey(Project)
    role = models.CharField(max_length=255, default='')

class UploadFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.FileField(upload_to=user_directory_path)

class Transaction(models.Model):
    uid=models.CharField(max_length=255, default='')
    load_date=models.CharField(max_length=255, default='')
    client=models.CharField(max_length=255, default='')
    vendor=models.CharField(max_length=255, default='')
    gl=models.CharField(max_length=255, default='')
    package=models.CharField(max_length=255, default='')
    sub_package=models.CharField(max_length=255, default='')
    spend=models.FloatField(default=0)
    
    def __str__(self):
        return str(self.uid)

class VisiFinancials(models.Model):
    uid = models.CharField(max_length=255, default='', db_index=True)
    project = models.ForeignKey(Project)
    upload = models.CharField(max_length=255, default='')
    gl_name = models.CharField(max_length=255, default='')
    vendor_name = models.CharField(max_length=255, default='')
    po_desc = models.CharField(max_length=255, default='')
    spend = models.FloatField(default=0)

class VisiMappings(models.Model):
    uid = models.CharField(max_length=255, default='', db_index=True)
    pct = models.FloatField(default=0)
    package_first = models.CharField(max_length=255, default='')
    sub_package_first = models.CharField(max_length=255, default='')
    package_second = models.CharField(max_length=255, default='')
    sub_package_second = models.CharField(max_length=255, default='')
    prob_first = models.FloatField(default=0)
    prob_second = models.FloatField(default=0)
    confidence = models.FloatField(default=0)
    index_first = models.FloatField(default=0)
    index_second = models.FloatField(default=0)
    date = models.CharField(max_length=255, default='')
    user = models.ForeignKey(User)
    status = models.CharField(max_length=255, default='')

class CompanyInfo(models.Model):
    company=models.CharField(max_length=255, default='')
    fte=models.FloatField(default=0)
    rev=models.FloatField(default=0)

class CompanyVisi(models.Model):
    company=models.ForeignKey(CompanyInfo)
    package=models.CharField(max_length=255, default='')
    sub_package=models.CharField(max_length=255, default='')
    month=models.FloatField(default=0)
    spend=models.FloatField(default=0)

class BenchmarkVisi(models.Model):
    quartile=models.CharField(max_length=255, default='')
    package=models.CharField(max_length=255, default='')
    month=models.FloatField(default=0)
    kpi=models.CharField(max_length=255, default='')
    value=models.FloatField(default=0)
    