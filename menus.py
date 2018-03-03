import tdl
import textwrap
import string

def menu(header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    window = tdl.Console(width, height)
    window.draw_rect(0, 0, width, height, None, fg=(255, 255, 255), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, i, header_wrapped[i])
    for i, (y, option) in enumerate(enumerate(options, start=header_height)):
        text = '(' + string.ascii_lowercase[i] + ') ' + option
        window.draw_str(0, y, text)
    # Return the position to blit the new console
    return window, screen_width // 2 - width // 2, screen_height //2 - height // 2

def invetory_menu(header, inventory, invetory_width, 
                  screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Invetory is Empty']
    else:
        options = [item.name for item in inventory.items]
    return menu(header, options, invetory_width,
                screen_width, screen_height)
