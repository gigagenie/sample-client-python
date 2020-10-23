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

kwargs_list = {'host', 'port', 'client_type', 'client_id', 'client_key', 'client_secret'}
def chk_kwargs(**kwargs):
    """Check `kwargs` has all nessesary keywards

    Parameters
    ----------
    **kwargs: obj
    """
    inter = kwargs_list.intersection(kwargs.keys())
    if set(kwargs_list) != set(inter):
        raise Exception("Enter proper kwargs. (%s)", kwargs)


def auth_url(host, port):
    return "{}:{}/v2/authorize".format(host, port)

# /v2/authorize 
def authorize(**kwargs):
    """Authorize client data with post

    Parameters
    ----------
    **kwargs: obj
        It must include post, port, client_type, client_id, client_key, client_secret.
        The ostype and pkgname are optional parameter.

    Return
    ------
    res_json: :obj:`json`
        uuid response requested with `**kwargs`.
    """
    chk_kwargs(**kwargs)
    headers = {
        'x-auth-clienttype': kwargs["client_type"]
    }
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = kwargs["client_id"] + ':' + kwargs["client_key"] + ':' + timestamp
    signature = hmac.new(kwargs["client_secret"].encode(), message.encode(), hashlib.sha256).hexdigest()
    client_userid = hex(uuid.getnode())
    
    payload = {
        'client_key':   kwargs["client_key"],
        'timestamp':    timestamp,
        'signature':    signature,
        'userid':       client_userid,
        'devicemodel':  'python'
    }
    
    r = requests.post(auth_url(kwargs["host"], kwargs["port"]), headers=headers, data=payload)

    res_json = r.json()
    return res_json


def check_authorize(**kwargs):
    """Check uuid with client data

    Paramters
    ---------
    **kwargs: obj
        It must include `host`, `port`, `client_uuid`, `client_id`, `client_key`, `client_secret`, `client_type`.

    Return
    ------
    res_json: :obj:`json`
        Return code and return message.
    """
    chk_kwargs(**kwargs)
    url = "{}/{}".format(auth_url(kwargs["host"], kwargs["port"]), kwargs["client_uuid"])
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = "{}:{}:{}".format(kwargs["client_id"], kwargs["client_key"], timestamp)
    signature = hmac.new(kwargs["client_secret"].encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {
        'x-auth-clienttype': kwargs["client_type"],
        'x-auth-timestamp': timestamp,
        'x-auth-signature': signature
    }
    r = requests.get(url, headers=headers)
    res_json = r.json()
    return res_json
