# Copyright 2020 KT AI Lab.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
import requests
import hashlib
import hmac
import datetime
import uuid

kwargs_list = {'host', 'port', 'client_type', 'client_id', 'client_key', 'client_secret', 'service_type', 'client_uuid'}
def chk_kwargs(**kwargs):
    """Check `kwargs` has all nessesary keywards

    Parameters
    ----------
    **kwargs: obj
    """
    inter = kwargs_list.intersection(kwargs.keys())
    if set(kwargs_list) != set(inter):
        raise Exception("Enter proper kwargs. (%s)", kwargs)

def service_url(host, port, service_type, uuid):
    return "{}:{}/v2/serviceLogin/{}/{}".format(host, port, service_type, uuid)

# /v2/authorize 
def logout(**kwargs):
    """Logout 3rd party service

    Parameters
    ----------
    **kwargs: obj

    Return
    ------
    res_json: :obj:`json`
        uuid response requested with `**kwargs`.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = kwargs["client_id"] + ':' + kwargs["client_key"] + ':' + timestamp
    signature = hmac.new(kwargs["client_secret"].encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {
        'x-auth-clienttype': kwargs["client_type"],
        'x-auth-timestamp': timestamp, 
        'x-auth-signature': signature
    }
    
    payload = {
        'login_type':   kwargs["login_type"]
    }
    
    r = requests.delete(
        url=service_url(kwargs["host"], kwargs["port"], kwargs["service_type"], kwargs["client_uuid"]),
        headers=headers,
        data=payload
    )

    res_json = r.json()
    print(res_json)

def login(**kwargs):
    """Logout 3rd party service

    Parameters
    ----------
    **kwargs: obj

    Return
    ------
    res_json: :obj:`json`
        uuid response requested with `**kwargs`.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = kwargs["client_id"] + ':' + kwargs["client_key"] + ':' + timestamp
    signature = hmac.new(kwargs["client_secret"].encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {
        'x-auth-clienttype': kwargs["client_type"],
        'x-auth-timestamp': timestamp, 
        'x-auth-signature': signature
    }
    
    payload = {
        'login_type':   kwargs["login_type"]
    }
    
    r = requests.post(
        url=service_url(kwargs["host"], kwargs["port"], kwargs["service_type"], kwargs["client_uuid"]),
        headers=headers,
        data=payload
    )

    res_json = r.json()
    print(res_json)
