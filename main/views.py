from django.http import response
from django.http import JsonResponse
from django.shortcuts import render
import json
import asyncio
import requests
import pandas as pd
import numpy as np

PAGE_VIEW_COUNT = 0
ADD_BUTTON_CLICK_COUNT = 0
CALCULATE_BUTTON_CLICK_COUNT = 0
DATA = []
res_wk = []
res_sp = []

def data_fresh(req):
    api = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=11736&range=1D"
    res = requests.get(api).json()
    etlspaceships = list(res["data"]["points"].items())[-1][1]["v"][0]
    df_spaceships, df_workers = getRawData()
    sp_prices = get_min_spaceships(df_spaceships)
    wk_prices = get_min_workers(df_workers)
    response = []
    for i in sp_prices:
        res = {}
        res['spaceships'] = i
        res['etlspaceships'] = round(i * etlspaceships, 2)
        response.append(res)
    for i in range(len(response)):
        res = response[i]
        res['workers'] = wk_prices[i]
    return JsonResponse(response, safe=False)

# Used in dashboard.js
def full_data_fresh(req):
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
    global PAGE_VIEW_COUNT
    PAGE_VIEW_COUNT += 1
    return render(request, 'main/index.html')


async def sendReq(url_sp, url_wk):
    global res_sp
    global res_wk
    headers = {
    'Content-type': 'application/json',
    }
    url_sp.extend(url_wk)
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None, 
            requests.get, 
            url_sp[i]
        )
        for i in range(10)
    ]
    for response in await asyncio.gather(*futures):
        if response.url.find('spaceships') != -1:
            res_sp.extend(response.json()['data'])
        elif response.url.find('workers') != -1:
            res_wk.extend(response.json()['data'])

# Get raw data
def getRawData():
    global res_sp
    global res_wk
    
    url_sp = ['https://api.cryptomines.app/api/spaceships?level=1&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=2&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=3&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=4&page=1&limit=10000&sort=eternal', 
          'https://api.cryptomines.app/api/spaceships?level=5&page=1&limit=10000&sort=eternal']
        


    url_wk = ['https://api.cryptomines.app/api/workers?level=1&page=1&limit=10000&sort=eternal',
         'https://api.cryptomines.app/api/workers?level=2&page=1&limit=10000&sort=eternal',
         'https://api.cryptomines.app/api/workers?level=3&page=1&limit=10000&sort=eternal',
          'https://api.cryptomines.app/api/workers?level=4&page=1&limit=10000&sort=eternal',
          'https://api.cryptomines.app/api/workers?level=5&page=1&limit=10000&sort=eternal']
    
    res_wk = []
    res_sp = []

    loop = asyncio.new_event_loop()
    loop.run_until_complete(sendReq(url_sp, url_wk))

    df_spaceships = pd.json_normalize(res_sp)
    df_spaceships['price'] = df_spaceships['price'].astype(float) / 1000000000000000000
    df_spaceships = df_spaceships[df_spaceships['nftData.level'] != 0]
        
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

def tracker(req):
    return JsonResponse({"PAGE_VIEW_COUNT": PAGE_VIEW_COUNT, "ADD_BUTTON_CLICK_COUNT": ADD_BUTTON_CLICK_COUNT, "CALCULATE_BUTTON_CLICK_COUNT": CALCULATE_BUTTON_CLICK_COUNT, "DATA": DATA}, safe=False)

def add_button_click(req):
    global ADD_BUTTON_CLICK_COUNT
    ADD_BUTTON_CLICK_COUNT += 1
    return JsonResponse({"success": True}, safe=False)

def calculate_button_click(req):
    global CALCULATE_BUTTON_CLICK_COUNT
    CALCULATE_BUTTON_CLICK_COUNT += 1
    return JsonResponse({"success": True}, safe=False)

def getTrackerData(request):
    global DATA
    DATA.append({"workers": request.GET['workers'], "spaceshipCapacity": request.GET['spaceshipCapacity'],"mp": request.GET['mp'],"rank": request.GET['rank'],"cost": request.GET['cost'], })
    return JsonResponse({"success": True}, safe=False)
