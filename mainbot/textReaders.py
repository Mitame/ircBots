import re
from googleapiclient.discovery import build
import urllib.request
import imgurpython
import time

class TextReader():
    regExp = ".*"


    def __init__(self,bot):
        if type(self) == TextReader:
            #raise RuntimeWarning ("You should not be loading the main TextReader class.")
            print("You should not be loading the main TextReader class.")


        self.bot = bot
        self.re = re.compile(self.regExp)
        self.bot.registerTextReader(self)


    def on_call(self,event,positions):
        print("TextReader '%s' has not been configured to do anything when called." % type(self))

    def privMsg(self,event,msg):
            if type(event) == str:
                self.bot.connection.notice(event,msg)
            else:
                self.bot.connection.notice(event.source.nick,msg)

    def pubMsg(self,event,msg):
        self.bot.sendPubMsg(event,msg)



class youTubeScanner(TextReader):
    regExp = "(?<=youtube.com/watch\?v=)[^&]*" #https://www.youtube.com/watch?v=pho9v2hMeng

    def __init__(self,bot,key):
        TextReader.__init__(self,bot)
        self.apikey = key
        print("Logging in to YouTube")
        self.api = build("youtube","v3")
        print("Done")

    def on_call(self,event,positions):
        id = positions.group(0)
        videoData = self.api.videos().list(part="snippet",id=id,key=self.apikey).execute()
        try:
            info = videoData["items"][0]["snippet"]
        except KeyError:
            #self.pubMsg(event,"Could not get video data for the video posted by \b%s\b." % event.source.nick)
            return
        except IndexError:
            #self.pubMsg(event,"Could not get video data for the video posted by \b%s\b." % event.source.nick)
            return

        title = info["title"]
        try:
            description = info["description"].split("\n")[0].strip()[:77].strip()+"..."
        except IndexError:
            description = info["description"].split("\n")[0]

        channel = info["channelTitle"]

        self.pubMsg(event,"Video posted by \b%s\b is: \b%s\b by \b%s\b, \b%s\b" % (event.source.nick,title,channel,description))


class imgurScanner(TextReader):
    regExp = "(?<=imgur.com/)[^?&]*"

    def __init__(self,bot,id,secret):
        TextReader.__init__(self,bot)
        self.id = id
        self.secret = secret
        print("Logging in to Imgur")
        self.client = imgurpython.ImgurClient(self.id,self.secret)
        print("Done")

    def on_call(self,event,positions):
        data = positions.group(0).split("/")
        if len(data) != 1:
            print("Not an image")
            return

        id = data[-1]
        print(id)
        x = self.client.get_image(id)

        # nick = event.source.nick
        # title = x.title if x.title is not None else "Not title"
        # uploader = x.account_url if x.account_url != "null" else "Anon"
        # date = time.strftime("%Y-%m-%d",time.gmtime(x.datetime))
        try:
            description = x.description[80]+"..." if len(x.description) > 80 else x.description
        except:
            description = None

        text = "Imgur link posted by \b%s\b: " % event.source.nick
        text += ("\b'%s'\b "% x.title) if x.title is not None else "This image was "
        text += "uploaded by \b%s\b " % (x.account_url if x.account_url is not None else "an anonymous user")
        text += "at \b%s\b GMT." % time.strftime("%Y-%m-%d",time.gmtime(x.datetime))
        text += ("'\b%s\b'" % description) if description is not None else ""
        if x.nsfw:
            text += "\bTHIS IMAGE HAS BEEN MARKED NSFW.\b"



        self.pubMsg(event,text)
