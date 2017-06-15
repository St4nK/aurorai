"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
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

def handler404(request):
    response = render_to_response('v2/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('v2/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

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
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'request':request,
            'user':request.user
        }
    return render(
        request,
        'app/landing.html',
        context
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

def logout(request):
    """Renders the home page."""
    auth_logout(request)
    assert isinstance(request, HttpRequest)
    context = {
            'title':'Login',
            'year':datetime.now().year,
            'path':request.get_full_path()
        }
    return render(
        request,
        'v2/login.html',
        context)

@login_required
def home_v2(request):
    """Renders the home page."""
    template = 'v2/index.html'
    assert isinstance(request, HttpRequest)
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'user':request.user
        }
    return render(
        request,
        template,
        context
    )

def landingv2(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    path = request.get_full_path()[7:]
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'path':path
        }
    return render(
        request,
        'v2/login.html',
        context)

@login_required
def opex_dashboard_v2(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor', 'gl'])
    return render(
        request,
        'v2/opex_dashboard.html',
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

@login_required
def opex_visi_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor'])
    return render(
        request,
        'v2/visibility_dashboard.html',
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

@login_required
def opex_package_visi_dashboard(request, package):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    #dataset = f.get_dataset("transactions", ['sub_package', 'vendor', 'gl'], {"package":package})
    package_list= f.get_value_list("transactions", "package")
    context = {
            'package_list':package_list,
            #'data2':dataset,
            'package':package
            
        }
    return render(
        request,
        'v2/package_visi_dashboard.html',
        context
        )
 
@login_required   
def opex_candm_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_visi(1, ['package','month'])
    return render(
        request,
        'v2/c_and_m_dashboard.html',
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

@login_required
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
        {
            'model_list':model_list,
            'page':'Add Data',
            'message':message,
        }
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
def get_json_dataset(request):
    if request.method == 'POST' :
        queryset = request.POST
        table = request.POST['table']
        dimensions = queryset.getlist('dimensions[]')
        filters = json.loads(request.POST.get('filters'))
        package = 'Sales'
        dataset = f.get_dataset(table, dimensions, filters)
        #print(dataset)
        return HttpResponse(dataset)
