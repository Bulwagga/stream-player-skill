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
        #self.speak_dialog(utterance)
        LOG.info(utterance)

        instance = None
        url_record = 'junk'
        count = 0
        
        while url_record != '':
                
                count = count + 1
                stream_name = 'stream' + str(count)
                url_record = self.settings.get(stream_name)
                
                if url_record == '':
                        continue
                        
                strings = url_record.split(" ")
                self.url = strings[1]
                print(self.url)
                print(strings[0])
                print(utterance)
        
                if re.search(strings[0].lower(), utterance):

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

        if url_record == '':
                self.speak_dialog("Please enter that station in your Stream Player skill setup")
        	
    @intent_handler('player.stop.intent')
    def handle_stop_intent(self, message):
        mystring = message.data.get('utterance')
        LOG.info(mystring)
        self.url = ''
        self.player.stop()
        
def create_skill():
    return StreamPlayer()

