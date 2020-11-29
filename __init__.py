from mycroft import MycroftSkill, intent_file_handler


class StreamPlayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('player.stream.intent')
    def handle_player_stream(self, message):
        self.speak_dialog('player.stream')


def create_skill():
    return StreamPlayer()

