#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import send_file
from flask import redirect
from flask import make_response

from multiprocessing import Process

import os
import json
from datetime import datetime

class APIhttp(object):
    """Twitch API with signal emitters for bits, subs, and point redeems

    Manages authentication and creating messages from API events to     use elsewhere
    """

    def __init__(self,key_path=None,log=False):
        """Init with file path"""
        self.service_name = "HTTP"

        self.app = Flask("The Web: Now with 100% More OOP")

        # Define routes in class to use with flask
        self.app.add_url_rule('/','home', self.index)
        self.app.add_url_rule('/dev/gpib_data.json','3478a-0', self.dev_3478a_0)
        self.app.add_url_rule('/window/','window', self.window)
        self.app.add_url_rule('/window/window.css','window-css', self.windowCss)
        self.app.add_url_rule('/window/window.js','window-js', self.windowJs)

        # Set headers for server
        self.app.after_request(self.add_header)

        self.host = "0.0.0.0"

        

    def set_host(self,host_ip):
        self.host = host_ip

    def add_header(self,r):
        """
        Force the page cache to be reloaded each time
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    async def connect(self):
        """ Run Flask in a process thread that is non-blocking """
        print("Starting Flask")
        self.web_thread = Process(target=self.app.run, kwargs={"host":self.host,"port":5001})
        self.web_thread.start()

    def disconnect(self):
        """ Send SIGKILL and join thread to end Flask server """
        self.web_thread.terminate()
        self.web_thread.join()

    def index(self):
        """ Simple class function to send HTML to browser """
        return """
<a href="/dev/gpib_data.json"><h2>DMM</h2></a>
<a href="/window/"><h2>Window</h2></a>
        """

    def window(self):
        """ Simple class function to send HTML to browser """
        return send_file("http/window.html")

    def windowCss(self):
        """ Simple class function to send HTML to browser """
        return send_file("http/window.css")

    def windowJs(self):
        """ Simple class function to send HTML to browser """
        return send_file("http/window.js")



    def dev_3478a_0(self):
        """ Simple class function to send JSON to browser """
        return send_file("/tmp/gpib_data.json")
