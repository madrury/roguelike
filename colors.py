import random

COLOR_PATHS = {
    'dark_to_light_green': [
        (0, g, 0) for g in [180, 190, 200, 210, 220, 230, 240, 250]]
}

def random_yellow():
    rg = int(random.uniform(220, 226))
    return (rg, rg, int(random.uniform(150, 200)))

def random_red():
    red = int(random.uniform(100, 255))
    return (red, 0, 0)

def random_light_water():
    return (40, 40, int(random.uniform(200, 255)))

def random_dark_water():
    return (40, 40, int(random.uniform(80, 140)))

def random_red_or_yellow():
    x = random.uniform(0, 1)
    if x <= 0.8:
        return random_red()
    else:
        return random_yellow()
