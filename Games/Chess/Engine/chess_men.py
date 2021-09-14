import abc
from enum import Enum

from Games.Chess.Engine.chess_engine import site, chessmen
import Games.Chess.Engine.chess_engine as engine


class Chessman(abc.ABC):
    def __init__(self, site:site, chessman:chessmen, name:str, kills=[], moves=[]):
        self.site = site
        self.chessman = chessman
        self.name = name
        self.kills = kills
        self.moves = moves

    @abc.abstractclassmethod
    def get_move_positions(self) -> list:
        pass
        # returns the move set from a abstract position
        # [(x-Direction, y-Directon, endless), ...]    -> endless in this direction
        # or
        # [(lines, rows, endless), ...]

    @abc.abstractclassmethod
    def get_attack_positions(self) -> list:
        pass

    def get_name(self) -> str:
        return self.name.title()

    def get_kills(self) -> int:
        return len(self.kills)

    def add_kill(self, enemie:str) -> str:
        self.kills += [enemie]

    def add_move(self, from_pos, to_pos):
        self.moves += [(from_pos, to_pos)]

    def info(self) -> str:
        txt = f"\n--> {self.name.title()}"
        txt += f"\n----> {self.site.name.title()}"
        txt += f"\n----> Kills: {len(self.kills)}"
        for kill in self.kills:
            txt += f"\n--------> {kill}"
        return txt


class Pawn(Chessman):
    def __init__(self, site:site, double_move_activated=False, double_jump_possible=True, kills=[], moves=[]):
        super().__init__(site, chessmen.PAWN, "pawn", kills, moves)
        self.last_move_double_jump = False
        self.double_jump_activated = double_move_activated    # by loading you have to check in moves
        self.double_jump_possible = double_jump_possible
        self.promotion = False

    def get_move_positions(self) -> list:
        if self.site == site.WHITE:
            if self.double_jump_possible and not self.double_jump_activated:
                return [(0, 1, False), (0, 2, False)]
            else:
                return [(0, 1, False)]
        elif self.site == site.BLACK:
            if self.double_jump_possible and not self.double_jump_activated:
                return [(0, -1, False), (0, -2, False)]
            else:
                return [(0, -1, False)]

    def get_attack_positions(self) -> list:
        if self.site == site.WHITE:
            return [(1, 1, False), (-1, 1, False)]
        elif self.site == site.BLACK:
            return [(1, -1, False), (-1, -1, False)]

    def post_attack(self, pos, field):
        self.last_move_double_jump = False

        # check dopple jump
        if self.double_jump_possible:
            self.double_jump_possible = False
            if self.site == site.WHITE:
                if int(pos[1]) == 4:
                    self.last_move_double_jump = True
                    self.double_jump_activated = True
                    # check if en passant is possible -> check both neighbors
                    # self.field.check(-1, 0) and self.field.check(1, 0)
                else:
                    self.double_jump_activated = False
            else:
                if int(pos[1]) == 5:
                    self.last_move_double_jump = True
                    self.double_jump_activated = True
                else:
                    self.double_jump_activated = False
        # check promotion
        if self.site == site.WHITE and int(pos[1]) == 8:
            self.promotion = True
            engine.event = "PROMOTION"
        elif self.site == site.BLACK and int(pos[1]) == 1:
            self.promotion = True
            engine.event = "PROMOTION"

         # check en'passant
        if field[pos].site == site.WHITE and pos[1] == "6":
            if field[pos[0]+'5'] != None and field[pos[0]+'5'].chessman == chessmen.PAWN:
                if field[pos[0]+'5'].last_move_double_jump:
                    self.kills += [field[pos[0]+'5'].name.title()]
                    field[pos[0]+'5'] = None
                    return "White Pawn destroys black Pawn by passing!"
        elif field[pos].site == site.BLACK and pos[1] == "3":
            if field[pos[0]+'4'] != None and field[pos[0]+'4'].chessman == chessmen.PAWN:
                if field[pos[0]+'4'].last_move_double_jump:
                    self.kills += [field[pos[0]+'4'].name.title()]
                    field[pos[0]+'4'] = None
                    return "Black Pawn destroys White Pawn by passing!"


class Rook(Chessman):
    def __init__(self, site:site, kills=[], moves=[]):
        super().__init__(site, chessmen.ROOK, "rook", kills, moves)

    def get_move_positions(self) -> list:
        return [(0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    def get_attack_positions(self) -> list:
        return [(0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    
class Bishop(Chessman):
    def __init__(self, site:site, kills=[], moves=[]):
        super().__init__(site, chessmen.BISHOP, "bishop", kills, moves)

    def get_move_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True)]

    def get_attack_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True)]


class Knight(Chessman):
    def __init__(self, site:site, kills=[], moves=[]):
        super().__init__(site, chessmen.KNIGHT, "knight", kills, moves)

    def get_move_positions(self) -> list:
        return [(1, 2, False), (-1, 2, False), (1, -2, False), (-1, -2, False), (2, 1, False), (-2, 1, False), (2, -1, False), (-2, -1, False)]

    def get_attack_positions(self) -> list:
        return [(1, 2, False), (-1, 2, False), (1, -2, False), (-1, -2, False), (2, 1, False), (-2, 1, False), (2, -1, False), (-2, -1, False)]

        
class Queen(Chessman):
    def __init__(self, site:site, kills=[], moves=[]):
        super().__init__(site, chessmen.QUEEN, "queen", kills, moves)

    def get_move_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True), (0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    def get_attack_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True), (0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]


class King(Chessman):
    def __init__(self, site:site, kills=[], moves=[]):
        super().__init__(site, chessmen.KING, "king", kills, moves)

    def get_move_positions(self) -> list:
        return [(1, 1, False), (-1, 1, False), (1, -1, False), (-1, -1, False), (0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False)]

    def get_attack_positions(self) -> list:
        return [(1, 1, False), (-1, 1, False), (1, -1, False), (-1, -1, False), (0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False)]

    def post_attack(self, pos, field):
        # check rochade
        if self.site == site.WHITE:
            # rochade left execute?
            if len(self.moves) == 1 and self.moves[0] == ('e1', 'c1'):
                field['d1'] = field['a1']
                field['a1'] = None
                field['d1'].add_move('a1', 'd1')
                return "White performs a grand Rochade!"
            elif len(self.moves) == 1 and self.moves[0] == ('e1', 'g1'):    # rochade right execute?
                field['f1'] = field['h1']
                field['h1'] = None
                field['f1'].add_move('h1', 'f1')
                return "White performs a small Rochade!"
        else:
            if len(self.moves) == 1 and self.moves[0] == ('e8', 'c8'):
                field['d8'] = field['a8']
                field['a8'] = None
                field['d8'].add_move('a8', 'd8')
                return "Black performs a grand Rochade!"
            elif len(self.moves) == 1 and self.moves[0] == ('e8', 'g8'):
                field['f8'] = field['h8']
                field['h8'] = None
                field['f8'].add_move('h8', 'f8')
                return "Black performs a small Rochade!"

