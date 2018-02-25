def render_all(con, entities, game_map, fov_recompute, colors):
    # Draw walls.
    if fov_recompute:
        draw_walls(con, game_map, colors) 
    # Draw Entities.
    for entity in entities:
        draw_entity(con, entity, game_map.fov)

def draw_walls(con, game_map, colors):
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

def draw_entity(con, entity, fov):
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def clear_entity(con, entity):
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
