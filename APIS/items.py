import json
import requests
import base64
import numpy as np
from datetime import datetime
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
client_id = 'BF6CC1CFA8C34E57A991E5730BB68D90'
client_secret = '1N9Zh0PMTdA9uLII33PMq5Gfg34-BVozal67fNSWL0uL-hjc'
redirect_url = 'https://xero.com/'
scope = 'offline_access accounting.transactions accounting.reports.read'
b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
itemsApi='https://api.xero.com/api.xro/2.0/Items'
def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
#     print(json_response)
    
    for tenants in json_response:
        json_dict = tenants
#         print(json_dict)
    return json_dict['tenantId']

def XeroRefreshToken(refresh_token):
    print(refresh_token)
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                            headers = {
                                'Authorization' : 'Basic ' + b64_id_secret,
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type' : 'refresh_token',
                                'refresh_token' : refresh_token
                            })
    json_response = response.json()
    # print(json_response)
    
    new_refresh_token = json_response['refresh_token']
    rt_file = open(r'data/refresh_token.txt', 'w+')
    rt_file.write(new_refresh_token)
    rt_file.close()
    
    return [json_response['access_token'], json_response['refresh_token']]

def XeroRequests():
    old_refresh_token = open(r'data/refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token)
    xero_tenant_id = XeroTenants(new_tokens[0])
    
    get_url = itemsApi
    response = requests.get(get_url,
                           headers = {
                               'Authorization': 'Bearer ' + new_tokens[0],
                               'Xero-tenant-id': xero_tenant_id,
                               'Accept': 'application/json'
                           })
    json_response = response.json()
#     print(f"JSON RESPONSE : {json_response}")
    
    xero_output = open(r'data/xero_output_items.txt', 'w+')
    xero_output.write(response.text)
    xero_output.close()
    # print(f"Length of Invoices : {len(json_response['Items'])}")
    # print(f"XeroRequests : COMPLETED")
XeroRequests()
from datetime import datetime
def export_csv_payments():
    invoices = open(r'data/xero_output_items.txt', 'r').read()
    json_invoice = json.loads(invoices)
    analysis = open(r'data/xero_output_items.csv', 'w+')
    analysis.write('Name' + ',' + 'purchaseUnitPrice'+ ','+ 'saleUnitPrice')
    analysis.write('\n')
    
    for val in json_invoice['Items']:
        for purchase,sale in zip(val['PurchaseDetails'],val['SalesDetails']):
            analysis.write(
                str(val['Name']) + ',' + 
                str(purchase['UnitPrice']) + ',' + 
                str(sale['UnitPrice'])
            )
            analysis.write('\n')
    
    analysis.close()
    # print(f"export_csv_payments : COMPLETED")
import pandas as pd
import matplotlib.pyplot as plt
# def chart_data():
#     df = pd.read_csv(r'data/xero_output_items.csv')
# #     df['Date']=pd.to_datetime(df['Date'])'saleUnitPrice'
#     print(f"DATA SET : {df} ")
#     pvt = df[ ['Name','purchaseUnitPrice'] ].groupby('Name').sum()
#     pvt2 = df[ ['Name','saleUnitPrice'] ].groupby('Name').sum()
#     print(pvt)
    
#     pvt.plot.bar()
#     pvt2.plot.bar()
#     plt.show()

def init():
    XeroRequests()
    export_csv_payments()
    df=pd.read_csv('data/xero_output_items.csv')
    # print(df)
    # df['Date']=pd.to_datetime(df['Date'])
    # df.sort_values(by='Date',ascending=False)
    fig = go.Figure(
    data=[
        go.Bar(
            x=df['Name'],
            y=df['purchaseUnitPrice'],
           
            # name=name,
        ),
        go.Bar(
            x=df['Name'],
            y=df['saleUnitPrice'],
           
            # name=name,
        ),
    ],
    layout=go.Layout(
    )
    )
    fig.update_layout(
    title_text=f'<b>Items W.R.T Purchase & Sale Price</b>',
    title_font_size=22,
    bargap=0.15,
    # height=550,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1,  # gap between bars of the same location coordinate.
    paper_bgcolor='white',
    plot_bgcolor='white',
    )
    return dcc.Graph(figure=fig)