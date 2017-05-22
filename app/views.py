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
from django.db.models import Count, F, Sum
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from app.models import *

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
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
    ppcs=Transaction.objects
    data=ppcs.values('package').annotate(label=F('package'), value=Sum('spend')).order_by('-value')
    data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    data2 = ppcs.values('package','sub_package').annotate(value=Sum('spend'))
    data2_json = json.dumps(list(data2), cls=DjangoJSONEncoder)
    return render(
        request,
        'app/OPEX/dashboard.html',
        context_instance = RequestContext(request,
        {
            'data':data_json,
            'data2':data2_json,
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
def opex_visi_dashboard(request):
    """Renders the opex dashboard."""
    assert isinstance(request, HttpRequest)
    ppcs=Transaction.objects
    data=ppcs.values('package').annotate(label=F('package'), value=Sum('spend')).order_by('-value')
    data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    data2 = ppcs.values('package','sub_package').annotate(value=Sum('spend'))
    data2_json = json.dumps(list(data2), cls=DjangoJSONEncoder)
    return render(
        request,
        'app/OPEX/visibility/dashboard.html',
        context_instance = RequestContext(request,
        {
            'data':data_json,
            'data2':data2_json,
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