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
#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Client for GiGA Genie Inside"""

from __future__ import print_function
from __future__ import absolute_import

import logging
import time

import agent

import sys
def get_input(text=''):
    if sys.version_info.major >= 3:
        return input(text)
    else:
        return raw_input(text)

logging.basicConfig(
    filename='run.log',
    level=logging.DEBUG,
    format="[%(asctime)s](%(filename)s:%(lineno)s)::%(levelname)s:%(message)s"
)
def main():
    """main method"""
    agent.regist(
        host = agent.REST_HOST,
        port = agent.REST_PORT,
        client_type = agent.CLIENT_TYPE,
        client_id = agent.CLIENT_ID, 
        client_key = agent.CLIENT_KEY, 
        client_secret = agent.CLIENT_SECRET
    )
    print ('GiGA Genie INSIDE Python Client v%s' % agent.__version__)
    print (agent.__copyright__)
    print ("\nEnter key to start voice mode or Input text to start text mode... \nPress Ctrl+C to quit...")
    while True:
        try:
            input_key = get_input("\nENTER(or input text & ENTER): ")
            agent.command(input_key)
            agent.ready_event.wait()
        except KeyboardInterrupt:
            print ('Bye bye!')
            break

if __name__ == '__main__':
    main()
