"""
AurorAI Functions Files
Author: Christophe Castan
Date of creation : 18/05/2017
Last Update: 18/05/2017
"""
import numpy
import pandas
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Sum
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
start_time = time.time()
######################################
###### EXCEL IMPORT FUNCTIONS ########
######################################


def open_excel(file):
    print("Opening the file...")
    df = pandas.read_excel(file)
    return df

def df_to_json(df):
    return df.to_json(orient="index")

def excel_to_json(file, n_lines=None):
    df = open_excel(file)
    json_columns = json.dumps(list(df), cls=DjangoJSONEncoder)
    if n_lines <> None:
        json_table = df_to_json(df.head(n_lines))
    else:
        json_table = df_to_json(df)

    return json_table, json_columns

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

def get_models_details():
    models_details = []
    app_models = apps.get_app_config('app').get_models()
    for model in app_models:
        models_details.append([model._meta.db_table, 
                              fields(model)])
    json_models = json.dumps(models_details, cls=DjangoJSONEncoder)
    return json_models



######################################
######## DATA SET FUNCTIONS ##########
######################################

def get_dataset(table,dimensions, filters={}):
    if table == 'transactions' :
        if filters != {} :
            object=Transaction.objects.filter(**filters)
        else:
            object=Transaction.objects
        dataset = object.values(*dimensions).annotate(value=Sum('spend'), count = Count('uid'))
        dataset_json = json.dumps(list(dataset), cls=DjangoJSONEncoder)
    if table == 'candmtravel':
        if filters != {} :
            object=CandMTravel.objects.filter(**filters)
        else:
            object=CandMTravel.objects
        dataset = object.values(*dimensions).annotate(value=Sum('Spend'), count = Count('id'))
        dataset_json = json.dumps(list(dataset), cls=DjangoJSONEncoder)
        print dataset_json
    return dataset_json


def get_value_list(table,dimension):
    object=Transaction.objects
    value_list = object.order_by(dimension).values_list(dimension, flat = True).distinct()
    
    return json.dumps(list(value_list), cls=DjangoJSONEncoder)


def get_assigned_users(request):  # returns users assigned to current project
    users = Project_User.objects.filter(project_id=request.session.get('project'))
    users_list = []
    for u in users:
        users_list.append(u.user.first_name.encode("latin-1"))
    users_list = json.dumps(users_list)

    return users_list


def get_unassigned_users(request):  # returns users unassigned to current project
    assigned_users = Project_User.objects.filter(project_id=request.session.get('project'))

    assigned_users_names = []
    for u in assigned_users:
        assigned_users_names.append(u.user.first_name.encode("latin-1"))
    assigned_users_names = json.dumps(assigned_users_names)

    unassigned_users = []
    for u in User.objects.all():
        if u.first_name not in assigned_users_names:
            print u.first_name
            unassigned_users.append(u.first_name.encode("latin-1"))

    return json.dumps(unassigned_users)


def get_projects_list(request):  # returns projects assigned to current user
    projects = Project_User.objects.filter(user = request.user)
    project_list = []
    for p in projects:
		project_list.append(p.project)
		print(p.id)
	
    return project_list

def get_visi(company_id, dimensions):
    company = CompanyInfo.objects.get(id = company_id)
    object = CompanyVisi.objects.filter(company = company)
    dataset = object.values(*dimensions).annotate(value = Sum('spend'))
    dataset_json = json.dumps(list(dataset), cls = DjangoJSONEncoder)
    return dataset_json

######################################
########  UPLOAD FUNCTIONS  ##########
######################################

def insert_new_data(variables):
    model = ''
    fields = []
    for key, value in variables.iteritems():
        print ("%s %s" % (key, value))
    return 'ok'

def add_member(new_user, request):
    project = get_session_info(request).get('project')
    new_entry_Project_User = Project_User(user=new_user, project=project, role="")
    new_entry_Project_User.save()


def remove_member(user, request):
    if user != request.user:
        project = get_session_info(request).get('project')
        project_user = Project_User.objects.get(user=user, project=project)
        entry_Project_User = Project_User(id=project_user.id, user = user, project = project, role = "")
        entry_Project_User.delete()
    

######################################
########  SESSION FUNCTIONS  #########
######################################

def get_session_info(request):
    project_id = request.session.get('project', None)
    print project_id
    if project_id != None :
        project = Project.objects.get(id=project_id)
    else:
        project = None
        try:
            exists = Project_User.objects.get(project_id=1, user_id=request.user)
        except ObjectDoesNotExist:
            email = User.objects.get(id=request.user.id).email
            if email[-13:] == 'accenture.com':
                default_project = Project.objects.get(id=1)
                new_entry_Project_User = Project_User(user=request.user, project=default_project, role="")
                new_entry_Project_User.save()
    notification = request.session.get('notification', None)
    session = {
        'project':project,
        'notification': notification,
        }
    return session

def select_project(request, project_id):
    project = Project_User.objects.get(user = request.user, project = project_id)
    request.session['project'] = project.project_id

