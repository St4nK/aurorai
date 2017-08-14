"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, user_project_access
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
    models = f.get_models_details()
    data = {'form': form, 'table':json_table, 'columns':json_columns, 'table_models':models, 'user':request.user.id}
    #data=RequestContext(request, data2)
    return render(request,'app/OPEX/upload.html', data)


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

#################
## TEMPLATE V2 ##
#################
## Login and Logout ##
def landingv2(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    path = request.get_full_path()[7:]
    if path =="" : path = "/home"
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'path':path
        }
    return render(
        request,
        'v2/login.html',
        context)

def logout(request):
    """Renders the home page."""
    auth_logout(request)
    assert isinstance(request, HttpRequest)
    path = request.get_full_path()[7:]
    if path =="" : path = "/home"
    context = {
            'title':'Login',
            'year':datetime.now().year,
            'path':path
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
    project_list = f.get_projects_list(request)
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'project_list':project_list,
            'session': f.get_session_info(request),
            'user':request.user,
            
        }
    return render(
        request,
        template,
        context
    )


@login_required
def projects_list(request):
    """Renders the home page."""
    template = 'v2/projects_list.html'
    assert isinstance(request, HttpRequest)
    project_list = f.get_projects_list(request)
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'user':request.user,
			'project_list':project_list,
            'page':'projects_list',
            'session': f.get_session_info(request)
        }
    return render(
        request,
        template,
        context
    )
@login_required
@user_project_access
def project_view(request):
    """Renders the home page."""
    template = 'v2/project_view.html'
    assert isinstance(request, HttpRequest)
    project_list = f.get_projects_list(request)
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'user':request.user,
            'project_list':project_list,
            'page':'project_view',
            'session': f.get_session_info(request)
        }
    return render(
        request,
        template,
        context
    )
@login_required
def edit_project_view(request):
    """Renders the home page."""
    template = 'v2/edit_project.html'
    assert isinstance(request, HttpRequest)
    assigned_users = f.get_assigned_users(request)
    assigned_users = json.dumps(assigned_users)
    unassigned_users = f.get_unassigned_users(request)
    unassigned_users = json.dumps(unassigned_users)
    if request.GET.get('selected') != None:
        new_user = request.GET.get('selected')
        new_user = User.objects.get(first_name=new_user)
        f.add_member(new_user, request)
        assigned_users = f.get_assigned_users(request)
        unassigned_users = f.get_unassigned_users(request)
        data = json.dumps({
            'assigned_users': assigned_users,
            'unassigned_users': unassigned_users
        })
        return HttpResponse(data, content_type='application/json')
    if request.GET.get('delete') != None:
        delete_user = request.GET.get('delete')
        delete_user = User.objects.get(first_name=delete_user)
        f.remove_member(delete_user, request)
        assigned_users = f.get_assigned_users(request)
        unassigned_users = f.get_unassigned_users(request)
        data = json.dumps({
            'assigned_users': assigned_users,
            'unassigned_users': unassigned_users
        })
        return HttpResponse(data, content_type='application/json')
    context = {
            'title': 'Edit Project',
            'year': datetime.now().year,
            'user': request.user,
            'page': 'edit_project',
            'assigned_users': assigned_users,
            'unassigned_users': unassigned_users,
            'session': f.get_session_info(request)
        }
    return render(
        request,
        template,
        context
    )

def select_project_view(request):
   """Renders the home page."""
   template = 'v2/select_project.html'
   assert isinstance(request, HttpRequest)
   project_id =  request.GET.get('id','')
   f.select_project(request, project_id)
   redirect = request.GET.get('redirect','')
   if redirect == "True":
       return HttpResponseRedirect("project_view.html")
   else:
       return HttpResponseRedirect(request.META['HTTP_REFERER'])
       

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
            'page':'opex_dashboard_v2',
            'session': f.get_session_info(request)
        }
    )

@login_required
def opex_visi_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    dataset = f.get_dataset("transactions", ['package','sub_package', 'vendor', 'country'])
    return render(
        request,
        'v2/visibility_dashboard2.html',
        {
            'data2':dataset,
            'title':'Home Page',
            'year':datetime.now().year,
            'user':request.user,
            'page':'opex_visi_dashboard',
            'session': f.get_session_info(request)
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
            'package':package,
            'user':request.user,
            'page':'opex_package_visi_dashboard',
            'session': f.get_session_info(request)

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
            'user':request.user,
            'page':'opex_candm_dashboard',
            'session': f.get_session_info(request)

        }
    )

@login_required
def improve_confidence(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'], user = request.user)
            print(new_file)
            new_file.save()
 
            return HttpResponseRedirect(reverse('improve_confidence'))
    else:
        form = UploadFileForm()
    uploads_root = settings.MEDIA_ROOT
    json_table, json_columns = f.excel_to_json(uploads_root +"/user_4/Data1_light.xlsx",3)
    models = f.get_models_details()
    data = {'form': form, 'table':json_table, 'columns':json_columns, 'table_models':models, 'user_id':request.user.id, 'user':request.user, 'page':'improve_confidence'}
    #data=RequestContext(request, data2)
    return render(request,'v2/improve_confidence.html', data)

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

########################
# Control and Monitoring  
########################


@login_required
def candm_travel(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'v2/candm-travel2.html',
        {
            'page':'candm_travel',
            'user':request.user,
            'session': f.get_session_info(request)
        }
    )
@login_required
def candm_events(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'v2/candm-travel.html',
        {
            'page':'candm_travel',
            'user':request.user,
            'session': f.get_session_info(request)
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

import django_excel as excel

@login_required
def download_file(request):
    #if 'excel' in request.POST:
    sheet = excel.pe.Sheet([[1, 2],[3, 4]])
    output =  excel.make_response(sheet, "xlsx")
    output["Content-Disposition"] = "attachment; filename=Demo-cycle-5.xlsx"
    output["Content-type"] = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return output
    
        
