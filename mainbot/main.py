#!/usr/bin/env python3
import irc.bot
import irc
from socket import gethostbyname
    
class BaseBot(irc.bot.SingleServerIRCBot):
    def __init__(self,serverspec,channel,nickname,callsign,manOplist,chatlog,allowExclaim,textPrefix,textPostfix):
        serverspec.host = gethostbyname(serverspec.host)
        nickname = nickname
        irc.bot.SingleServerIRCBot.__init__(self, [serverspec], nickname, nickname)
        self.channelName = channel
        self.commands = {}
        
        self.callsign = callsign
        self.manOplist = manOplist
        self.chatlog = chatlog
        self.allowExclaimCommand = allowExclaim
        self.textPrefix = textPrefix
        self.textPostfix = textPostfix
        
    def die(self,event, msg="Bye, cruel world!"):
        try:
            for x in self.commands.keys():
                self.commands[x].on_die(event)
        except:
            pass
        irc.bot.SingleServerIRCBot.die(self, msg=msg)
        
    def isPermitted(self,event):
        return event.source.nick in self.manOplist
    
    def isOp(self,event):
        return self.channels[self.channelName].is_oper(event.source.nick)
    
    def getPermLevel(self,event):
        if event.source.nick in self.manOplist:
            return 3
        elif self.channels[self.channelName].is_oper(event.source.nick):
            return 2
        elif self.channels[self.channelName].is_halfop(event.source.nick):
            return 1
        else:
            return 0
    def on_nicknameinuse(self,c,event):
        c.nick(c.get_nickname()+ "_")
        
    def on_welcome(self,c,event):
        c.join(self.channelName)
    
    def on_privmsg(self,c,event):
        self.do_command(event,event.arguments[0])
    
    def on_pubmsg(self,c,event):
        if event.arguments[0] == "": return
        try:
            self.chatlog.write(("<%s>: " % event.source.nick)+event.arguments[0]+"\n")
        except NameError:
            pass
        
        a = event.arguments[0].split(":", 1)
        if len(a) > 1 and a[0].lower() == self.callsign:
            self.do_command(event,a[1].strip())
        
        if self.allowExclaimCommand:
            if event.arguments[0].strip()[0] == "!":
                if event.arguments[0].split(" ")[0][1:] in self.commands.keys():
                    self.do_command(event, event.arguments[0].strip()[1:])
        
        
        return
    
    def sendMsg(self,event,msg):
        self.connection.privmsg(self.channelName, msg)
    
    def sendPubMsg(self,event,message):
        self.connection.privmsg(self.channelName, message)

    def on_dccmsg(self,c,event):
        c.privmsg("You said: "+ event.arguments[0])
    
    def on_dccchat(self, c, event):
        if len(event.arguments) != 2:
            return
        args = event.arguments[1].split()
        if len(args) == 4:
            try:
                address = irc.client.ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)
    
    def do_command(self,event,cmd):
        args = cmd.split(" ")[1:]
        cmd = cmd.split(" ")[0]
        if cmd.lower() in self.commands.keys():
            cmdclass = self.commands[cmd.lower()]
            if cmdclass.permissionLevel == -1:
                if not cmdclass.checkPermissions(event,*args):
                    return
            else:
                if self.getPermLevel(event) < cmdclass.permissionLevel:
                    self.connection.notice(event.source.nick, "This command requires elevated privilages, which you do not possess. Level %s privilages are required." % str(cmdclass.permissionLevel))
                    return
                    
            
            if not cmdclass.manArgCheck:
                if not (len(args) == len(cmdclass.arguments) or (len(args) >= len(cmdclass.arguments) and cmdclass.permitExtraArgs)):
                    self.connection.notice(event.source.nick, "This command requires %s arguments" % str(len(cmdclass.arguments)))
                    return
                
                for x in range(len(cmdclass.arguments)):
                    if cmdclass.arguments[x] == "int":
                        if not (args[x].isdecimal() or "." in args[x]):
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x] 
                        else:
                            args[x] = int(args[x])
                        
                    elif cmdclass.arguments[x] == "float":
                        if not (args[x].isdecimal()):
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x]
                        else:
                            args[x] = float(args[x])
                    elif cmdclass.arguments[x] == "str":
                        if len(cmdclass.defaultArgs) > x:
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x]
            else:
                if cmdclass.checkArgs(event,*args):
                    pass
                else:
                    return 
            cmdclass.on_call(event,*args)
        else:
            self.connection.notice(event.source.nick,"%s is not a valid command." % cmd)
