import tdl
import textwrap
import string

from etc.colors import COLORS


def menu(header, options, width, screen_width, screen_height, colors):
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

    colors: List[(int, int, int)]
      Colors to draw the description of the item.  Used to grey out items that
      are not selectable though the currently displayed menu.

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
    # The amount of whitespace:
    #  - header_buffer: Between the header and the first option.
    #  - For the border and any surrounding whitespace.
    #  - Between the left and right boundries and the text.
    header_buffer, border_buffer, edge_buffer = 1, 2, 2
    height = len(options) + header_height + header_buffer + 2*border_buffer
    
    window = tdl.Console(width, height)
    # Draw background and display frame.
    window.draw_rect(0, 0, width, height, None, fg=COLORS['white'], bg=None)
    window.draw_frame(0, 0, width, height, '~', fg=None, bg=COLORS['darker_red'])
    # Write the menu header.
    for i, line in enumerate(header_wrapped):
        window.draw_str(edge_buffer, i + border_buffer, header_wrapped[i])
    # Write all the options.
    options_buffer = border_buffer + header_height + header_buffer
    options_colors = zip(options, colors)
    iter_options = enumerate(enumerate(options_colors, start=options_buffer))
    for i, (y, (option, color)) in iter_options:
        text = '(' + string.ascii_lowercase[i] + ') ' + option
        window.draw_str(edge_buffer, y, text, fg=color) 
    # Return the position to blit the new console
    return window, screen_width // 2 - width // 2, screen_height //2 - height // 2


def invetory_menu(header, inventory, inventory_width, 
                  screen_width, screen_height, highlight_attr=None):
    if len(inventory.items) == 0:
        options = ['Invetory is Empty']
        highlight = [COLORS['white']]
    else:
        options = make_inventory_options(inventory)
        if highlight_attr:
            highlight = [
                COLORS['white'] if getattr(item, highlight_attr) 
                else COLORS['medium_grey'] 
                for item in inventory.items]
        else:
            highlight = [COLORS['white'] for item in inventory.items]
    return menu(header, options, inventory_width,
                screen_width, screen_height, colors=highlight)

def make_inventory_options(inventory):
    options = []
    for item in inventory.items:
        option = make_item_menu_display(item)
        options.append(option)
    return options

def make_item_menu_display(item):
    option = item.name
    if item.equipable:
        option += " " + item.equipable.make_menu_display()
    if item.consumable:
        option += " " + item.consumable.make_menu_display()
    return option
