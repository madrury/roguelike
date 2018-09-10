import random

def random_red():
    red = int(random.uniform(150, 255))
    return (red, 0, 0)

def random_orange():
    green = int(random.uniform(0, 130))
    return (255, green, 0)

def random_yellow():
    blue = int(random.uniform(100, 180))
    return (255, 255, blue)

def random_orange_or_red():
    x = random.uniform(0, 1)
    if x <= 0.5:
        return random_red()
    else:
        return random_orange()

def random_red_or_yellow():
    x = random.uniform(0, 1)
    if x <= 0.8:
        return random_red()
    else:
        return random_yellow()

def random_light_green():
    g = int(random.uniform(120, 200))
    return (0, g, 30)

def random_grey():
    g = int(random.uniform(200, 250))
    return (g, g, g)

def random_dark_grey():
    g = int(random.uniform(40, 130))
    return (g, g, g)

def random_light_blue():
    rg = int(random.uniform(0, 160))
    return (rg, rg, 255)

def random_dark_blue():
    rg = int(random.uniform(0, 160))
    return (rg, rg, 200)

def random_light_water():
    return (40, 40, int(random.uniform(200, 255)))

def random_dark_water():
    return (40, 40, int(random.uniform(80, 140)))

def random_light_ice():
    dr = int(random.uniform(-10, 10))
    dg = int(random.uniform(-10, 10))
    db = int(random.uniform(-10, 10))
    return (30 + dr, 200 + dg, 245 + db)

def random_dark_ice():
    dr = int(random.uniform(-10, 10))
    dg = int(random.uniform(-10, 10))
    db = int(random.uniform(-10, 10))
    return (15 + dr, 100 + dg, 150 + db)


# Paths through the color space, used for potion animations.
COLOR_PATHS = {
    'dark_to_light_green': [
        (0, g, 0) for g in [180, 190, 200, 210, 220, 230, 240, 250]],
    'yellow_to_red': [
        (255, g, 0) for g in [250, 210, 170, 130, 90, 50, 10, 0]],
    'dark_to_light_purple': [
        (x, 0, x) for x in [250, 230, 210, 190, 170, 150, 130, 110]],
    'flickering_yellow': [random_yellow() for x in range(8)],
    'flickering_blue': [random_light_blue() for x in range(8)]
}
