from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import re


class StreamPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('player.stream.intent')
    def handle_stream_wamc_intent(self, message):
        self.speak_dialog("listen to this")
        print('Message: "{}"'.format(message.data.get('utterance')))
        mystring = message.data.get('utterance')
        self.speak_dialog(mystring)
        LOG.info(mystring)
        
        stations = [ 'wamc', 'weqx' ]
        
        if re.search(stations, mystring):
        	pass
        else:
        	self.speak_dialog("Please enter that station in your Stream Player skill setup"
        	

def create_skill():
    return StreamPlayer()

