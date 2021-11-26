from django.http import response
from django.http import JsonResponse
from django.shortcuts import render
import json
import threading
import requests
import pandas as pd
import numpy as np

def data_fresh(req):
    context = {"data1": 1,
               "data2": 2}
    df_spaceships, df_workers = getRawData()
    sp_prices = get_min_spaceships(df_spaceships)
    wk_prices = get_min_workers(df_workers)
    response = []
    for i in sp_prices:
        res = {}
        res['spaceships'] = i
        response.append(res)
    for i in range(len(response)):
        res = response[i]
        res['workers'] = wk_prices[i]
    return JsonResponse(response, safe=False)

# Used in dashboard.js
def full_data_fresh(req):
    context = {"data1": 1,
               "data2": 2}
    df_spaceships, df_workers = getRawData()
    wk_prices = get_min_workers(df_workers)
    response = []
    for i in range(len(response), len(wk_prices)):
        res = {}
        res['category'] = i + 15
        res['value'] = wk_prices[i]
        response.append(res)

    return JsonResponse(response, safe=False)

# Create your views here.
def index(request): 
    context = {"data1": 1,
            "data2": 2}
    df_spaceships, df_workers = getRawData()
    sp_prices = get_min_spaceships(df_spaceships)
    wk_prices = get_min_workers(df_workers)
    response = []
    for i in sp_prices:
        res = {}
        res['spaceships'] = i
        response.append(res)
    for i in range(len(response)):
        res = response[i]
        res['workers'] = wk_prices[i]
    return render(request, 'main/index.html', {'response':response})


def sendReq(gop, url, data, headers):
    furl = url
    print(furl)
    if gop == 'POST':
        response = requests.post(url, data=data, headers=headers)
    elif gop == 'GET':
        response = requests.get(furl, data={}, headers=headers)
    else:
        response = requests.delete(furl, data={}, headers=headers)
    return response

# Get raw data
def getRawData():
    def sendReq(gop, url, data, headers):
        furl = url
        print(furl)
        if gop == 'POST':
            response = requests.post(url, data=data, headers=headers)
        elif gop == 'GET':
            response = requests.get(furl, data={}, headers=headers)
        else:
            response = requests.delete(furl, data={}, headers=headers)
        return response
    
    headers = {
        'Content-type': 'application/json',
    }
    data = {}

    url_sp = ['https://api.cryptomines.app/api/spaceships?level=1&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=2&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=3&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=4&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=5&page=1&limit=10000&sort=eternal']

    res_sp = []
    for url in url_sp:
        response = sendReq('GET', url, data, headers)
        res = response.json()
        res_sp.extend(res['data'])
        
    df_spaceships = pd.json_normalize(res_sp)
    df_spaceships['price'] = df_spaceships['price'].astype(float) / 1000000000000000000
    df_spaceships = df_spaceships[df_spaceships['nftData.level'] != 0]

    
    
    headers = {
    'Content-type': 'application/json',
    }
    data = {}

    url_wk = ['https://api.cryptomines.app/api/workers?level=1&page=1&limit=10000&sort=eternal',
         'https://api.cryptomines.app/api/workers?level=2&page=1&limit=10000&sort=eternal',
         'https://api.cryptomines.app/api/workers?level=3&page=1&limit=10000&sort=eternal',
          'https://api.cryptomines.app/api/workers?level=4&page=1&limit=10000&sort=eternal',
          'https://api.cryptomines.app/api/workers?level=5&page=1&limit=10000&sort=eternal']
    
    res_wk = []
    for url in url_wk:
        response = sendReq('GET', url, data, headers)
        res = response.json()
        res_wk.extend(res['data'])
        
    df_workers = pd.json_normalize(res_wk)
    df_workers['price'] = df_workers['price'].astype(float) / 1000000000000000000
    df_workers = df_workers[df_workers['nftData.level'] != 0]

    return df_spaceships, df_workers


def returnLowestCost(spaceshipSummary, workerSummary, df_spaceships, df_workers):
    # Process spaceship raw data
    df_spaceships_min = df_spaceships[['_id', 'price', 'nftData.level']].groupby('nftData.level').min().rename({'_id': 'Spaceship ID', 'price': 'Spaceship price'}, axis=1)
    df_spaceships_min.index.names = ['Star']
    df_spaceships_min = df_spaceships_min.reset_index()
    
    # Process workers raw data
    df_workers_min = df_workers[['_id', 'price', 'nftData.level', 'nftData.minePower']]
    df_workers_min = df_workers_min.groupby(['nftData.level', 'nftData.minePower']).min()
    df_workers_min = df_workers_min.rename({'_id': 'Worker ID', 'price': 'Worker price'}, axis=1)
    df_workers_min.index.names = ['Star', 'MP']
    df_workers_min = df_workers_min.reset_index()
    
    # Calculate worker cost
    workerSummary = pd.merge(workerSummary, df_workers_min, on = ['Star', 'MP'], how = 'left')
    workerSummary['totalCost'] = workerSummary['Quantity'] * workerSummary['Worker price']
    workerCost = workerSummary['totalCost'].sum()
    
    # Calculate spaceship cost
    spaceshipSummary =pd.merge(spaceshipSummary, df_spaceships_min, on = 'Star', how = 'left')
    spaceshipSummary['totalCost'] = spaceshipSummary['Quantity'] * spaceshipSummary['Spaceship price']
    spaceshipCost = spaceshipSummary['totalCost'].sum()
    
    return workerCost + spaceshipCost

def get_min_spaceships(df_spaceships):
    df_spaceships_min = df_spaceships[['_id', 'price', 'nftData.level']].groupby('nftData.level').min()
    return list(df_spaceships_min['price'])

def get_min_workers(df_workers):
    df_workers_min = df_workers[df_workers['nftData.minePower'] >= 15]
    df_workers_min = df_workers_min[['_id', 'price', 'nftData.level', 'nftData.minePower']]
    df_workers_min = df_workers_min.groupby(['nftData.minePower']).min()
    return list(df_workers_min['price'])

