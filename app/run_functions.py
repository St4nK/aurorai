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
import sys
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Sum
from app.models import *
import pyexcel as pe


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
######## EXCEL LOAD FUNCTIONS ########
######################################

def xl_to_records(file, rl=1000000):
    sheet = pe.get_sheet(file_name=file, name_columns_by_row=0, row_limit=rl)
    records = sheet.to_records()
    return records

def add_pk (records, column, pk):
    sheet = pe.get_sheet(records=records, name_columns_by_row=0)
    n_rows = (len(list(sheet.rows())))
    pks = [pk] * n_rows
    sheet.column[column] = pks
    records_out = sheet.to_records()
    return records_out

def load_records_to_db(records, model):
    n_rows = (len(list(records)))
    i=1
    objs=[]
    for rec in records:
        row = model(**rec)
        sys.stdout.write("loading " + str(i) + " on " + str(n_rows) + "\r")
        sys.stdout.flush()
        objs.append(row)
        #row.save()
        i=i+1
    model.objects.bulk_create(objs)
    return True

#rec = xl_to_records(file="C:/Users/christophe.castan/Documents/AurorAI/AurorAIApp/uploads/BenchmarkVisi.xlsx")
#pk=BenchmarkVisi.objects.get(id=1)
#rec = add_pk(rec, "company", pk)
#load_records_to_db(rec,BenchmarkVisi)

def get_visi(company_id, dimensions):
    company = CompanyInfo.objects.get(id = company_id)
    object = CompanyVisi.objects.filter(company = company)
    dataset = object.values(*dimensions).annotate(value = Sum('spend'))
    dataset_json = json.dumps(list(dataset), cls = DjangoJSONEncoder)
    return dataset_json