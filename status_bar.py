from etc.colors import COLORS


class StatusBar:

    def __init__(self, *, total_width, bar_colors):
        self.total_width = total_width
        self.bar_color = bar_colors['bar_color']
        self.back_color = bar_colors['back_color']
        self.string_color = bar_colors['string_color']

    def render(self, panel, x, y, *, name, maximum, value):
        bar_width = int(self.total_width * value / maximum)
        panel.draw_rect(
            x, y, self.total_width, 1, None, bg=self.back_color)
        if bar_width > 0:
            panel.draw_rect(
                x, y, bar_width, 1, None, bg=self.bar_color)
        text = name + ': ' + str(value) + '/' + str(maximum)
        x_centered = x + int((self.total_width - len(text)) / 2)
        panel.draw_str(x_centered, y, text, fg=self.string_color, bg=None)
