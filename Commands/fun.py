from mainbot.commands import Command

import datetime
import time
import pyfiglet
import os
import shlex

class slap(Command):
    arguments = ["str"]
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "slap"
    
    def on_call(self, event, *args):
        print(args[0])
        self.bot.connection.privmsg(self.bot.channelName,"\001ACTION slapped %s.\001" % args[0])

class asciiClock(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "time"
    
    def on_call(self,event,*args):
        font = pyfiglet.Figlet()
        
        x = font.renderText(str(time.ctime()).split(" ")[4])
        for line in x.split("\n"):
            if line != "":
                self.pubMsg(event,line)
        
class cowsay(Command):
    arguments = ["str"]
    permissionLevel = 0
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callName = "cowsay"
    
    def on_call(self,event,*args):
        y = os.popen("cowsay " + shlex.quote(" ".join(args)))
        for line in y.read().split("\n"):
            self.pubMsg(event,line)


    
                                   
        