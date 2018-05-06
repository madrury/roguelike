from etc.colors import COLORS


class StatusBar:

    def __init__(self, x, y, name, total_width, maximum, bar_colors):
        self.x = x
        self.y = y
        self.name = name
        self.total_width = total_width
        self.maximum = maximum
        self.bar_color = bar_colors['bar_color']
        self.back_color = bar_colors['back_color']
        self.string_color = bar_colors['string_color']

    def render(self, panel, value):
        bar_width = int(self.total_width * value / self.maximum)
        panel.draw_rect(
            self.x, self.y, self.total_width, 1, None, bg=self.back_color)
        if bar_width > 0:
            panel.draw_rect(
                self.x, self.y, bar_width, 1, None, bg=self.bar_color)
        text = self.name + ': ' + str(value) + '/' + str(self.maximum)
        x_centered = self.x + int((self.total_width - len(text)) / 2)
        panel.draw_str(x_centered, self.y, text, fg=self.string_color, bg=None)
