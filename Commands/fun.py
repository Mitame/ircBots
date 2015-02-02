from mainbot.commands import Command

import datetime
import time
import urllib.request
import urllib.parse
import json
import pyfiglet

class slap(Command):
    arguments = ["str"]
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "slap"
    
    def on_call(self, event, *args):
        print(args[0])
        self.bot.connection.privmsg(self.bot.channelName,"\001ACTION slapped %s.\001" % args[0])

class asciiClock(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "time"
    
    def on_call(self,event,*args):
        font = pyfiglet.Figlet()
        
        x = font.renderText(str(time.ctime()).split(" ")[4])
        for line in x.split("\n"):
            if line != "":
                self.pubMsg(event,line)
        
                                   
        