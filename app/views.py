"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import json
from django.core.urlresolvers import reverse
import functions as f
from run_functions import *
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

def home(request):
    """Renders the home page."""
    template = 'app/home.html'
    assert isinstance(request, HttpRequest)
    return render(
        request,
        template,
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def opex_home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/OPEX/home.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def opex_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor'])
    return render(
        request,
        'app/OPEX/dashboard.html',
        context_instance = RequestContext(request,
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )



from forms import UploadFileForm
from models import UploadFile
 
 
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'], user = request.user)
            print(new_file)
            new_file.save()
 
            return HttpResponseRedirect(reverse('upload'))
    else:
        form = UploadFileForm()
    uploads_root = settings.MEDIA_ROOT
    json_table, json_columns = f.excel_to_json(uploads_root +"/user_4/Data1_light.xlsx",3)
    models = f.get_models()
    data = {'form': form, 'table':json_table, 'columns':json_columns, 'table_models':models, 'user':request.user.id}
    return render_to_response('app/OPEX/upload.html', data, context_instance=RequestContext(request))


def landing(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/landing.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'request':request,
            'user':request.user
        })
    )

def welcome(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/welcome.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'request':request,
            'user':request.user
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

################
# TEMPLATE V2 ##
################
def home_v2(request):
    """Renders the home page."""
    template = 'v2/index.html'
    assert isinstance(request, HttpRequest)
    return render(
        request,
        template,
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def landingv2(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'v2/login.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'request':request,
            'user':request.user
        })
    )
def opex_dashboard_v2(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor', 'gl'])
    return render(
        request,
        'v2/opex_dashboard.html',
        context_instance = RequestContext(request,
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def opex_visi_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor'])
    return render(
        request,
        'v2/visibility_dashboard.html',
        context_instance = RequestContext(request,
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def opex_package_visi_dashboard(request, package):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['sub_package', 'vendor', 'gl'], {"package":package})
    package_list= f.get_value_list("transactions", "package")
    return render(
        request,
        'v2/package_visi_dashboard.html',
        context_instance = RequestContext(request,
        {
            'package_list':package_list,
            'data2':dataset,
            'package':package
            
        })
    )
def opex_candm_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_visi(1, ['package','month'])
    return render(
        request,
        'v2/c_and_m_dashboard.html',
        context_instance = RequestContext(request,
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def adddata(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    message = 'none'
    if request.method == 'POST':
        model = request.POST['model']
        variables = request.POST
        message = f.insert_new_data(variables)
    model_list = f.get_models_details()
    return render(
        request,
        'v2/adddata.html',
        context_instance = RequestContext(request,
        {
            'model_list':model_list,
            'page':'Add Data',
            'message':message,
        })
    )
################
# JSON REQUESTS 
################
def get_json_table(request):
    if request.method == 'GET':
        uploads_root = settings.MEDIA_ROOT
        file = request.GET['file']
        user_id = request.GET['user_id']
        json_table, json_columns = f.excel_to_json(uploads_root +"/user_"+user_id+"/"+file,3)
        data = {
            'json_table':json_table,
            'json_columns':json_columns
        }
        data = json.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(data)