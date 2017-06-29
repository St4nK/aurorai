"""
Definition of urls for DjangoApp.
"""

from datetime import datetime
from django.conf.urls import url, include
from app.forms import BootstrapAuthenticationForm
from app.views import *
from app.models import *
from django.contrib.auth.views import *


# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    ## Identification ##
    url('', include('social_django.urls', namespace='social')),  
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', landingv2, name='landing'),
    url(r'^welcome', welcome, name='welcome'),
    url(r'^home', home_v2, name='home'),
    url(r'^upload', upload, name='upload'),
    url(r'^opex/home', opex_home, name='opex_home'),
    url(r'^opex/projects_list', projects_list, name='projects_list'),
    url(r'^opex/project_view/(?P<project>(\w*))', project_view, name='project_view'),
    url(r'^opex/dashboard', opex_dashboard_v2, name='opex_dashboard_v2'),
    url(r'^opex/visibility/$', opex_visi_dashboard, name='opex_visi_dashboard'),
    url(r'^opex/visibility/package/(?P<package>(\w*))', opex_package_visi_dashboard, name='opex_package_visi_dashboard'),
    url(r'^opex/visibility/improve_confidence', improve_confidence, name='improve_confidence'),
    url(r'^opex/candm/', opex_candm_dashboard, name='opex_candm_dashboard'),
    url(r'^adddata/', adddata, name='adddata'),
    url(r'^download/', download_file, name='download_file'),

    ## Control and Monitoring
    url(r'^candm/travel', candm_travel, name='candm_travel'),

    ## API Calls ##
    url(r'^get_json_table', get_json_table, name='get_json_table'),
    url(r'^get_json_dataset', get_json_dataset, name='get_json_datase'),

    ## Login Logout ##
    url(r'^login/$', landingv2, name='landing'),
    url(r'^logout$', logout, {  'next_page': '/'  },        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ### To be deleted ###
    url(r'^opex/dashboardv1', opex_dashboard, name='opex_dashboard'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
    url(r'^v2', home_v2, name='home_v2'),
]
