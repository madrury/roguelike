def handle_keys(user_input):
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
    # Meta Events
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        return {'exit': True}
    return {}
