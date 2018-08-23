from etc.enum import GameStates, InputTypes, INVENTORY_STATES


class PlayerInputHandler:

    def handle_keys(self, user_input, game_state):
        """Consider user input and return a consequent action.

        Interpretation of user input is context dependent, so we have multiple
        helper functions to handle keys in differing contexts.

        Arguments
        ---------
        user_input: tdl.event.Event object
          A current event.  Probably a keypress or mouse event.

        game_state: GameState object
          The current game state.  Key presses are context dependent, and this
          supplies the context for the press.

        Returns
        -------
        action: dict {action_name [str]: action_data}
          A dictionary telling the game engine what action to take in response
          to this event.
        """
        if user_input == None:
            return {}
        if game_state == GameStates.PLAYER_TURN:
            return self.handle_player_turn_keys(user_input)
        elif game_state in INVENTORY_STATES:
            return self.handle_inventory_keys(user_input)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keys(user_input)
        elif game_state == GameStates.CURSOR_INPUT:
            return handle_cursor_keys(user_input)
        else:
            return {}

    def handle_player_turn_keys(self, user_input):
        """Handle user input on the player's turn."""   
        key_char = user_input.char
        # Movement events
        if user_input.key == 'UP' or key_char == 'k':
            return {InputTypes.MOVE: (0, -1)}
        elif user_input.key == 'DOWN' or key_char == 'j':
            return {InputTypes.MOVE: (0, 1)}
        elif user_input.key == 'LEFT' or key_char == 'h':
            return {InputTypes.MOVE: (-1, 0)}
        elif user_input.key == 'RIGHT' or key_char == 'l':
            return {InputTypes.MOVE: (1, 0)}
        elif key_char == 'y':
            return {InputTypes.MOVE: (-1, -1)}
        elif key_char == 'u':
            return {InputTypes.MOVE: (1, -1)}
        elif key_char == 'b':
            return {InputTypes.MOVE: (-1, 1)}
        elif key_char == 'n':
            return {InputTypes.MOVE: (1, 1)}
        elif key_char == 'z':
            return {InputTypes.MOVE: (0, 0)}
        # Other player events
        if key_char == 'g':
            return {InputTypes.PICKUP: True}
        # Meta Events
        if key_char == 'i':
            return {InputTypes.SHOW_INVENTORY: True}
        if key_char == 'd':
            return {InputTypes.DROP_INVENTORY: True}
        if key_char == 't':
            return {InputTypes.THROW_INVENTORY: True}
        if key_char == 'e':
            return {InputTypes.EQUIP_INVENTORY: True}
        return handle_generic_keys(user_input)

    def handle_inventory_keys(self, user_input):
        if not user_input.char:
            return {}
        # Index in the alphabet starting with 'a' at index 0
        index = ord(user_input.char) - ord('a')
        if index >= 0:
            return {InputTypes.INVENTORY_INDEX: index}
        return handle_generic_keys(user_input)


def handle_player_dead_keys(user_input):
    key_char = user_input.char
    if key_char == 'i':
        return {InputTypes.SHOW_INVENTORY: True}
    return handle_generic_keys(user_input)

def handle_cursor_keys(user_input):
    key_char = user_input.char
    if user_input.key == 'ENTER':
        return {InputTypes.CURSOR_SELECT: True}
    elif user_input.key == 'UP' or key_char == 'k':
        return {InputTypes.MOVE: (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 'j':
        return {InputTypes.MOVE: (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'h':
        return {InputTypes.MOVE: (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'l':
        return {InputTypes.MOVE: (1, 0)}
    elif key_char == 'y':
        return {InputTypes.MOVE: (-1, -1)}
    elif key_char == 'u':
        return {InputTypes.MOVE: (1, -1)}
    elif key_char == 'b':
        return {InputTypes.MOVE: (-1, 1)}
    elif key_char == 'n':
        return {InputTypes.MOVE: (1, 1)}
    elif key_char == 'z':
        return {InputTypes.MOVE: (0, 0)}
    return handle_generic_keys(user_input)

def handle_generic_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:
        return {InputTypes.FULLSCREEN: True}
    elif user_input.key == 'ESCAPE':
        return {InputTypes.EXIT: True}
    return {}
