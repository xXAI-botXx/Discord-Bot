from copy import deepcopy

import Games.Chess.Engine.chess_men as chess
from Games.Chess.Engine.chess_engine import lines, modes, positions, site, chessmen

class Field(object):
    def __init__(self, field=dict(), moves=[], new_game=True, mode=modes.CLASSIC):
        self.field = field
        self.moves = moves
        self.mode = mode

        self.graveyard_white = []
        self.graveyard_black = []

        if new_game:
            self.create_new_field()

    def create_new_field(self):
        if self.mode == modes.CLASSIC:
            for pos in positions:
                if pos[1] == '2':
                    self.field[pos] = chess.Pawn(site.WHITE, False, True, kills=[], moves=[])
                elif pos[1] == '1':
                    if pos[0] == 'a' or pos[0] == 'h':
                        self.field[pos] = chess.Rook(site.WHITE, kills=[], moves=[])
                    elif pos[0] == 'b' or pos[0] == 'g':
                        self.field[pos] = chess.Knight(site.WHITE, kills=[], moves=[])
                    elif pos[0] == 'c' or pos[0] == 'f':
                        self.field[pos] = chess.Bishop(site.WHITE, kills=[], moves=[])
                    elif pos[0] == 'd':
                        self.field[pos] = chess.Queen(site.WHITE, kills=[], moves=[])
                    elif pos[0] == 'e':
                        self.field[pos] = chess.King(site.WHITE, kills=[], moves=[])
                elif pos[1] == '7':
                    self.field[pos] = chess.Pawn(site.BLACK, False, True, kills=[], moves=[])
                elif pos[1] == '8':
                    if pos[0] == 'a' or pos[0] == 'h':
                        self.field[pos] = chess.Rook(site.BLACK, kills=[], moves=[])
                    elif pos[0] == 'b' or pos[0] == 'g':
                        self.field[pos] = chess.Knight(site.BLACK, kills=[], moves=[])
                    elif pos[0] == 'c' or pos[0] == 'f':
                        self.field[pos] = chess.Bishop(site.BLACK, kills=[], moves=[])
                    elif pos[0] == 'd':
                        self.field[pos] = chess.Queen(site.BLACK, kills=[], moves=[])
                    elif pos[0] == 'e':
                        self.field[pos] = chess.King(site.BLACK, kills=[], moves=[])
                else:
                    self.field[pos] = None

    def move(self, field, from_pos, to_pos) -> tuple:
        """executes a move (if possible) directly on the field.\n 
           Returns if the turn has been executed"""
        messages = ""
        if to_pos in self.valid_moves(field, from_pos):
            # check if danger the king
            new_field = self.move_without_changes(field, from_pos, to_pos)
            x_ = self.field['e1']
            if not self.is_check(new_field, field[from_pos].site):
                if field[to_pos] != None:
                    field[from_pos].add_kill(field[to_pos].get_name())
                    if field[to_pos].site == site.WHITE:
                        self.graveyard_white += [field[to_pos]]
                        messages += f"\nBlack {field[from_pos].get_name()} defeats white {field[to_pos].get_name()}"
                    else:
                        self.graveyard_black += [field[to_pos]]
                        messages += f"\nWhite {field[from_pos].get_name()} defeats black {field[to_pos].get_name()}"
                        
                    if field[from_pos].get_kills() == 3:
                        messages += f"\n{field[from_pos].get_name()} is heroic."
                    elif field[from_pos].get_kills() == 4:
                        messages += f"\n{field[from_pos].get_name()} will kill'em all."
                    elif field[from_pos].get_kills() == 5:
                        messages += f"\n{field[from_pos].get_name()} is unstoppable."
                    elif field[from_pos].get_kills() == 6:
                        messages += f"\n{field[from_pos].get_name()} is a legend!"

                field[to_pos] = field[from_pos]
                field[from_pos] = None

                # post attack
                field[to_pos].add_move(from_pos, to_pos)
                if field[to_pos].chessman == chessmen.PAWN:
                    m = field[to_pos].post_attack(to_pos, field)
                    if type(m) == str:
                        messages += "\n"+m+"\n"
                elif field[to_pos].chessman == chessmen.KING:
                    m = field[to_pos].post_attack(to_pos, field)
                    if type(m) == str:
                        messages += "\n"+m+"\n"
                self.moves += [(from_pos, to_pos)]
                return (True, messages)
            else:
                messages += "\nYou have to make the safety of your king sure!"
                return (False, messages)
        else:
            return (False, messages)

    def move_without_changes(self, field, from_pos, to_pos) -> dict:
        """executes a turn on a new map and returns that map"""
        # all objects (the chessmen) have to be copies!!!
        copy_field = deepcopy(field)
        if to_pos in self.valid_moves(field, from_pos):
            if copy_field[to_pos] != None:
                #copy_field[from_pos].add_kill(copy_field[to_pos].get_name())
                if copy_field[to_pos].site == site.WHITE:
                    self.graveyard_white += [copy_field[to_pos]]
                else:
                    self.graveyard_black += [copy_field[to_pos]]

            copy_field[to_pos] = copy_field[from_pos]
            copy_field[from_pos] = None
            # post attack
            if copy_field[to_pos].chessman == chessmen.PAWN:
                copy_field[to_pos].post_attack(to_pos, copy_field)
            #self.moves += [(from_pos, to_pos)]
            return copy_field
        else:
            return None

    def valid_moves(self, field, pos) -> list:    # the new pos have to be in move-set or in attack-set -> but there have to be a enemy
        if field[pos] == None:
            return []
        else:
            valid_moves = []
            moves = field[pos].get_move_positions()
            for x, y, endless in moves:
                if endless:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]])
                    new_y = int(pos[1])
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[new_x]+x)
                        new_y += y
                        if new_x != None:
                            new_pos = f"{new_x}{new_y}"
                            # position in field
                            if new_pos in positions:
                                # field is free
                                if field[new_pos] == None:
                                    # if not added in possible moves
                                    if new_pos not in valid_moves:
                                        valid_moves += [new_pos]
                                else:
                                    break
                            else:
                                break
                        else:
                            break
                else:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                    if new_x != None:
                        new_pos = f"{new_x}{int(pos[1])+y}"
                        # position in field
                        if new_pos in positions:
                            # field is free
                            if field[new_pos] == None:
                                # if not added in possible moves
                                if new_pos not in valid_moves:
                                    valid_moves += [new_pos]

            attacks = field[pos].get_attack_positions()
            for x, y, endless in attacks:
                if endless:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]])
                    new_y = int(pos[1])
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[new_x]+x)
                        new_y += y
                        if new_x != None:
                            new_pos = f"{new_x}{new_y}"
                            # position in field
                            if new_pos in positions:
                                # field is enemy
                                if field[new_pos] != None:
                                    if field[new_pos].site != field[pos].site:
                                        # if not added in possible moves
                                        if new_pos not in valid_moves:
                                            valid_moves += [new_pos]
                                            break
                                    else:
                                        break
                                else:
                                    pass
                            else:
                                break
                        else:
                            break
                else:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                    if new_x != None:
                        new_pos = f"{new_x}{int(pos[1])+y}"
                        # position in field
                        if new_pos in positions:
                            # field is enemy
                            if field[new_pos] != None and field[new_pos].site != field[pos].site:
                                # if not added in possible moves
                                if new_pos not in valid_moves:
                                    valid_moves += [new_pos]
            # check doople jump -> no chessman?
            if field[pos].chessman == chessmen.PAWN:
                if field[pos].site == site.WHITE and pos[1] == "2":
                    if field[pos].double_jump_possible and field[pos[0]+"3"] != None:
                        valid_moves.remove(pos[0]+"4")    # inplace change (mit seiteneffekt)
                elif field[pos].site == site.BLACK and pos[1] == "7":
                    if field[pos].double_jump_possible and field[pos[0]+"6"] != None:
                        valid_moves.remove(pos[0]+"5")    # inplace change (mit seiteneffekt)
            # check en_passant
            if field[pos].chessman == chessmen.PAWN:
                if field[pos].site == site.WHITE and pos[1] == "5":
                # if one neighbor, which use his double jump
                    if pos[0] == 'a':
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]+1)+str(int(pos[1])+1)
                            valid_moves += [new_pos]
                    elif pos[0] == 'h':
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]-1)+str(int(pos[1])+1)
                            valid_moves += [new_pos]
                    else:
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]+1)+str(int(pos[1])+1)
                            valid_moves += [new_pos]
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]-1)+str(int(pos[1])+1)
                            valid_moves += [new_pos]
                elif field[pos].site == site.BLACK and pos[1] == "4":
                    if pos[0] == 'a':
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]+1)+str(int(pos[1])-1)
                            valid_moves += [new_pos]
                    elif pos[0] == 'h':
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]-1)+str(int(pos[1])-1)
                            valid_moves += [new_pos]
                    else:
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]+1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]+1)+str(int(pos[1])-1)
                            valid_moves += [new_pos]
                        if self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]] != None and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].chessman == chessmen.PAWN and \
                            self.field[self.numerical_field_to_alphabetic(lines[pos[0]]-1)+pos[1]].last_move_double_jump:
                            new_pos = self.numerical_field_to_alphabetic(lines[pos[0]]-1)+str(int(pos[1])-1)
                            valid_moves += [new_pos]

            # check rochade
            if field[pos].chessman == chessmen.KING and len(field[pos].moves) == 0:
                if field[pos].site == site.WHITE:
                    # check rochade with left rook
                    if field['a1'] != None and field['a1'].chessman == chessmen.ROOK and len(field['a1'].moves) == 0:
                        if field['b1'] == None and field['c1'] == None and field['d1'] == None:
                            valid_moves += ['c1']
                    # check rochade with right rook
                    if field['h1'] != None and field['h1'].chessman == chessmen.ROOK and len(field['h1'].moves) == 0:
                        if field['f1'] == None and field['g1'] == None:
                            valid_moves += ['g1']
                elif field[pos].site == site.BLACK:
                     # check rochade with left rook
                    if field['a8'] != None and field['a8'].chessman == chessmen.ROOK and len(field['a8'].moves) == 0:
                        if field['b8'] == None and field['c8'] == None and field['d8'] == None:
                            valid_moves += ['c8']
                    # check rochade with right rook
                    if field['h8'] != None and field['h8'].chessman == chessmen.ROOK and len(field['h8'].moves) == 0:
                        if field['f8'] == None and field['g8'] == None:
                            valid_moves += ['g8']

            return valid_moves

    def numerical_field_to_alphabetic(self, num:int):
        try:
            return {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}[num]
        except KeyError:
            return None

    def get_field(self) -> dict:
        return self.field

    def king_pos(self, field, site):
        for pos in positions:
            if field[pos] != None:
                if field[pos].chessman == chessmen.KING and field[pos].site == site:
                    return pos

    def is_check(self, field, site) -> bool:
        """Checks if the givin site is in check"""
        king_pos = self.king_pos(field, site)
        if king_pos != None:
            for pos in positions:
                if field[pos] != None and field[pos].site != site:
                    if king_pos in self.valid_moves(field, pos):
                        return True
            return False
        else:
            pass
            # no king

    # is working? -> or false used
    def is_check_mate(self, field:dict, site) -> bool:
        """Checks if the givin site is in checkmate"""
        # is there no legal move without dangerous the king?
        king_pos = self.king_pos(field, site)
        if king_pos != None:
            # search a turn which endanger the king
            for pos in positions:
                    if field[pos] != None and field[pos].site == site:
                        for to_pos in self.valid_moves(field, pos):
                            copy_field = self.move_without_changes(field, pos, to_pos)
                            if not self.is_check(copy_field, site):
                                return False
            return True
        else:
            pass
            # no king

    def is_there_a_legal_turn(self, check_site):
        for pos in positions:
            if self.field[pos] != None and self.field[pos].site == check_site:
                for to_pos in self.valid_moves(self.field, pos):
                    copy_field = self.move_without_changes(self.field, pos, to_pos)
                    if not self.is_check(copy_field, check_site):
                        return True
        return False

    def get_opposite_site(self, op_site):
        if op_site == site.WHITE:
            return site.BLACK
        else:
            return site.WHITE

    def upgrade_pawn(self, new_chessman, site):
        global event
        # find pawn
        pawn_pos = None
        kills = []
        for pos in positions:
            if self.field[pos] != None and self.field[pos].chessman == chessmen.PAWN and self.field[pos].promotion == True:
                pawn_pos = pos
                kills = self.field[pos].kills
        if pawn_pos == None:
            return (0, "Pawn not found.")
        else:
            # replace pawn with ne chessman
            self.field[pawn_pos] = self.convert_chessmen_to_chessman(new_chessman, site, kills)
            self.moves += [(pawn_pos, new_chessman.name.upper())]
            return (1, f"Pawn replaced with {new_chessman.name.title()}")

    def convert_chessmen_to_chessman(self, to_convert, site, kills) -> chess.Chessman:
        """Converts a Chessmen-Enum-State into a real Chessman"""
        if to_convert == chessmen.PAWN:
            return chess.Pawn(site, kills=kills)
        elif to_convert == chessmen.ROOK:
            return chess.Rook(site, kills=kills)
        elif to_convert == chessmen.KNIGHT:
            return chess.Knight(site, kills=kills)
        elif to_convert == chessmen.BISHOP:
            return chess.Bishop(site, kills=kills)
        elif to_convert == chessmen.QUEEN:
            return chess.Queen(site, kills=kills)
        elif to_convert == chessmen.KING:
            return chess.King(site, kills=kills)
