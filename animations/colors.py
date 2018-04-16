import random

COLOR_PATHS = {
    'dark_to_light_green': [
        (0, g, 0) for g in [180, 190, 200, 210, 220, 230, 240, 250]]
}

def random_yellow():
    rg = int(random.uniform(220, 226))
    return (rg, rg, int(random.uniform(0, 256)))
