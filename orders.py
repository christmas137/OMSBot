# orders.py
import requests
import os
from dotenv import load_dotenv


load_dotenv()


domain ="rrpoms.pmru.local"
def send_cancel_request(url, body, headers):
    response = requests.patch(url, json=body, headers=headers, verify=False)
    return response

def cancel_order(order_id):
    url = f"https://{domain}/api/retail/retailsaleorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_ORDER_AUTH')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailSaleOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other"
        }
    }
    return send_cancel_request(url, body, headers)

def cancel_self_reg_order(order_id):
    url = f"https://{domain}/api/selfreg/retailsaleorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_SELF_REG')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailSaleOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other"
        }
    }
    return send_cancel_request(url, body, headers)

def cancel_return_order(order_id):
    url = f"https://{domain}/api/retail/retailreturnorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_RETURN_ORDER')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailReturnOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other"
        }
    }
    return send_cancel_request(url, body, headers)

def cancel_replacement_order(order_id):
    url = f"https://{domain}/api/retail/retailreplacementorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_REPLACE_ORDER')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailReplacementOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other"
        }
    }
    return send_cancel_request(url, body, headers)

def cancel_lending_order(order_id):
    url = f"https://{domain}/api/retail/retaillendingorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_LENDING_ORDER')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailLendingOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other"
        }
    }
    return send_cancel_request(url, body, headers)

def cancel_ecom_order(order_id):
    url = f"https://{domain}/api/ecom/retailsaleorders/{order_id}"
    headers = {
        'Authorization': f"{os.getenv('CANCEL_ECOM_ORDER')}",
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    body = {
        "$type": "PMI.BDDM.Transactionaldata.RetailSaleOrder",
        "Status": "Cancelled",
        "CancellationInfo": {
            "Channel": "CallCenter",
            "Comment": "",
            "Initiator": "CallCenter",
            "Reason": "Other",
            "RequestDate": "2024-04-02T00:00:00.0Z"
        }
    }
    return send_cancel_request(url, body, headers)
