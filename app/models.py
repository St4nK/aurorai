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

class CandMTravel(models.Model):
    Region=models.CharField(max_length=255, default='')
    Country=models.CharField(max_length=255, default='')
    Function=models.CharField(max_length=255, default='')
    Scenario=models.CharField(max_length=255, default='')
    Package=models.CharField(max_length=255, default='')
    SubPackage=models.CharField(max_length=255, default='')
    FTE=models.FloatField(default=0)
    Month=models.CharField(max_length=255, default='')
    Spend=models.FloatField(default=0)
    FTE_travel=models.FloatField(default=0)
    NR_Month=models.FloatField(default=0)
    Total_Trips=models.FloatField(default=0)
    Trips_14D=models.FloatField(default=0)
    DomTrip_2D=models.FloatField(default=0)
    UnitPrice=models.FloatField(default=0)
    Trip_length=models.FloatField(default=0)


class BenchmarkVisi(models.Model):
    quartile=models.CharField(max_length=255, default='')
    package=models.CharField(max_length=255, default='')
    month=models.FloatField(default=0)
    kpi=models.CharField(max_length=255, default='')
    value=models.FloatField(default=0)

class MappingFull(models.Model):
    UIN=models.CharField(max_length=255, default='')
    Team=models.CharField(max_length=255, default='')
    Sector=models.CharField(max_length=255, default='')
    Country=models.CharField(max_length=255, default='')
    ClientGLDescription=models.CharField(max_length=255, default='')
    ClientVendorDescription=models.CharField(max_length=255, default='')
    ClientSpecific1=models.CharField(max_length=255, default='')
    ClientSpecific2=models.CharField(max_length=255, default='')
    ClientSpecific3=models.CharField(max_length=255, default='')
    ClientSpecific4=models.CharField(max_length=255, default='')
    ClientSpecific5=models.CharField(max_length=255, default='')
    ClientSpecific6=models.CharField(max_length=255, default='')
    ClientSpecific7=models.CharField(max_length=255, default='')
    ClientSpecific8=models.CharField(max_length=255, default='')
    ClientSpecific9=models.CharField(max_length=255, default='')
    ClientSpecific10=models.CharField(max_length=255, default='')
    ClientSpecific11=models.CharField(max_length=255, default='')
    ClientSpecific12=models.CharField(max_length=255, default='')
    ClientSpecific13=models.CharField(max_length=255, default='')
    ClientSpecific14=models.CharField(max_length=255, default='')
    ClientSpecific15=models.CharField(max_length=255, default='')
    ClientSpecific16=models.CharField(max_length=255, default='')
    ClientSpecific17=models.CharField(max_length=255, default='')
    ClientSpecific18=models.CharField(max_length=255, default='')
    ClientSpecific19=models.CharField(max_length=255, default='')
    ClientSpecific20=models.CharField(max_length=255, default='')
    ClientSpecific21=models.CharField(max_length=255, default='')
    ClientSpecific22=models.CharField(max_length=255, default='')
    Industry_Specific=models.CharField(max_length=255, default='')
    Exclude_from_Mapping=models.CharField(max_length=255, default='')
    ORIGINALSPENDLOCALCURRENCY=models.FloatField(default=0)
    Fx=models.CharField(max_length=255, default='')
    ORIGINALSPEND=models.FloatField(default=0)
    REVISEDSPEND=models.FloatField(default=0)
    DefaultMappingCostSegment=models.CharField(max_length=255, default='')
    DefaultMappingCostSubSegment=models.CharField(max_length=255, default='')
    DefaultMappingComment=models.CharField(max_length=255, default='')
    Topofspend=models.CharField(max_length=255, default='')
    Absolutevalueofspend=models.FloatField(default=0)
    AnalyticsTeamOwner=models.CharField(max_length=255, default='')
    InMarketTeamOwner=models.CharField(max_length=255, default='')
    DetailedMappingCostSegment=models.CharField(max_length=255, default=''),
    DetailedMappingCostSubSegment=models.CharField(max_length=255, default='')
    DetailedMappingComment=models.CharField(max_length=255, default='')
    MappingStatus=models.CharField(max_length=255, default='')
    Detailed_mapping_flag_for_mapping_usage=models.CharField(max_length=255, default='')
    Detailed_mapping_error=models.CharField(max_length=255, default='')
    MappingQuestion=models.CharField(max_length=255, default='')
    MappingAnswer=models.CharField(max_length=255, default='')
    MappingRationale=models.CharField(max_length=255, default='')
    SplitStatus=models.CharField(max_length=255, default='')
    prio_for_review=models.CharField(max_length=255, default='')
    quality_index=models.FloatField(default=0)
    Autom_index=models.FloatField(default=0)
    First_SubCategory_Cat=models.CharField(max_length=255, default='')
    First_SubCategory=models.CharField(max_length=255, default='')
    First_SubCategory_Prob=models.CharField(max_length=255, default='')
    Sec_SubCategory_Cat=models.CharField(max_length=255, default='')
    Sec_SubCategory=models.CharField(max_length=255, default='')
    Sec_SubCategory_Prob=models.CharField(max_length=255, default='')
    Keyword_GL=models.CharField(max_length=255, default='')
    Keyword_Vendor=models.CharField(max_length=255, default='')
    Keywords_PO=models.CharField(max_length=255, default='')
    LASTCHANGEDBY=models.CharField(max_length=255, default='')
    Dateoflastchange=models.CharField(max_length=255, default='')
    Status=models.CharField(max_length=255, default='')
    Count=models.FloatField(default=0)
    MappedSpend=models.FloatField(default=0)
    LatestCategoryMapping=models.CharField(max_length=255, default='')
    LatestSubCategoryMapping=models.CharField(max_length=255, default='')
    LAST_UPDATE=models.DateTimeField(auto_now_add=True)

    