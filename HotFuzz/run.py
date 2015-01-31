#!/usr/bin/env python3
import main
import threading
import irc.bot
import subprocess
import time
names = open("names").read().split("\n")

channel = "#BANANARAMA"
def makeBot(name):
    print(name)
    y = main.BaseBot(irc.bot.ServerSpec("home.mrmindimplosion.co.uk",6667),channel,name.replace(" ","").replace(".","").replace('"',""))
    x = threading.Thread(target = y.start)
    threads.append(x)
    x.start()
 
 
threads = []
for name in names:
    if name != "" and name[0] != "#":
        makeBot(name)
        time.sleep(5)

# for name in names:
#     subprocess.Popen(["python3","./main.py",name,channel])