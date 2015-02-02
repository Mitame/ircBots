from mainbot.commands import Command

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