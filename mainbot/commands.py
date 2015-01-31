#!/usr/bin/env python3

class Command():
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = ""
    
    def __init__(self,bot):
        self.bot = bot
        bot.commands[self.callname] = self
    
    def on_call(self,event,*args):
        self.bot.do_command("help "+" ".join(args))
    
    def on_fail(self,event):
        self.notify(event.source.nick,\
        "The command must follow the syntax: /%s "% self.callname+" "+str(self.arguments))
    
    def checkPermissions(self,event,*args):
        pass
    
    def checkArgs(self,event,*args):
        pass
    
    def privMsg(self,event,msg):
        self.bot.connection.notice(event.source.nick,msg)
    
    def on_die(self,event):
        pass
    
    def pubMsg(self,event,msg):
        self.bot.sendPubMsg(event,msg)
        
        
class ping(Command):
    arguments = []
    permissionLevel = 2
    permitExtraArgs = False
    callname = "ping"
    defaultArgs = []
    
    def on_call(self,event,*args):
        self.privMsg(event,"PONG")
    
          
class die(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    callname = "die"
    defaultArgs = []
    
    def on_call(self,event,*args):
        self.bot.die(event, " ".join(args))


class cnJoke(Command):
    arguemnts = []
    permissionLevel = 0
    permitExtraArgs = False
    callname = "cnjoke"
    defaultArgs = []
    
    def __init__(self,*args,**kwargs):
        Command.__init__(self,*args,**kwargs)
        global json, urllib
        import json
        import urllib.request

    def on_call(self,event,*args):
        x = urllib.request.urlopen("http://api.icndb.com/jokes/random")
        z = str(x.read(),"utf8")
        try:
            a = json.loads(z)
            self.bot.sendMsg(event, a["value"]["joke"])
        except ValueError:
            print(z)
    
    def on_fail(self,event):
        self.notify(event.source.nick,\
        "You failed to type the command correctly puny human. \nChuck Norris will roundhouse kick you in the face shortly."% self.callname+" "+str(self.arguments))


class vote(Command):
    arguments = ["str","str"]
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = True
    defaultArgs = []
    callname = "vote"
    
    class poll():
        def __init__(self,*args):
            self.votes = {}
            self.voteids = {}
            self.voted = []
            for vote in args:
                self.votes[vote] = 0
                self.voteids[args.index(vote)] = vote
        def getVote(self,id,data="name"):
            if data == "name":
                return self.voteids[id]
            elif data == "score":
                return self.votes[self.voteids[id]]
            
    def __init__(self,bot):
        Command.__init__(self, bot)
        self.polls = {}
        self.pollids = {}
        self.currentPoll = ""
    
    
        
    def createPoll(self,event,name,question,*options):
        self.currentPoll = name
        self.polls[name] = self.poll(*options)
        self.polls[len(self.polls.keys())] = name
        self.pubMsg(event,"""%s has started a poll!""" % event.source.nick)
        self.pubMsg(event,"---%s---" % question)
        
        for x in range(len(self.polls[name].voteids)):
            self.pubMsg(event,str(x)+" :\t"+self.polls[name].getVote(x))
        
        self.pubMsg(event,"To vote, type in '%s:vote #', where '#' is your vote." % self.bot.callsign)
        self.pubMsg(event,"---Note, you can't change your mind after you have voted, so think carefully.")
    
    def castVote(self,event,*args):
        if self.currentPoll == "":
            self.bot.sendPubMsg(event,"Sorry %s, there is not vote running currently." % event.source.nick)
            return
        
        curpoll = self.polls[self.currentPoll]
        if event.source.nick in curpoll.voted:
            self.bot.sendPubMsg(event,"Sorry %s, you can't vote again." % event.source.nick)
            return
        
        curpoll = self.polls[self.currentPoll]
        curpoll.votes[curpoll.voteids[int(args[0])]] += 1
        alert = ("%s voted for '" +self.polls[self.currentPoll].voteids[int(args[0])]+"'!")%event.source.nick

        curpoll.voted.append(event.source.nick)
        self.bot.sendPubMsg(event,alert)
        
    def checkPermissions(self, event, *args):
        if len(args) == 0:
            return True
        base = args[0]
        if base in ("create","results","close"):
            if self.bot.getPermLevel(event) >= 1:
                return True
            else:
                return False
        else:
            if base.isdecimal() and (0<=int(base)<len(self.polls[self.currentPoll].voteids)):
                return True
            else:
                return False
    
    def checkArgs(self, event, *args):
        if len(args) == 0:
            return 0
        return True
    
    def getResults(self,event,*args):
        if self.currentPoll == "":
            self.bot.sendPubMsg(event,"Sorry %s, there is not vote running currently." % event.source.nick)
            return
        
        self.bot.sendPubMsg(event,"---Current poll results---")
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            
            self.bot.sendPubMsg(event,("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x )
        self.bot.sendPubMsg(event,"--------------------------")
    
    def closePoll(self,event,name):        
        self.pubMsg(event, "The voting has now ended. The final results are:")
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            
            self.bot.sendPubMsg(event,("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x )
        self.bot.sendPubMsg(event,"--------------------------")
        
        self.currentPoll = ""
        
    def on_call(self, event, *args):
        print(args)
        if args[0] == "create":
            args = " ".join(args[1:]).split(", ")
            self.createPoll(event,args[0],args[1],*args[2:])
        elif args[0] == "results":
            self.getResults(event)
        elif args[0] == "close":
            try:
                self.closePoll(event,self.currentPoll)
            except NameError:
                self.pubMsg("No poll to close.")
        else:
            if args[0].isdecimal():
                self.castVote(event,int(args[0]))


class help(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "help"
    
    def on_call(self,event,*args):
        commands = []
        print(self.bot.commands)
        for x in list(self.bot.commands.items()):
            print(x)
            if x[1].permissionLevel <= self.bot.getPermLevel(event):
                commands.append(x[0])
        
        commands.sort()
        self.privMsg(event,"---Commands avaliable to you---")
        for cmd in commands:
            self.privMsg(event,self.bot.callsign+":"+cmd)
        self.privMsg(event,"-------------------------------")

       
class flushLog(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "flushlog"  
    
    def on_call(self, event, *args):
        self.bot.logfile.flush()


class say(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callname = "say"
    
    def on_call(self, event, *args):
        self.bot.sendPubMsg(event," ".join(args))

class op(Command):
    arguments = ["str"]
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "op"
    
    def on_call(self, event, *args):
        print(args[0])
        self.bot.connection.mode("#BANANARAMA","+o %s" % args[0])

class deop(Command):
    arguments = ["str"]
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "deop"
    
    def on_call(self, event, *args):
        print(args[0])
        self.bot.connection.mode("#BANANARAMA","-o %s" % args[0])
            
        