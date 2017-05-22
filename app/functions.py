"""
AurorAI Functions Files
Author: Christophe Castan
Date of creation : 18/05/2017
Last Update: 18/05/2017
"""
import pandas
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
start_time = time.time()


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

print (get_models())

#print(excel_to_json("C:\Users\christophe.castan\Documents\AurorAI\AurorAIApp\uploads\user_4\Data1_light.xlsx"))

#print("--- %s seconds ---" % (time.time() - start_time))