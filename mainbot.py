#!/usr/bin/env python3
import irc.bot

from conf import settings

def main():
    from mainbot.main import BaseBot
    bot = BaseBot(irc.bot.ServerSpec(settings.host,settings.port,settings.servPass),
                    settings.channel,settings.name,settings.callSign,
                    settings.manOpList,settings.chatLog,
                    settings.commandPrefix,settings.textPrefix,
                    settings.textPostfix,settings.textReplacements,settings.nickPass,settings.nickServ)
    
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

    import Commands.fun
    Commands.fun.asciiClock(bot)
    Commands.fun.cowsay(bot)
    Commands.fun.slap(bot)

    import mainbot.textReaders
    mainbot.textReaders.youTubeScanner(bot,open("youtube.apikey","r").read().strip())

    mainbot.textReaders.imgurScanner(bot,*open("imgur.apikey").read().strip().split("\n"))

    bot.start()

if __name__ == "__main__":
    main()
