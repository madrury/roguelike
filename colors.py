import random

COLOR_PATHS = {
    'dark_to_light_green': [
        (0, g, 0) for g in [180, 190, 200, 210, 220, 230, 240, 250]],
    'yellow_to_red': [
        (255, g, 0) for g in [250, 210, 170, 130, 90, 50, 10, 0]]
}

def random_yellow():
    rg = int(random.uniform(220, 226))
    return (rg, rg, int(random.uniform(150, 200)))

def random_red():
    red = int(random.uniform(150, 255))
    return (red, 0, 0)

def random_orange():
    green = int(random.uniform(0, 130))
    return (255, green, 0)

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

def random_light_water():
    return (40, 40, int(random.uniform(200, 255)))

def random_dark_water():
    return (40, 40, int(random.uniform(80, 140)))
