from time import sleep
from collections import deque
import random

import tdl

from utils.utils import coordinates_within_circle, bresenham_line
from etc.enum import Animations
from etc.colors import COLORS
from etc.chars import CHARS
from colors import (
    COLOR_PATHS, random_yellow, random_red, random_orange,
    random_red_or_yellow, random_grey, random_light_blue, random_dark_blue)

def construct_animation(animation_data, game_map):
    """Construct an appropriate animation player object given the type of
    animation and the data needed to construct the animation.  This is
    basically a large switch statement.
    """
    animation_type = animation_data[0]
    if animation_type == Animations.MAGIC_MISSILE:
        _, source, target = animation_data
        animation_player = MagicMissileAnimation( game_map, source, target)
    elif animation_type == Animations.THROWING_KNIFE:
        _, source, target = animation_data
        animation_player = ThrowingKnifeAnimation(game_map, source, target)
    elif animation_type == Animations.FIREBALL:
        _, source, target = animation_data
        animation_player = FireballAnimation(game_map, source, target)
    elif animation_type == Animations.ICEBALL:
        _, source, target = animation_data
        animation_player = IceballAnimation(game_map, source, target)
    elif animation_type == Animations.THROW_POTION:
        _, source, target = animation_data
        animation_player = ThrownPotionAnimation(game_map, source, target)
    elif animation_type == Animations.HEALTH_POTION:
        _, target = animation_data
        animation_player = ColorCycleAnimation(
            game_map, target, COLOR_PATHS['dark_to_light_green'])
    elif animation_type == Animations.POWER_POTION:
        _, target = animation_data
        animation_player = ColorCycleAnimation(
            game_map, target, COLOR_PATHS['yellow_to_red'])
    elif animation_type == Animations.CONFUSION_POTION:
        _, target = animation_data
        animation_player = ColorCycleAnimation(
            game_map, target, COLOR_PATHS['dark_to_light_purple'])
    elif animation_type == Animations.SPEED_POTION:
        _, target = animation_data
        animation_player = ColorCycleAnimation(
            game_map, target, COLOR_PATHS['flickering_yellow'])
    elif animation_type == Animations.TELEPORTATION_POTION:
        _, target = animation_data
        animation_player = ColorCycleAnimation(
            game_map, target, COLOR_PATHS['flickering_blue'])
    elif animation_type == Animations.FIREBLAST:
        _, center, radius = animation_data
        animation_player = FireblastAnimation(
            game_map, center, radius)
    elif animation_type == Animations.WATERBLAST:
        _, center, radius = animation_data
        animation_player = WaterblastAnimation(
            game_map, center, radius)
    elif animation_type == Animations.CONCATINATED:
        animation_player = ConcatinatedAnimation.construct(
            game_map, animation_data[1])
    elif animation_type == Animations.SIMULTANEOUS:
        animation_player = SimultaneousAnimation.construct(
            game_map, animation_data[1])
    return animation_player


class ConcatinatedAnimation:
    """An animation constructed from concatinating other animations together.

    Concatinated animations are played by playing the component animations in
    sequence, until the final animation in the sequence is finished.
    """
    def __init__(self, *animations):
        self.animations = animations
        self.n_animations = len(animations)
        self.current_animation = 0

    def next_frame(self):
        current_animation = self.animations[self.current_animation]
        result = current_animation.next_frame()
        if result and self.current_animation != self.n_animations - 1:
            self.current_animation += 1
            return False
        elif result and self.current_animation == self.n_animations - 1:
            return True
        else:
            return False

    @staticmethod
    def construct(game_map, animation_data):
        """Consume runtime game data and construct a concatinated animation.
        """
        animations = []
        for datum in animation_data:
            animations.append(construct_animation(datum, game_map))
        return ConcatinatedAnimation(*animations)


class SimultaneousAnimation:
    """An animation constructed from playing other animations simultaneously.

    Simultaneous animations are played concurrently, until all of the component
    animations are finished.
    """
    def __init__(self, *animations):
        self.animations = animations
        self.n_animations = len(animations)

    def next_frame(self):
        finished = [False] * self.n_animations
        for idx, a in enumerate(self.animations):
            if not finished[idx]:
                finished[idx] = a.next_frame()
        return all(finished)

    @staticmethod
    def construct(game_map, animation_data):
        """Consume runtime game data and construct a concatinated animation.
        """
        animations = []
        for datum in animation_data:
            animations.append(construct_animation(datum, game_map))
        return SimultaneousAnimation(*animations)

            

class ColorCycleAnimation:
    """Animation that cycles through a sequence of background colors for a
    tile.  Used for various potions (health, power, etc).

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    target: (int, int):
      The location of the animation.

    color_path: List[Color]
      A sequence of RGB colors to cycle through.
    """
    def __init__(self, game_map, target, color_path=None):
        self.game_map = game_map
        self.target = target
        self.fg_color = game_map.fg_colors[target[0], target[1]]
        self.bg_color = game_map.bg_colors[target[0], target[1]]
        self.char = game_map.chars[target[0], target[1]]
        self.color_iter = iter(color_path)

    def next_frame(self):
        try:
            color = next(self.color_iter)
            self.game_map.draw_char(
                self.target[0], self.target[1], self.char, 
                fg=self.fg_color, bg=color)
        except StopIteration:
            self.game_map.draw_char(
                self.target[0], self.target[1], self.char, 
                fg=self.fg_color, bg=self.bg_color)
            return True
        return False


class ThrownPotionAnimation:
    """Animation for throwing a potion.

    Draws the potion glyph along a path from a source to a target.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    target: (int, int):
      The location of the target.
    """
    def __init__(self, game_map, source, target):
        self.game_map = game_map
        self.source = source
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.char = '!'
        self.color = COLORS['violet']
        self.current_frame = 0

    def next_frame(self):
        return draw_missile(self)
        

class MagicMissileAnimation:
    """Animation for casting a magic missile.

    Fickers tiles random shades of yellow between a source and a target.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    target: (int, int):
      The location of the target.
    """
    def __init__(self, game_map, source, target):
        self.game_map = game_map
        self.source = source
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.char = '*'
        self.current_frame = 0

    def next_frame(self):
        return draw_missile(self, random_yellow(), random_yellow())


class FireblastAnimation:
    """Animation for casting a fireblast.

    Draws an expanding circle (in the L1 metric) centerd at a source in random
    shades of red/yellow.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    radius: int:
      The radius of the fireblast.
    """
    def __init__(self, game_map, source, radius=4):
        self.game_map = game_map
        self.source = source
        self.radius = radius
        self.radius_iter = iter(range(radius + 1))

    def next_frame(self):
        return draw_blast(self, char='^', 
                          fg_color_callback=random_red_or_yellow,
                          bg_color_callback=random_red_or_yellow)         


class WaterblastAnimation:
    """Animation for casting a waterblast.

    Same as a fireblast animation, but uses water colors.
    """
    def __init__(self, game_map, source, radius=4):
        self.game_map = game_map
        self.source = source
        self.radius = radius
        self.radius_iter = iter(range(radius + 1))

    def next_frame(self):
        return draw_blast(self, char='~', 
                          fg_color_callback=random_light_blue,
                          bg_color_callback=random_light_blue)         


class ThrowingKnifeAnimation:
    """Animation for throwing a knife potion.

    Draws the throwing knife along a path from a source to a target.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    target: (int, int):
      The location of the target.
    """
    def __init__(self, game_map, source, target):
        self.game_map = game_map
        self.source = source
        self.target = target
        # TODO: This should use a brenenham ray.
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.char = self._get_char()
        self.color = COLORS['white']
        self.current_frame = 0

    def _get_char(self):
        """The knife uses a different character depending on the direction it
        is thrown.
        """
        if len(self.path) == 1:
            # Nothing to draw.
            return ' '
        dx, dy = (self.path[1][0] - self.path[0][0],
                  self.path[1][1] - self.path[0][1])
        if (dx, dy) in ((-1, 1), (0, 1), (1, 1)):
            return CHARS['down_arrow']
        elif (dx, dy) in ((-1, -1), (0, -1), (1, -1)):
            return CHARS['up_arrow']
        elif (dx, dy) == (1, 0):
            return CHARS['left_arrow']
        else:
            return CHARS['right_arrow']
        raise ValueError('Path does not move away from starting position.')

    def next_frame(self):
        return draw_missile(self)


class FireballAnimation:
    """Animation for a fireball, as from a FireStaff.

    Draws a three tile travelling sequence from a source to a target.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    target: (int, int):
      The location of the target.
    """
    def __init__(self, game_map, source, target):
        self.game_map = game_map
        self.source = source
        self.target = target
        self.pathiter = iter(bresenham_line(game_map, source, target))
        self.current_positions = deque()
        self.current_frame = 0

    def next_frame(self):
        return draw_ball(self, head_fg_callback=random_orange, 
                               head_bg_callback=random_red,
                               middle_fg_callback=random_yellow,
                               middle_bg_callback=random_orange,
                               tail_fg_callback=random_yellow,
                               tail_bg_callback=random_yellow)


class IceballAnimation:
    """Animation for a Ice, as from an IceStaff.

    Draws a three tile travelling sequence from a source to a target.

    Parameters
    ----------
    game_map: GameMap object
      The game_map to draw the animation on.

    source: (int, int):
      The location of the source.

    target: (int, int):
      The location of the target.
    """
    def __init__(self, game_map, source, target):
        self.game_map = game_map
        self.source = source
        self.target = target
        self.pathiter = iter(bresenham_line(game_map, source, target))
        self.current_positions = deque()
        self.current_frame = 0

    def next_frame(self):
        return draw_ball(self, head_fg_callback=lambda: (255, 255, 255), 
                               head_bg_callback=random_grey,
                               middle_fg_callback=random_grey,
                               middle_bg_callback=random_light_blue,
                               tail_fg_callback=random_light_blue,
                               tail_bg_callback=random_dark_blue)



def draw_ball(animation, *, head_fg_callback, head_bg_callback,
                            middle_fg_callback, middle_bg_callback,
                            tail_fg_callback, tail_bg_callback):
    """Animate a ball projectile travelling from a source to a target.

    A ball projectile is made of three tiles, a head, middle, and tail.  It
    travels in a straight line path from a source to a target.

    Parameters
    ----------
    animation: Animation object
      Must have .current_frame, and game_map attributes.

    head_fg_callback: function: [] -> (int, int, int)
      A callback that returns an RGB tuple, used to color the foreground
      charecter.

    head_bg_callback: function: [] -> (int, int, int)
      A callback that returns an RGB tuple, used to color the background of
      each tile.

    middle_fg_callback, middle_bg_callback, tail_fg_callback, tail_bg_callback:
       Similar.
    """
    position = None
    try:
        position = next(animation.pathiter)
    except StopIteration:
        pass
    if position:
        animation.current_positions.appendleft(position)
    if animation.current_frame >= 3:
        p = animation.current_positions.pop()
        animation.game_map.draw_position(p[0], p[1])
    if len(animation.current_positions) >= 1:
        x, y = animation.current_positions[0]
        if animation.game_map.fov[x, y]:
            animation.game_map.draw_char(
                x, y, '*', head_fg_callback(), head_bg_callback())
        # When the head of the fireball leaves the fov, immediately break
        # out of the animation.
        else:
            return True
    if len(animation.current_positions) >= 2:
        x, y = animation.current_positions[1]
        if animation.game_map.fov[x, y]:
            animation.game_map.draw_char(
                x, y, '*', middle_fg_callback(), middle_bg_callback())
    if len(animation.current_positions) >= 3:
        x, y = animation.current_positions[2]
        if animation.game_map.fov[x, y]:
            animation.game_map.draw_char(
                x, y, '*', tail_fg_callback(), tail_bg_callback())
    animation.current_frame += 1
    if len(animation.current_positions) == 0:
        return True
    return False


def draw_blast(animation, *, char, fg_color_callback, bg_color_callback):
    """Animate a blast emenating from a source.

    Parameters
    ----------
    animation: Animation object
      Must have .current_frame, and game_map attributes.

    char:
      The character to draw for each tile of the blast.

    fg_color_callback: function: [] -> (int, int, int)
      A callback that returns an RGB tuple, used to color the foreground
      charecter.

    fg_color_callback: function: [] -> (int, int, int)
      A callback that returns an RGB tuple, used to color the backgrounf of
      each tile.
    """
    try:
        blast_radius = next(animation.radius_iter)
    # Clear the drawing of the blast, the animation has finished.
    except StopIteration:
        clear_coordinates = coordinates_within_circle(
            (animation.source[0], animation.source[1]), animation.radius)
        for x, y in clear_coordinates:
            if animation.game_map.within_bounds(x, y):
                animation.game_map.draw_position(x, y)
        return True
    # Draw a circle centered at `source`.
    blast_coordinates = coordinates_within_circle(
        (animation.source[0], animation.source[1]), blast_radius)
    for x, y in blast_coordinates:
        if (animation.game_map.within_bounds(x, y) and 
            (animation.game_map.fov[x, y] or animation.game_map.shrub[x, y]) and 
            animation.game_map.walkable[x, y]):
            animation.game_map.draw_char(
                x, y, char, fg_color_callback(), bg_color_callback())
    return False


def draw_missile(animation, fg=None, bg=None):
    """Animate a missile moving from a source to a target.

    Parameters
    ----------
    animation: Animation object
      Must have .current_frame, and game_map attributes.
    """
    if len(animation.path) == 0:
        return True
    missile_location = animation.path[animation.current_frame]
    if not fg:
        fg = animation.color
    if not bg:
        bg = animation.game_map.bg_colors[
            missile_location[0], missile_location[1]]
    # Clear the previous frame's missile.
    if animation.current_frame >= 1:
        x, y = animation.path[animation.current_frame - 1]
        animation.game_map.draw_position(x, y)
    # If the missile has reached the target, the animation is done.
    if missile_location == animation.target:
        return True
    # Draw the missile.
    if animation.game_map.fov[missile_location[0], missile_location[1]]:
        animation.game_map.draw_char(
            missile_location[0], missile_location[1],
            animation.char, fg=fg, bg=bg)
    animation.current_frame += 1
    return False
