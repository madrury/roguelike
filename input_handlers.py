from etc.enum import GameStates

def handle_keys(user_input, game_state):
    """Consider user input and return a consequent action.

    Interpretation of user input is context dependent, so we have
    multiple helper functions to handle keys in differing contexts.

    Arguments
    ---------
    user_input: tdl.event.Event object
      A current event.  Probably a keypress or mouse event.

    game_state: GameState object
      The current game state.  Key presses are context dependent, and
      this supplies the context for the press.

    Returns
    -------
    action: dict {action_name [str]: action_data}
      A dictionary telling the game engine what action to take in response
      to this event.
    """
    if game_state == GameStates.PLAYER_TURN:
        return handle_player_turn_keys(user_input)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(user_input)
    elif game_state in (GameStates.SHOW_INVETORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(user_input)
    else:
        return {}

def handle_player_turn_keys(user_input):
    """Handle user input on the player's turn."""   
    key_char = user_input.char
    # Movement events
    if user_input.key == 'UP' or key_char == 'k':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 'j':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'h':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'move': (0, 0)}
    # Other player events
    if key_char == 'g':
        return {'pickup': True}
    # Meta Events
    if key_char == 'i':
        return {'show_invetory': True}
    if key_char == 'd':
        return {'drop_inventory': True}
    return handle_generic_keys(user_input)

def handle_player_dead_keys(user_input):
    key_char = user_input.char
    if key_char == 'i':
        return {'show_invetory': True}
    return handle_generic_keys(user_input)

def handle_inventory_keys(user_input):
    if not user_input.char:
        return {}
    # Index in the alphabet starting with 'a' at index 0
    index = ord(user_input.char) - ord('a')
    if index >= 0:
        return {'inventory_index': index}
    return handle_generic_keys(user_input)

def handle_generic_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        return {'exit': True}
    return {}
