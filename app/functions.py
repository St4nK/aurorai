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

def get_models():
    models = []
    model1 = fields(VisiFinancials)
    models.append(['VisiFinancials',model1])
    model2 = fields(VisiMappings)
    models.append(['VisiMappings',model2])
    json_models = json.dumps(models, cls=DjangoJSONEncoder)
    return json_models

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

    return dataset_json

def get_value_list(table,dimension):
    object=Transaction.objects
    value_list = object.order_by(dimension).values_list(dimension, flat = True).distinct()
    
    return json.dumps(list(value_list), cls=DjangoJSONEncoder)

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