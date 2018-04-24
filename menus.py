import tdl
import textwrap
import string

from etc.colors import COLORS

def menu(header, options, width, screen_width, screen_height,
         header_buffer=1, border_buffer=1):
    """Draw a generic menu with a header and options for selection.

    Arguments
    ---------
    header: str
      A text string to print at the top of a menu for description.

    options: list[str]
      A list of options for the user to select.

    width: int
      The width of the menu.

    screen_width: int
      The width of the screen into which the menu will be drawn.

    screen_height: int
      The height of the screen into which the menu will be drawn.

    Returns
    -------
    (window, x_position, y_position): tdl.Console, int, int:
      The console contining the window, and the position to blit the console
      onto the main console.
    """
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height + header_height + 4*border_buffer

    window = tdl.Console(width, height)
    window.draw_rect(0, 0, width, height, None, fg=COLORS['white'], bg=None)
    window.draw_frame(0, 0, width, height, '~', fg=None, bg=COLORS['darker_red'])
    for i, line in enumerate(header_wrapped):
        window.draw_str(2, i+2, header_wrapped[i])
    for i, (y, option) in enumerate(enumerate(options, start=header_height + 3)):
        text = '(' + string.ascii_lowercase[i] + ') ' + option
        window.draw_str(2, y, text)
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
