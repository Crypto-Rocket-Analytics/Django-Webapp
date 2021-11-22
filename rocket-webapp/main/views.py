from django.http import response
from django.shortcuts import render
import threading
import requests
import pandas as pd
import numpy as np
import json

# Create your views here.
def index (request): 
    df_spaceships, df_workers = getRawData()
    sp_prices = get_min_spaceships(df_spaceships)
    wk_prices = get_min_workers(df_workers)
    res = {}
    res['spaceships'] = sp_prices
    res['workers'] = wk_prices
    response = json.dumps(res)
    print(response)
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

    url = 'https://api.cryptomines.app/api/spaceships'

    response = sendReq('GET', url, {}, headers)
    print("get response")
    res = response.json()
    # df_spaceships = pd.read_json(json.dumps(res))
    df_spaceships = pd.json_normalize(res)
    df_spaceships['price'] = df_spaceships['price'].astype(float) / 1000000000000000000
    df_spaceships = df_spaceships[df_spaceships['nftData.level'] != 0]

    
    
    headers = {
    'Content-type': 'application/json',
    }

    url = 'https://api.cryptomines.app/api/workers'
    data = {}
    response = sendReq('GET', url, data, headers)
    res = response.json()
    # df_workers = pd.read_json(json.dumps(res))
    df_workers = pd.json_normalize(res)
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

