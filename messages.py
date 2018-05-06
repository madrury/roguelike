import textwrap


class Message:
    
    def __init__(self, text, color=(255, 255, 255)):
        self.text = text
        self.color = color


class MessageLog:

    def __init__(self, message_config):
        self.messages = []
        self.x = message_config['x']
        self.width = message_config['width']
        self.height = message_config['height']

    def add_message(self, message):
        msg_lines = textwrap.wrap(message.text, self.width)
        for line in msg_lines:
            if len(self.messages) == self.height:
                del self.messages[0]
            self.messages.append(Message(line, message.color))

    def render(self, panel):
        for y, message in enumerate(self.messages, start=1):
            panel.draw_str(
                self.x, y, message.text, bg=None, fg=message.color)
