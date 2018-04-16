def render_all(con, entities, game_map, fov_recompute, colors):
    # Draw walls.
    if fov_recompute:
        _draw_walls(con, game_map, colors) 
    # Draw Entities.
    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        _draw_entity(con, entity, game_map.fov)

def render_health_bars(panel, player, panel_config, colors):
    panel.clear(fg=colors['white'], bg=colors['black'])
    hp_bar_colors = {
        'bar_color': colors['light_red'],
        'back_color': colors['darker_red'],
        'string_color': colors['white']}
    _render_bar(panel, 'HP', 1, 1, panel_config['bar_width'], 
                player.harmable.hp, player.harmable.max_hp,
                hp_bar_colors)

def render_messages(panel, message_log):
    for y, message in enumerate(message_log.messages, start=1):
        panel.draw_str(
            message_log.x, y, message.text, bg=None, fg=message.color)

def clear_all(con, entities):
    for entity in entities:
        _clear_entity(con, entity)


def _render_bar(panel, name, x, y, total_width, value, maximum, bar_colors):
    bar_color = bar_colors['bar_color']
    back_color = bar_colors['back_color']
    string_color = bar_colors['string_color']
    bar_width = int(total_width * value / maximum)
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width - len(text)) / 2)
    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def _draw_walls(con, game_map, colors):
    for x, y in game_map:
        wall = not game_map.transparent[x, y]
        if game_map.fov[x, y]:
            if wall:
                con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
            else:
                con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))
            game_map.explored[x, y] = True
        elif game_map.explored[x, y]:
            if wall:
                con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
            else:
                con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))

def _draw_entity(con, entity, fov):
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def _clear_entity(con, entity):
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
