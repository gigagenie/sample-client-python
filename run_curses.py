#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""Simple Client for GiGA Genie Inside"""
import sys,os
import curses
import locale
locale.setlocale(locale.LC_ALL, '')

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

import logging
import time
import threading
import json

import agent

VERSION = agent.__version__

logging.basicConfig(
    filename='run.log',
    level=logging.DEBUG,
    format="[%(asctime)s](%(filename)s:%(lineno)s)::%(levelname)s:%(message)s"
)

logger = logging.getLogger()

guide_text = 'ready'

def start_command():
    global guide_text

    agent.command("")
    agent.ready_event.wait()
    guide_text = 'ready'

def draw_screen(stdscr):
    global guide_text
    
    infoDetail = None

    curses.initscr()
    curses.halfdelay(10)
    curses.noecho()

    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN or k == ord('j'):
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP or k == ord('k'):
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT or k == ord('l'):
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT or k == ord('h'):
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "G-INSIDE Sample Client"[:width-1]
        subtitle = "copyright (c) 2018-2020 kt corp."[:width-1]
        verstr = "Version {}".format(VERSION)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {} | Keycode: {}"[:width-1].format(cursor_x, cursor_y, k)
        guidestr = "To start, press SPACE key..."[:width-1]
        
        if k == 32:
            guide_text = 'Listening ...'
            threading.Thread(target = start_command).start()

        if agent.get_sendVoiceFlag() is True:
            guide_text = 'Listening ...'
        else:
            guide_text = 'ready'

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_verstr = int((width // 2) - (len(verstr) // 2) - len(verstr) % 2)
        #start_y = int((height // 2) - 2)
        start_y = 0

        # Rendering some text
        #whstr = "Width: {}, Height: {}".format(width, height)
        #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 3, start_x_verstr, verstr)
        stdscr.addstr(start_y + 5, 0, guidestr, curses.color_pair(1))
        stdscr.addstr(start_y + 6, 0, guide_text, curses.color_pair(1))

        # get stt_text, tts_text, metainfo from agent/service.py
        stt_text = agent.get_g_stt_text()
        tts_text = agent.get_g_tts_text()
        metainfo = agent.get_meta_info()
        #logger.debug("METAINFO JSON\n"+json.dumps(agent.get_meta_info()))

        if metainfo is not None and 'infoDetail' in metainfo:
            infoDetail = metainfo['infoDetail']
        if infoDetail is not None:
            stdscr.attron(curses.color_pair(4))

            try:
                title = infoDetail['title']
            except:
                title = ''
            try:
                artist = infoDetail['artist']
            except:
                artist = ''

            m_info1 = "{}".format(title)[:width-1]
            stdscr.addstr(start_y + 7, 0, 'Now playing: ' + m_info1)
            if artist != '':
                m_info2 = "{}".format(artist)[:width-1]
                stdscr.addstr(start_y + 8, 13, m_info2)

            stdscr.attroff(curses.color_pair(4))

        stdscr.addstr(start_y + 10, 0, "You:   %s" % stt_text)
        stdscr.addstr(start_y + 12, 0, "Genie: %s" % tts_text)
        stdscr.addstr(start_y + 15, 0, '')
        stdscr.refresh()
        #stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    agent.regist(
        host = agent.REST_HOST,
        port = agent.REST_PORT,
        client_type = agent.CLIENT_TYPE,
        client_id = agent.CLIENT_ID, 
        client_key = agent.CLIENT_KEY, 
        client_secret = agent.CLIENT_SECRET
    )
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()
