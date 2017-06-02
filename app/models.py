"""
Definition of models.
"""

from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

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
    