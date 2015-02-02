#!/usr/bin/env python3
import irc.bot

from conf import settings

def main():
    from mainbot.main import BaseBot
    bot = BaseBot(irc.bot.ServerSpec(settings.host,settings.port),
                    settings.channel,settings.name,settings.callsign,
                    settings.manOplist,settings.chatlog,
                    settings.allowExclaimCommand,settings.textPrefix,
                    settings.textPostfix)
    
    import mainbot.commands as commands
    commands.ping(bot)
    commands.die(bot)
    commands.cnJoke(bot)
    commands.vote(bot)
    commands.help(bot)
    commands.flushLog(bot)
    commands.say(bot)
    commands.op(bot)
   
    import games.textAdv
    games.textAdv.cca(bot)
    
    bot.start()

if __name__ == "__main__":
    main()
