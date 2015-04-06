MMI-Bot Base and Test Bots for IRC
==================================

These are some testbots for IRC servers.
They are easily configurable and should be easy to make new commands for.
Written in python.



Dependencies
------------
####For everything:
[IRC for python](https://pypi.python.org/pypi/irc)

####For Commands/fun (These can be disabled)
[pyfiglet](https://pypi.python.org/pypi/pyfiglet) for generating ascii clocks in ```asciiClock()``` command.

[cowsay](http://en.wikipedia.org/wiki/Cowsay) for generating cowsay ascii art in ```cowsay()``` command.

[pexpect](http://pexpect.sourceforge.net/pexpect.html) and [adventure](http://en.wikipedia.org/wiki/Colossal_Cave_Adventure) for ```cca()``` command.



Running a bot
-------------
1. Copy defaultconf.py to conf.py and edit it to your liking.
2. Copy mainbot.py and edit to your liking. Comment out lines to remove commands.

Creating commands
-----------------
To create commands, create a new class which inherits `mainbot.commands.Command`
```python
from mainbot.commands import Command

class newCommand(Command):
    pass
```
Next, set the variables for the command that the bot reads when calling it to check parameters.
```python
class newCommand(Command):
    arguments = ["str"]
        permissionLevel = 3
        permitExtraArgs = False
        manArgCheck = False
        defaultArgs = []
        callName = "new"
```
When a command is recieved and is allowed to be executed, ```Commands.on_call(self,event,*args)``` is called for the command. Add a class method to recieve this.

```python
class newCommand(Command):
    argu...

    def on_call(self,event,*args):
        "do stuff"
```

The bot will receive messages from both the channel it has joined and private messages. Use ```self.pubMsg(event,message)``` and ```self.privMsg(event,message)``` to send channel and private messages, respectively.
