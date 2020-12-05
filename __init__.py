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
        #print("Utterance:" + utterance)

        instance = None
        empty_record = 'empty_record'
        url_record = 'junk'
        count = 0

        
        while url_record != None and url_record != empty_record:

                count = count + 1
                stream_name = 'stream' + str(count)
                #print("Try reading from: " + stream_name)
                url_record = self.settings.get(stream_name)
                if url_record == None or url_record == empty_record:
                        ...
                        if url_record == None:
                                print(" Returned: None")
                        else:
                                print(" Returned: " + empty_record)
                        ...
                        continue

                print(" Returned: " + url_record)
                        
                strings = url_record.split(",")
                self.url = strings[1]
                #print("  found: " + strings[0])
        
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

        # if we didn't find our station
        if url_record == empty_record or url_record == None:
                self.speak_dialog("Please enter this station in your Stream Player skill setup")
        
        # if there is no open record in the user's table, create one
        if url_record == None:
                f = open("skills/stream-player-skill/settingsmeta.yaml","a+")
                f.write("        - name: stream%d\n" % count)
                f.write("          type: text\n")
                f.write("          label: Stream %d\n" % count)
                f.write("          value: \"empty_record\"\n")
                f.close()
         
    @intent_handler('player.stop.intent')
    def handle_stop_intent(self, message):
        mystring = message.data.get('utterance')
        LOG.info(mystring)
        self.url = ''
        self.player.stop()
        
def create_skill():
    return StreamPlayer()

