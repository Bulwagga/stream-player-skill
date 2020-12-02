from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import re
import vlc
import time

class StreamPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    url = ''
    player=''
    
    @intent_handler('player.stream.intent')
    def handle_stream_intent(self, message):
        #self.speak_dialog("find a station")
        #print('Message: "{}"'.format(message.data.get('utterance')))
        utterance = message.data.get('utterance')
        self.speak_dialog(utterance)
        LOG.info(utterance)
        words = utterance.split(" ")

        stations = [ 'wamc', 'weqx' ]
        instance = None
        
        for station in stations:
                if re.search(station, words[1]):
                
                        self.url = 'http://playerservices.streamtheworld.com/api/livestream-redirect/WAMCHD2.mp3'
                        
                        if instance == None:
                                #define VLC instance
                                instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
                                if instance is None:      # atfer bundled self.instance is None
                                        LOG.exception("VLC could not create an Instance")
                                        break

                                #Define VLC player
                                self.player=instance.media_player_new()

                        #Define VLC media
                        media=instance.media_new(self.url)

                        #Set player media
                        self.player.set_media(media)

                        #Play the media
                        self.player.play()
                        
                        break
        if self.url == '':
                self.speak_dialog("Please enter that station in your Stream Player skill setup")
        	
    @intent_handler('player.stop.intent')
    def handle_stop_intent(self, message):
        mystring = message.data.get('utterance')
        LOG.info(mystring)
        self.url = ''
        self.player.stop()
        
def create_skill():
    return StreamPlayer()

