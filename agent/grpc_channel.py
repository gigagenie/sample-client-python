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

import logging
from proto import gigagenieM_pb2_grpc
import datetime
import hmac
import hashlib
from ._config import *
import grpc

# Config for GiGA Genie gRPC : config.read('agent.config')
CLIENT_TYPE = config.get('client', 'client_type')
CLIENT_ID = config.get('client', 'client_id')
CLIENT_KEY = config.get('client', 'client_key')
CLIENT_SECRET = config.get('client', 'client_secret')
CLIENT_UUID = ''

HOST = config.get('grpc', 'host')
PORT = int(config.get('grpc', 'port'))

REST_HOST = config.get('rest', 'host')
REST_PORT = config.get('rest', 'port')
PKGNAME = ''

logger = logging.getLogger()

### COMMON : Client Credentials ###
def set_uuid(filename):
    global CLIENT_UUID
    with open(filename) as f:
        try:
            CLIENT_UUID = f.read()
        except FileNotFoundError:
            logger.error("No uuid.config file...")


def getMetadata():
    set_uuid("uuid.config")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + CLIENT_KEY + ':' + timestamp

    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    metadata = [('x-auth-clienttype', CLIENT_TYPE),
                ('x-auth-clientuuid', CLIENT_UUID),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]

    return metadata


def credentials(context, callback):
    callback(getMetadata(), None)


def getCredentials():
    sslCred = grpc.ssl_channel_credentials()
    authCred = grpc.metadata_call_credentials(credentials)
    return grpc.composite_channel_credentials(sslCred, authCred)
###

# gRPC channel

g_channel = None
g_stub = None


def log_connectivity_changes(connectivity):
    logger.debug("Channel changed status to %s." % connectivity)


def grpc_conn():
    global g_channel
    global g_stub

    if g_channel is None:
        g_channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
        g_channel.subscribe(log_connectivity_changes)
    if g_stub is None:
        g_stub = gigagenieM_pb2_grpc.GigagenieMStub(g_channel)

    return g_stub


def grpc_disconn():
    global g_channel
    global g_stub

    if g_channel is not None:
        g_channel.unsubscribe(log_connectivity_changes)
        g_channel.close()
    g_channel = None
    g_stub = None

###
