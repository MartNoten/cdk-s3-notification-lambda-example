import codecs
import csv
import json
import urllib.parse
import boto3

s3 = boto3.client('s3')

GROCERY_TAGS = ['ALBERT HEIJN', ]
FOOD_DELIVERY = ['Thuisbezorgdnl']
FOOD_DURING_TRAVEL = ['CCVStarbucks', 'Smullers', 'AH to Go', 'Mc Donalds']
MOVIES = ['PATHE THEATERS']
WEBSHOP_PURCHASES = ['bol.com', '']
VINYL_RECORDS = ['Plato']
EATING_OUT = ['Restaurant Lombok', 'Drink en Eetlokaal']

def handler(event, context):
    file_data = download_file(event)
    costs = analyze_records(file_data)
    print(costs)
    

def download_file(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def analyze_records(data):    
    costs = {
        "GROCERY": {
            'total': 0,
            'records': []
        },
        "VINYL": {
            'total': 0,
            'records': []
        },
        "WEBSHOP": {
            'total': 0,
            'records': []
        },
        "MOVIES": {
            'total': 0,
            'records': []
        },
        "FOOD_DELIVERY": {
            'total': 0,
            'records': []
        },
        "COMMUTE_FOOD": {
            'total': 0,
            'records': []
        },
    }

    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        for word in row['Naam / Omschrijving'].split(" "):
            spend = float(row['Bedrag (EUR)'].replace(",","."))
            if word in GROCERY_TAGS:
                costs['GROCERY']['total'] += spend
                costs['GROCERY']['records'] += row

            if word in VINYL_RECORDS:
                costs['VINYL']['total'] += spend
                costs['VINYL']['records'] += row

            if word in FOOD_DURING_TRAVEL:
                costs['COMMUTE_FOOD']['total'] += spend
                costs['COMMUTE_FOOD']['records'] += row
            
            if word in WEBSHOP_PURCHASES:
                costs['WEBSHOP']['total'] += spend
                costs['WEBSHOP']['records'] += row
                                               
    return costs
