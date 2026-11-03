from classes.modules.hitbox import OverlapParams, query_cone
import pygame
import sys
from pathlib import Path



CHOP_REACH = 45
CHOP_HALF_ANGLE = 50
CHOP_PARAMS = OverlapParams(names=frozenset({"tree trunk"}))

shaking_trees = []


def resource_path(relative_p):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    
    return base_path / relative_p

pygame.mixer.init()

chopped = pygame.mixer.Sound(
                        str(
                            resource_path("Assets/Audio/choptree.wav")
                        )
                    )

def chop_tree(player, dmg, trees, solid_obs, obstacle_grid, resource_inventory):
    hits = query_cone(
        obstacle_grid, player.pos, player.angle,
        CHOP_REACH, CHOP_HALF_ANGLE, CHOP_PARAMS,
    )

    if not hits:
        return False #swing!!

    chopped.play()

    closest_obstacle = hits[0]
    tree = closest_obstacle.owner
    tree.hp -= dmg
    if tree.hp > 0:
        tree.shake = 0.18
        if tree not in shaking_trees:
            shaking_trees.append(tree)
        return True
    
    if not resource_inventory.add("wood_log", tree.log_yield):
        tree.hp = 1
        return True
    
    obstacle_grid.remove(closest_obstacle)
    solid_obs.remove(closest_obstacle)
    trees.remove(tree)
    return True

