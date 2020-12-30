from mycroft import MycroftSkill, intent_handler
# see https://github.com/johnbartkiw/mycroft-skill-iheartradio/__init__.py
from mycroft.util.log import LOG
from mycroft.audio.services.vlc import VlcService
import re
import time

class StreamPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    url = ''
    mediaplayer=''
    
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
        mediaplayer = None
       
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
                        
                strings = url_record.split(",")
                self.url = strings[1]

                if re.search(strings[0].lower(), utterance):

                        if instance == None:
                                self.mediaplayer = VlcService(config={'low_volume': 10, 'duck': True})

                                if self.mediaplayer is None:
                                        LOG.exception("VLC could not create an Instance")
                                        break

                        #Play the media
                        self.speak_dialog("player.stream")
                        time.sleep(2.0)
                        tracklist = []
                        tracklist.append(self.url)
                        self.mediaplayer.add_list(tracklist)
                        self.mediaplayer.play()
                        break

        # if we didn't find our station
        if url_record == empty_record or url_record == None:
                self.speak_dialog("player.settings")
        
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
        self.mediaplayer.stop()
        self.mediaplayer.clear_list()
        self.url = ''
        
def create_skill():
    return StreamPlayer()

