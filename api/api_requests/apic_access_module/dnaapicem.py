import requests
import json

from requests.exceptions import Timeout
from django.core.exceptions import ObjectDoesNotExist
from requests.auth import HTTPBasicAuth

from app.models import Network

DEF_TIMEOUT = 5

requests.packages.urllib3.disable_warnings()

def apic_get_X_auth_token(ip=None, uname=None, pword=None):
    r_json = {
        "username": uname,
        "password": pword
    }

    post_url = "https://" + ip + "/api/system/v1/auth/token"

    headers = {'content-type': 'application/json',}

    try:
        r = requests.post(post_url, auth=HTTPBasicAuth(uname, pword), headers=headers, verify=False, timeout=DEF_TIMEOUT)
    except Timeout as e:
        raise Timeout(e)
    except:
        raise BaseException('Something went wrong while getting access token')
    else:
        response_data = r.json()
        if 'Token' in response_data.keys():
            return response_data['Token']
        elif 'exp' in response_data.keys():
            raise PermissionError(response_data['exp'] + '.')
        elif 'errorCode' in response_data.keys() and response_data['errorCode'] == 'INVALID_CREDENTIALS':
            raise PermissionError(response_data['detail'] + '. ' + response_data['message'])
        #"error": "Authentication has failed. Please provide valid credentials."

def get_query_credentials():
    """
    Get query credentials for current network from DB
    :return: Dictionary
            {
                'ip': network-ip,
                'ticket': API-service-ticket
            }
    """
    try:
        network = Network.objects.get(current=True)
    except ObjectDoesNotExist:
        return {}
    else:
        return {'ip': network.ip,
                'ticket': network.service_ticket}

def get(api='', params='', ver=''):
    cred = get_query_credentials()

    if cred:
        url = "https://" + cred['ip'] + "/" + api
        headers = {"x-auth-token": cred['ticket']}

        try:
            resp = requests.get(url, headers=headers, params=params, verify=False, timeout=DEF_TIMEOUT)
        except Timeout as e:
            raise Timeout(e)
        except:
            raise BaseException('Something went wrong while making GET request')
        else:
            return (resp.json()['response'])
    else:
        raise BaseException('Unable to make request. No credentials')

def post(api='', data='', ver=''):
    cred = get_query_credentials()

    if cred:
        url = "https://" + cred['ip'] + "/api/" + ver + "/" + api
        headers = {"content-type": "application/json", "x-auth-token": cred['ticket']}

        try:
            resp = requests.post(url, json.dumps(data), headers=headers, verify=False, timeout=DEF_TIMEOUT)
        except Timeout as e:
            raise Timeout(e)
        except:
            raise BaseException('Something went wrong while making POST request')
        else:
            return (resp.json()['response'])
    else:
        raise BaseException('Unable to make request. No credentials')

def put(api='', data='', ver=''):
    cred = get_query_credentials()

    if cred:
        headers = {"content-type": "application/json", "x-auth-token": cred['ticket']}
        url = "https://" + cred['ip'] + "/api/" + ver + "/" + api

        try:
            resp = requests.put(url, json.dumps(data), headers=headers, verify=False, timeout=DEF_TIMEOUT)
        except Timeout as e:
            raise Timeout(e)
        except:
            raise BaseException('Something went wrong while making POST request')
        else:
            return (resp.json()['response'])
    else:
        raise BaseException('Unable to make request. No credentials')

def delete(api='', params='', ver=''):
    cred = get_query_credentials()

    if cred:
        headers = {"x-auth-token": cred['ticket'], 'content-type': 'application/json'}
        url = "https://" + cred['ip'] + "/api/" + ver + "/" + api

        try:
            resp = requests.delete(url, headers=headers, params=params, verify=False, timeout=DEF_TIMEOUT)
        except Timeout as e:
            raise Timeout(e)
        except:
            raise BaseException('Something went wrong while making POST request')
        else:
            return (resp.json()['response'])
    else:
        raise BaseException('Unable to make request. No credentials')
