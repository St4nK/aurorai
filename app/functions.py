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
    model1 = ['Column1', 'data', 'Column3']
    models.append(['model1',model1])
    model2 = ['uin', 'Column4', 'Column5', 'Column6']
    models.append(['model2',model2])
    json_models = json.dumps(models, cls=DjangoJSONEncoder)
    return json_models


######################################
######## DATA SET FUNCTIONS ##########
######################################

def get_dataset(table,dimensions):
    if table == 'transactions' :
        object=Transaction.objects
        dataset = object.values(*dimensions).annotate(value=Sum('spend'), count = Count('uid'))
        dataset_json = json.dumps(list(dataset), cls=DjangoJSONEncoder)

    return dataset_json

def get_visi(company_id, dimensions):
    company = CompanyInfo.objects.get(id = company_id)
    object = CompanyVisi.objects.filter(company = company)
    dataset = object.values(*dimensions).annotate(value = Sum('spend'))
    dataset_json = json.dumps(list(dataset), cls = DjangoJSONEncoder)
    return dataset_json

