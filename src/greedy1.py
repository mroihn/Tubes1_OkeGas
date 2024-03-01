import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position

from ..util import get_direction

teleport = []


class Greedy1Logic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        global teleport
        teleport = []

        minDist = -1
        for i in board.game_objects:
            if i.type == "DiamondGameObject":
                tmp = abs(i.position.x - current_position.x) + abs(
                    i.position.y - current_position.y
                )
                if tmp != 0:
                    if props.diamonds == 4:
                        if i.properties.points == 1:
                            if minDist == -1:
                                minDist = tmp
                                self.goal_position = i.position
                                # self.goal_position.y = i.position.y
                            elif tmp < minDist:
                                minDist = tmp
                                self.goal_position = i.position
                                # self.goal_position.y = i.position.y
                    else:
                        if minDist == -1:
                            minDist = tmp
                            self.goal_position = i.position
                            # self.goal_position.y = i.position.y
                        elif tmp < minDist:
                            minDist = tmp
                            self.goal_position = i.position
                            # self.goal_position.y = i.position.y
            if i.type == "TeleportGameObject":
                teleport.append(i)

            # print(i.position)
        # print(self.goal_position)
        # print(current_position)
        # print(board.game_objects)
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base

        distTel0 = abs(teleport[0].position.x - current_position.x) + abs(
            teleport[0].position.y - current_position.y
        )
        distTel1 = abs(teleport[1].position.x - current_position.x) + abs(
            teleport[1].position.y - current_position.y
        )

        distNow = abs(self.goal_position.x - current_position.x) + abs(
            self.goal_position.y - current_position.y
        )

        print(distTel0, " ", distTel1, " ", distNow," ",board_bot.properties.name)
        if distTel0 != 0 and distTel1 != 0:
            if distTel0 < distTel1 and distTel1 < distNow:
                self.goal_position = teleport[0].position
            elif distTel1 < distTel0 and distTel0 < distNow:
                self.goal_position = teleport[1].position

        # else:
        #     # Just roam around
        #     self.goal_position = None

        # current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            # delta = self.directions[self.current_direction]
            # delta_x = delta[0]
            # delta_y = delta[1]
            # if random.random() > 0.6:
            #     self.current_direction = (self.current_direction + 1) % len(
            #         self.directions
            #     )
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        return delta_x, delta_y
