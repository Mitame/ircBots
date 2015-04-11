__author__ = 'leviwright'

from mainbot.commands import Command

class NickServLogin(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "login"

    def on_call(self,event,*args):
        self.bot.connection.privmsg("NickServ","identify %s" % self.bot.nickPass)
        for x in self.bot.manOplist:
            self.privMsg(x,"Sent request")
