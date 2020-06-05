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

# gRPC
import grpc
from proto import gigagenieM_pb2
import agent
import agent.grpc_channel as grpc_channel
from agent._player import *
from agent._audio import *

import json
import logging
import threading

logger = logging.getLogger()
ttsplayer = WavePlayer()
mediaplayer = VlcMediaPlayer()
mediaplayer.start()
time.sleep(0.5)

serviceflag = threading.Event()
"""To handle command one at a time"""
gen_event = threading.Event()
"""To check request event. If request is handle, gen_event wait to be 1."""
ready_event = threading.Event()
ttsplayStatus = 0

message = gigagenieM_pb2.reqM()
g_msgType = ''
g_msgPayload = ''
dev_dssStatus = {'SU:016', 'SU:027', 'SI:002', 'SG:000'} # initial status: laucher main, hdmi connected, remote voice input, nobody here
sendVoiceFlag = False


def mic_off_ready():
    global sendVoiceFlag
    sendVoiceFlag = False
    gen_event.clear()
    ready_event.set()


def mic_on():
    global sendVoiceFlag
    sendVoiceFlag = True
    gen_event.set()
    t = threading.Timer(5.0, mic_off_ready)
    t.start()


# -------------- media ------------ #
def media_end_callback(event):
    """Set message for grpc request and off the mic.

    This is callback function for `VlcMediaPlayer.set_end_callback`.
    
    Parameters
    ----------
    event: :obj
        Recieve from VlcMediaPlayer end event
    """
    logger.debug('End of media stream (event %s)' % event.type)

    if mediaplayer.get_state() != 0:
        msgType = 'Upd_MEST'
        channel = mediaplayer.get_channel()
        duration = mediaplayer.get_duration() / 1000
        msgPayload = json.dumps({'cmdOpt':{'channel':channel, 'status': 'complete', 'playTime': duration}})
        sendMessage(msgType, msgPayload)
        mic_off_ready()


def change_media_process(act):
    """Change vlc media player state.

    Check the current state with `mediaplayer.get_state()` and compare it with `act` and then changing the mediaplayer status.

    `mediaplayer.get_state().value` is {0: 'NothingSpecial', 1: 'Opening', 2: 'Buffering', 3: 'Playing', 4: 'Paused', 5: 'Stopped', 6: 'Ended', 7: 'Error'}

    Parameters
    ----------
    act: str
    """
    state = mediaplayer.get_state().value 
    logger.debug(mediaplayer.get_state())
    if act == "pause" and state == 3: # stop
        logger.info('ACTION >>> Media Pause')
        mediaplayer.pause()
    elif act == "resume" and state in [4, 5]: # playing
        logger.info('ACTION >>> Media Resume')
        msgType = 'Upd_MEST'
        msgPayload = json.dumps({'cmdOpt':{'channel':mediaplayer.get_channel(),'status':act,'playTime':0}})
        sendMessage(msgType, msgPayload)
        mediaplayer.play()
    elif act == "stop":
        logger.info('ACTION >>> Media Stop')
        #dss_state_update(option):
        mediaplayer.stop()


def processMediaPlay(msgPayloadJson):
    """Play wave file or media from url

    If `msgPayloadJson` does not include `url`, set `ttsplayStatus` to playing state.
    Or, play the media from `url`.  

    Parameters
    ----------
    msgPayloadJson: :obj:`str`
        Json data from grpc response.
    """
    global ttsplayStatus

    playOptions = msgPayloadJson['cmdOpt']
    dss_state_update(playOptions)

    playUrl = playOptions.get('url') 
    meta_info = playOptions.get('metaInfo', None)
    if meta_info:
        tts_text = meta_info.get('mesg', '')
        logger.info('TTS_TEXT: %s' % tts_text)
        print('TTS_TEXT: %s' % tts_text)
    if playUrl == None:  # media(tts) type is audio data(wave)
        change_media_process(playOptions['actOnOther'])
        logger.info('ACTION >>> TTS Play')
        ttsplayStatus = 1
        # audio data from server through 'voice' field
        # - SEE ALSO grpc_request()
    else: # media type is url
        change_media_process(playOptions['actOnOther'])
        channelReceived = playOptions['channel']
        
        msgType = 'Upd_MEST'
        msgPayload = json.dumps({'cmdOpt':{'channel':channelReceived,'status':'started','playTime':0}})
        sendMessage(msgType, msgPayload)
        logger.info('Play Media Url: '+playUrl)
        mediaplayer.play(playUrl, channelReceived, meta_info)
        mediaplayer.set_end_callback(media_end_callback)
        # to stop generator of grpc requests
        gen_event.clear()
# ---------------------------------- #


# --------------- TTS -------------- #
def ttsplay(fname):
    """Play wave file and set message for grpc request.

    Play the file with wave player is to enhance the playing speed.

    Parameters
    ----------
    fname:  str
        file name to play
    """
    global ttsplayStatus
    # play
    msgType = 'Upd_MEST'
    msgPayload = json.dumps({'cmdOpt':{'channel':0, 'status': 'started', 'playTime': 0}})
    sendMessage(msgType, msgPayload)
    duration = ttsplayer.play(fname) / 1000 # msec to sec
    # end
    os.remove(fname)
    msgPayload = json.dumps({'cmdOpt':{'channel':0, 'status': 'complete', 'playTime': duration}})
    sendMessage(msgType, msgPayload)

    ttsplayStatus = 0
    time.sleep(0.2)
    mic_off_ready()
# ---------------------------------- #


# -------- response handling ------- #
def dss_state_update(option):
    """Upload device state to server.

    Parameters
    ----------
    option: :obj: `dict`
        dssStatus data
    """
    global dev_dssStatus
    if 'setDssStatus' in option:
        for k in option['setDssStatus']:
            dev_dssStatus.add(k)

    if 'clearDssStatus' in option:
        for k in list(option['clearDssStatus']):
            dev_dssStatus.discard(k)

    msgType = 'Upd_DSST'
    msgPayload = json.dumps({'cmdOpt':{}, 'dssStatus':list(dev_dssStatus)})
    sendMessage(msgType, msgPayload)


def sendMessage(msgType='', msgPayload=''):
    """Change `get_event` to 1 (set) to send grpc message

    Paramters
    ---------
    msgType: str
        command name of grpc message
    msgPayload: str(json)
        command parameter of grpc message
    """
    global g_msgType
    global g_msgPayload

    g_msgType = msgType
    g_msgPayload = msgPayload
    if msgType != '':
        gen_event.set()


def _generate_request():
    """Set data to grpc message

    Yield
    -----
    message: obj
        grpc message
    """
    while True:
        gen_event.wait()
        if sendVoiceFlag is True: # mic on
            logger.info("START of send voice")
            with MicrophoneStream(RATE, CHUNK) as stream:
                audio_generator = stream.generator()
                print('mic on')
                for content in audio_generator:
                    message.voice = content
                    yield message
                    if sendVoiceFlag is False:
                        gen_event.clear()
                        break
            logger.info("END of send voice")
        else: # command handling
            message.devCommand.msgType = g_msgType
            if g_msgType == 'Req_VOCM':  # voice command
                message.devCommand.msgPayload = json.dumps({'cmdOpt': {}, 'dssStatus': list(dev_dssStatus)})
            elif g_msgType == 'Req_TXCM':  # text command
                message.devCommand.msgPayload = json.dumps(g_msgPayload)
            elif g_msgType in ['Upd_DSST', 'Upd_MEST']:
                message.devCommand.msgPayload = g_msgPayload
            logger.debug(g_msgType + ' : ' + message.devCommand.msgPayload)
            yield message
            gen_event.clear()
# ---------------------------------- #


# -------- response handling ------- #
def processNextCmd(msgPayloadJson):
    """Call next command which is in the `msgpayloadJson`

    Parameters
    ----------
    msgPayloadJson: :obj:`json`
    """
    nextCmd = msgPayloadJson['nextCmd'] if 'nextCmd' in msgPayloadJson else ''
    nextCmdOpt = msgPayloadJson['nextCmdOpt'] if 'nextCmdOpt' in msgPayloadJson else ''

    if nextCmd == 'Req_STRV':
        mic_on()
    elif nextCmd == 'Req_PLMD':
        processMediaPlay({'cmdOpt':nextCmdOpt})


def doServerCommand_Snd_SVEV(msgPayloadJson):
    """Set server event command
    
    Parameters
    ----------
    msgPayloadJson: :obj:`json`
    """
    logger.debug('Snd_SVEV')
    cmdOptions = msgPayloadJson['cmdOpt']
    ev_type = cmdOptions['type']
    if ev_type == 'servDisc':   # Server Disconnect
        logger.debug('Server Disconnection')
        grpc_channel.grpc_disconn()


def grpc_request(): 
    """Handle the responses and send request to `grpc_channel`.
    Open grpc channel with `grpc_channel.grpc_conn()` and handle the response message by each command type.
    """
    global sendVoiceFlag
    global ttsplayStatus
    
    logger.info("START: grpc_request()")
    stub = grpc_channel.grpc_conn()
    metadata = (('x-client-version', 'python-client/%s' % agent.__version__), )
    requests = stub.serviceM(_generate_request(), metadata = metadata)

    for responses in requests:
        """
        TODO: exception handling RPC.call
            except grpc.RpcError as rpc_error_call:
                err_code = rpc_error_call.code()
                err_details = rpc_error_call.details()
        """
        if responses.HasField("srvCommand"):
            mType = responses.srvCommand.msgType
            mPayload = responses.srvCommand.msgPayload
            mPayloadJson = json.loads(mPayload)
            logger.debug('srvCommand:msgType='+mType+', msgPayload='+mPayload)
            if mType == 'Res_VOCM':
                if mPayloadJson['rc'] == 200:
                    processNextCmd(mPayloadJson)
            elif mType == 'Req_STRV':
                sendVoiceFlag = True
                gen_event.set()
                logger.info('ACTION >>> Send Voice Stream')
            elif mType == 'Req_STPV':
                sendVoiceFlag = False
                gen_event.clear()
                if 'cmdOpt' in mPayloadJson and 'uword' in mPayloadJson['cmdOpt']:
                    stt_text = mPayloadJson['cmdOpt']['uword']
                    if stt_text is None: # null
                        stt_text = ''
                else:
                    stt_text = ''
                logger.info('STT_TEXT: %s' % stt_text)
                print('STT_TEXT: %s' % stt_text)
                processNextCmd(mPayloadJson)
            elif mType == 'Req_PLMD':
                processMediaPlay(mPayloadJson)
            elif mType == 'Req_UPMD':
                dss_state_update(mPayloadJson['cmdOpt'])
                cmdOptions = mPayloadJson['cmdOpt']
                change_media_process(cmdOptions['act'])
            elif mType == 'Req_UPDS':
                dss_state_update(mPayloadJson['cmdOpt'])
            elif mType == 'Snd_SVEV':
                doServerCommand_Snd_SVEV(mPayloadJson)
        elif responses.HasField("voice"): # Response of voice
            if ttsplayStatus == 1:
                ttsplayStatus = 2
                fname = './tmp.wav'
                writeFile = open(fname, 'wb')
                writeFile.write(responses.voice)
                writeFile.close()
                ttsplay(fname)
        else: # error
            logger.error("ERROR: gRPC call - UNKNOWN RESPONSE")
            break
    logger.info("END of grpc_request()")
# ----------------------------- #


def service_start():
    """Connect grpc service
    """
    while True:
        try:
            logger.debug('wait until triggered')
            # wait until service-request triggered(eg. kws detected)
            serviceflag.wait()
            logger.debug('service starting...')
            grpc_request()
            serviceflag.clear()
        except grpc.RpcError as rpc_error:
            logger.debug('gRPC ERROR')
            if rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logger.debug('The service is currently unavailable.')
            elif rpc_error.code() == grpc.StatusCode.CANCELLED:
                logger.debug('Channel closed!')
            elif rpc_error.code() == grpc.StatusCode.UNKNOWN:
                logger.debug('write after end')
            else:
                raise rpc_error
            serviceflag.clear()
            mic_off_ready()
        except Exception as e:
            logger.error('Error: ' + str(e))
        else:
            logger.error('UNKNOWN ERROR. retry grpc service.')


# -------- main thread -------- #
grpcThread = threading.Thread()


def start_grpc_thread():
    """Make and start thread with `service_start` method
    """
    global grpcThread
    grpcThread = threading.Thread(target=service_start)
    grpcThread.daemon = True
    grpcThread.start()
# ----------------------------- #


# -------- main command ------- #
def command(request_text=''):
    """Handle the command
        It start thread and set the flags and handle the start command.

    Parameters
    ----------
    request_text: str
    """
    global sendVoiceFlag
    if not grpcThread.is_alive():
        start_grpc_thread()
    # gRPC connection & reqeust-ready
    serviceflag.set()
    ready_event.clear()

    if sendVoiceFlag is True:
        sendVoiceFlag = False
        gen_event.clear()
        ready_event.set()
        return
    logger.info("ACTION >>> START COMMAND")
    if ttsplayStatus == 2:
        print("Please command after TTS...")
    change_media_process("pause")

    if request_text == "":
        msgType = 'Req_VOCM'
        msgPayload = json.dumps({'cmdOpt': {}, 'dssStatus': list(dev_dssStatus)})
        logger.debug('END of voicecommand()')
    else:
        msgType = 'Req_TXCM'
        msgPayload = {'cmdOpt': {'cmdType': 'query', 'text': request_text}, 'dssStatus': list(dev_dssStatus)}
        logger.debug('END of textcommand()')

    sendMessage(msgType, msgPayload)
# ----------------------------- #
