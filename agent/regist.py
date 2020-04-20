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

# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import logging
logger = logging.getLogger()

from ._authorize import *

def new_uuid(**kwargs):
    """Write uuid to file name of `uuid.config`
    Call authorize method and set uuid

    Parameters
    ----------
    **kwargs: It must include url, client_type, client_id, client_key, client_secret. 

    Return
    ------
    res['uuid']: str
        uuid
    """
    with open("uuid.config", "wt") as u:
        res = authorize(**kwargs)
        if res["rc"] == 200:
            u.write(res['uuid'])
            return res['uuid']
        else:
            logger.error("Check client config data...")


def regist(**kwargs):
    """Open saved uuid is correct and regist.

    Parameters
    ----------
    **kwargs: It must include url, client_type, client_id, client_key, client_secret. 
    """
    try:
        with open("uuid.config") as u:
            data = u.readlines()
            if len(data) == 0:
                new_uuid(**kwargs)
                return
            uuid = data[0]
            chk_uuid = check_authorize(client_uuid=uuid, **kwargs)
            if chk_uuid["rc"] == 404:
                new_uuid(**kwargs)

    except IOError:
            new_uuid(**kwargs)
