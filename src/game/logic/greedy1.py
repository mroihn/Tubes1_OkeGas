import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position

from ..util import get_direction


class Greedy1Logic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.teleportLoc = []
        self.otherBot = None
        self.button = None

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # Cari diamond terdekat
        self.findNearestDiamond(board_bot, board)

        # Cari diamond berdasarkan density
        # self.findByDensityDiamond(board_bot, board)

        # Pakek button atau nggak
        self.useButtonOrNot(board_bot, board)

        # Jika inventory sudah full kembali ke base
        if props.diamonds == 5:
            base = board_bot.properties.base
            self.goal_position = base
        elif props.diamonds >= 3:
            self.cekBaseOrDir(board_bot, board)

        # Cek lebih cepat lewat teleport untuk ke tujuan atau nggak
        # self.cekTeleport(board_bot, board)

        # Cek kalo ada bot disekitar
        # if self.otherBot != None:
        #     self.goal_position = self.otherBot.position

        print(board_bot.properties.name, " ", current_position, " ", self.goal_position)
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        # else:
        #     # Move to base
        #     base = board_bot.properties.base
        #     self.goal_position = base
        return delta_x, delta_y

    def findNearestDiamond(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        props = board_bot.properties
        minDist = -1
        # Iterasi seluruh game object
        for i in board.game_objects:
            # Jika ketemu diamond cek apakah itu diamond terdekat
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
                            elif tmp < minDist:
                                minDist = tmp
                                self.goal_position = i.position
                    else:
                        if minDist == -1:
                            minDist = tmp
                            self.goal_position = i.position
                        elif tmp < minDist:
                            minDist = tmp
                            self.goal_position = i.position
            # Jika ketemu teleport simpan objeknya
            if i.type == "TeleportGameObject":
                self.teleportLoc.append(i)

            if i.type == "BotGameObject":
                distOtherBot = abs(i.position.x - current_position.x) + abs(
                    i.position.y - current_position.y
                )
                if distOtherBot == 1:
                    self.otherBot = i

            if i.type == "DiamondButtonGameObject":
                self.button = i

    def findByDensityDiamond(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        props = board_bot.properties
        minDen = -1
        goal = current_position
        # Iterasi seluruh game object
        for i in board.game_objects:
            # Jika ketemu diamond cek apakah itu diamond terdekat
            dist = abs(i.position.x - current_position.x) + abs(
                i.position.y - current_position.y
            )
            if i.type == "DiamondGameObject" and dist != 0:
                tmp = i.properties.points / dist
                if tmp != 0:
                    if props.diamonds == 4:
                        if i.properties.points == 1:
                            if minDen == -1:
                                minDen = tmp
                                goal = i.position
                            elif tmp > minDen:
                                minDen = tmp
                                goal = i.position
                    else:
                        if minDen == -1:
                            minDen = tmp
                            goal = i.position
                        elif tmp > minDen:
                            minDen = tmp
                            goal = i.position
            # Jika ketemu teleport simpan objeknya
            if i.type == "TeleportGameObject":
                self.teleportLoc.append(i)

            if i.type == "BotGameObject":
                distOtherBot = abs(i.position.x - current_position.x) + abs(
                    i.position.y - current_position.y
                )
                if distOtherBot == 1:
                    self.otherBot = i

            if i.type == "DiamondButtonGameObject":
                self.button = i

        self.goal_position = goal

    def cekTeleport(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position

        # jarak teleport 0 ke lokasi sekarang
        distTel0Cur = abs(self.teleportLoc[0].position.x - current_position.x) + abs(
            self.teleportLoc[0].position.y - current_position.y
        )
        # jarak teleport 1 ke lokasi sekarang
        distTel1Cur = abs(self.teleportLoc[1].position.x - current_position.x) + abs(
            self.teleportLoc[1].position.y - current_position.y
        )
        # jarak tujuan ke lokasi sekarang
        distGoalCur = abs(self.goal_position.x - current_position.x) + abs(
            self.goal_position.y - current_position.y
        )

        # print(distTel0, " ", distTel1, " ", distNow," ",board_bot.properties.name)
        # Cek lebih cepat pakek teleport atau nggak
        if distTel0Cur != 0 and distTel1Cur != 0:
            if distTel0Cur < distTel1Cur:
                distTel1Goal = abs(
                    self.teleportLoc[1].position.x - self.goal_position.x
                ) + abs(self.teleportLoc[1].position.y - self.goal_position.y)
                if distTel1Goal < distGoalCur:
                    self.goal_position = self.teleportLoc[0].position
            elif distTel1Cur < distTel0Cur:
                distTel0Goal = abs(
                    self.teleportLoc[0].position.x - self.goal_position.x
                ) + abs(self.teleportLoc[0].position.y - self.goal_position.y)
                if distTel0Goal < distGoalCur:
                    self.goal_position = self.teleportLoc[1].position

    def cekBaseOrDir(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position

        distBase = abs(board_bot.properties.base.x - current_position.x) + abs(
            board_bot.properties.base.y - current_position.y
        )

        distNow = abs(self.goal_position.x - current_position.x) + abs(
            self.goal_position.y - current_position.y
        )

        print(board_bot.properties.base)
        if distBase != 0 and distNow != 0:
            if distBase < distNow:
                self.goal_position = board_bot.properties.base

    def useButtonOrNot(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        distBase = abs(self.button.position.x - current_position.x) + abs(
            self.button.position.y - current_position.y
        )

        distNow = abs(self.goal_position.x - current_position.x) + abs(
            self.goal_position.y - current_position.y
        )

        if distBase < distNow:
            self.goal_position = self.button.position
