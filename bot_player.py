import discord
from discord.utils import get
from datetime import datetime
import sys
import os
import random
import time
import threading
import asyncio
from enum import Enum
import Games.Chess.Engine.chess_engine as engine
import Games.Chess.Engine.chess_men as pieces

emojis = [":relieved:", ":upside_down:", ":kissing_heart:", ":relaxed:", ":exploding_head:", ":face_in_clouds:", ":hugging:", ":expressioness:", ":rolling_eyes:", ":face_vomiting:", ":robot:", ":metal:", ":pinched_fingers:", ":raised_hands:", ":middle_finger:", ":lipstick:", ":eyes:", ":tongue:", ":baby:", ":farmer:", ":man_detective:", ":student:", ":teacher:", ":technologist:", ":office_worker:", ":man_astronaut:", ":ninja:", ":man_superhero:", ":man_mage:", ":man_elf:", ":man_vampire:", ":man_zombie:", ":mermaid:", ":pregnant_woman:", ":man_bowing:", ":man_gesturing_no:", ":man_facepalming:", ":man_gesturing_ok:", ":man_in_manual_wheelchair:", ":man_running:", ":bikini:", ":yarn:", ":crown:", ":socks:", ":dog:", ":cat:", ":mouse:", ":tiger:", ":lion_face_:", ":pig:", ":frog:", ":monkey:", ":penguin:", ":bird:", ":hatching_chick:", ":eagle:", ":bat:", ":unicorn:", ":bee:", ":t_rex:", ":sauropod:", ":turtle:", ":snake:", ":shark:", ":fish:", ":kangaroo:", ":dove:", ":sloth:", ":chipmunk:", ":dragon:", ":feather:", ":ringed_planet:", ":full_moon_with_face:", ":earth_americas:", ":snowman:", ":maple_leaf:", ":sunflower:", ":banana:", ":strawberry:", ":poultry_leg:", ":hotdog:", ":hamburger:", ":pizza:", ":taco:", ":burrito:", ":ramen:", ":birthday:", ":doghnut:", ":archery:", ":parachute:", ":man_cartwheeling:", ":person_in_lotus_position:", ":volcano:", ":compass:", ":desktop:", ":axe:", ":smoking:", ":pill:", ":dna:", ":heart:", ":cupid:", ":radioactive:", ":musical_note:", ":purple_circle:", ":green_circle:", ":yellow_circle:", ":small_orange_diamond:", ":small_blue_diamond:", ":dash:", ":flushed:", ":eyes:", ":ok_hand_tone4:", ":pinched_fingers_tone5:", ":nose_tone5:", ":baby_tone5:", ":pinching_hand_tone5:", ":call_me_tone5:", ":middle_finger_tone5:", ":man_gesturing_no_tone5:", ":man_gesturing_ok_tone5:", ":disguised_face:", ":joy:", ":crying_cat_face:", ":person_in_motorized_wheelchair_tone5:"]
bg_emojis = [":ice_cube:", ":classical_building:", ":shinto_shrine:", ":window:", ":cyclone:", ":parking:", ":free:", ":orange_square:", ":blue_square:", ":red_square:", ":purple_square:", ":green_square:", ":yellow_square:"]
win_emojis = [":star:", ":zap:", ":rainbow:", ":boom:", ":dizzy:", ":sparkles:", ":ocean:", ":cherries:", ":dart:", ":dvd:"]

class SchereSteinPapier():
    def __init__(self, bot, channel):
        self.GameState = Enum("GameState", "PLAYERCHOICE RUNNING COMPLETED")
        self.state = self.GameState.PLAYERCHOICE
        self.players = []
        self.match = 0
        self.computer = False
        self.result = dict()
        self.bot = bot
        self.channel = channel

    async def commander(self, message):
        if str(message.guild
                ) == "None" and message.author != self.bot.user:  #bot.user
            if self.get_state() == "RUNNING":
                await self.add_input(str(message.author),
                                        message.content.lower(),
                                        Bot_xX_Player_Xx.MAIN_CHANNEL)
        elif str(message.guild
                    ) != "None" and message.author != self.bot.user:  # bot.user
            if message.content.lower().split(" ")[0] in [
                "begin", "play", "start"
            ]:
                if len(self.get_player()) >= 2 or (len(self.get_player()) == 1
                                                    and self.get_computer()):
                    if self.get_state() == "PLAYERCHOICE" or self.get_state(
                    ) == "COMPLETED":
                        await self.play(message.channel)
                else:
                    await message.channel.send("There are not enough players.")
            elif self.bot.check_startswith(
                message.content.lower(),
                ["ki on", "ai on", "bot on", "com", "player too"]):
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_self()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower().split()[0] == "ich":
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_player(str(message.author), message.channel)
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")

    async def add_player(self, name, channel):
        name = name[:-5]
        if name not in self.players:
            if name not in self.players:
                await channel.send(f"{name} has joined the game :tickets:")
                self.players += [name]
        else:
            await self.channel.send(f"{name} don't play with you anymore.")
            self.players = self.players.remove(name)
            if self.players == None:
                self.players = []

    async def add_self(self):
        if self.computer != True:
            self.computer = True
            self.players += ["computer"]
            await self.channel.send("I'm playing with you.")
        else:
            await self.channel.send("Computer don't play with you anymore.")
            self.players = self.players.remove("computer")
            self.computer = False
            if self.players == None:
                self.players = []

    async def add_input(self, author, vote, channel):
        author = author[:-5]
        if self.state.name == "RUNNING":
            if vote.strip() == "📄":
                vote = "papier"
            elif vote.strip() == "✂️":
                vote = "schere"
            elif vote.strip() == "🪨":
                vote = "stein"
            if self.result.get(author) == None and vote.strip() in [
                "schere", "stein", "papier", ":scissors:", ":rock:",
                ":page_facing_up:"
            ]:
                self.result[author] = vote
                await channel.send(
                    f"Alright. Your decision is logged in :thumbsup:")
                await self.channel.send(f"{author} has made his move.")
                # checking complete
                if len(self.result.keys()) == len(self.players):
                    await self.complete(self.channel)

    def get_player(self):
        return self.players

    def get_state(self):
        return self.state.name

    def get_computer(self):
        return self.computer

    async def play(self, channel):
        self.state = self.GameState.RUNNING
        txt = ":tada: Lasst die Spiele beginnen! :confetti_ball:\n\nMatch: " + str(
            self.match+1
        ) + "\n\nSchreibe mir eine private Nachricht 'schere', 'stein' oder 'papier'.\n Oder sendet mir einer folgenden Smileys:\n:scissors:\n:rock:\n:page_facing_up:"
        # auch smileys möglich?
        await channel.send(txt)
        self.result = dict()
        if self.computer:
            vote = random.choice(["schere", "stein", "papier"])
            self.result["computer"] = vote

    async def complete(self, channel):
        self.match += 1
        self.state = self.GameState.COMPLETED
        await channel.send(
            "--------\nAlle Eingaben wurden getätigt. Lasst die Auswertung beginnen:\n\n"
        )
        for i in self.result.items():
            if i[1] in ["schere", ":scissors:"]:  #smiley hinzufügen
                vote = "**Schere** :scissors:"
            elif i[1] in ["stein", ":rock:"]:
                vote = "**Stein** :rock:"
            else:
                vote = "**Papier** :page_facing_up:"
            await channel.send(f"--------> {i[0]} hat {vote}")
        # Gewinner errechnen !
        await self.resulting(channel)

    async def resulting(self, channel):
        await channel.send("--------\nCalculating the results...")
        point_map_schere = {"schere": 1, "papier": 0, "stein": 2}
        point_map_stein = {"schere": 0, "papier": 2, "stein": 1}
        point_map_papier = {"schere": 2, "papier": 1, "stein": 0}
        points = dict()
        player = []
        for player_name, choice in self.result.items():
            points[player_name] = 0
            if choice == ":scissors:":
                choice = "schere"
            elif choice == ":rock:":
                choice = "stein"
            elif choice == ":page_facing_up:":
                choice = "papier"
            player += [(player_name, choice)]

        for i in range(len(self.result.keys())):
            for j in range(i + 1, len(self.result.keys())):
                if player[i][1] == "schere":
                    if point_map_schere["schere"] > point_map_schere[player[j]
                                                                        [1]]:
                        points[player[i][0]] += 1
                    elif point_map_schere["schere"] < point_map_schere[
                        player[j][1]]:
                        points[player[j][0]] += 1
                elif player[i][1] == "stein":
                    if point_map_stein["stein"] > point_map_stein[player[j]
                                                                    [1]]:
                        points[player[i][0]] += 1
                    elif point_map_stein["stein"] < point_map_stein[player[j]
                                                                    [1]]:
                        points[player[j][0]] += 1
                elif player[i][1] == "papier":
                    if point_map_papier["papier"] > point_map_papier[player[j]
                                                                        [1]]:
                        points[player[i][0]] += 1
                    elif point_map_papier["papier"] < point_map_papier[
                        player[j][1]]:
                        points[player[j][0]] += 1
                else:
                    print(
                        "\nFehler: Ein anderer Wert als Schere, Stein oder Papier wurde gefunden und zwar:",
                        player[i][1])
        # sort player and add placement
        sorted_results = sorted(points.items(),
                                key=lambda x: x[1],
                                reverse=True)
        results = []
        placement = 1
        last_points = None
        for player, points in sorted_results:
            if last_points == None:
                results += [(player, points, placement)]
                last_points = points
            else:
                if last_points > points:
                    placement += 1
                    results += [(player, points, placement)]
                    last_points = points
                else:
                    results += [(player, points, placement)]
                    last_points = points

        # printing results
        for player, points, placement in results:
            if placement == 1:
                await channel.send(
                    f":tada: {placement}.Platz {player} mit {points} Punkten :tada:"
                )
            else:
                await channel.send(
                    f"{placement}.Platz {player} mit {points} Punkten")


class TicTacToe():
    def __init__(self, bot, channel):
        self.GameState = Enum("GameState", "PLAYERCHOICE RUNNING COMPLETED")
        self.state = self.GameState.PLAYERCHOICE
        self.turn = 0
        self.player_turn = 0
        self.players = []
        self.match = 0
        self.computer = False
        self.channel = channel
        self.bot = bot
        self.field = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    async def commander(self, message):
        if str(message.guild
                ) == "None" and message.author != self.bot.user:  #bot.user
            pass
        elif str(message.guild) != "None" and message.author != self.bot.user:
            if message.content.lower().split()[0] == "ich":
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_player(str(message.author), message.channel)
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower().split(" ")[0] in [
                "begin", "play", "start"
            ]:
                if len(self.get_player()) == 2:
                    if self.get_state() == "PLAYERCHOICE" or self.get_state(
                    ) == "COMPLETED":
                        await self.play(message.channel)
                else:
                    await message.channel.send("There are not enough players.")
            elif message.content.lower() in [
                "ki on", "ai on", "bot on", "com", "player too"
            ]:
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_self()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["field", "f"]:
                if self.get_state() == "RUNNING":
                    await self.show_field()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["current field", "cf"]:
                if self.get_state() == "RUNNING":
                    await self.show_current_field()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["player", "mitspieler"]:
                if self.get_state() == "RUNNING":
                    await self.show_player()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["?", "cp"]:
                if self.get_state() == "RUNNING":
                    await self.get_current_player()
            elif len(message.content.lower()) == 1 and message.content.lower().isdigit():
                if self.get_state() == "RUNNING":
                    await self.make_turn(message.content)

    async def add_player(self, name, channel):
        name = name[:-5]
        if name not in self.players:
            if len(self.players) < 2:
                if name not in self.players:
                    await channel.send(f"{name} has joined the game :tickets:")
                    self.players += [name]
            else:
                await self.channel.send("There are to enough player.")
        else:
            await self.channel.send(f"{name} don't play with you anymore.")
            self.players = self.players.remove(name)
            if self.players == None:
                self.players = []

    async def add_self(self):
        if self.computer != True:
            if len(self.players) < 2:
                self.computer = True
                self.players += ["computer"]
                await self.channel.send("I'm playing with you.")
            else:
                await self.channel.send("There are to enough player.")
        else:
            await self.channel.send("Computer don't play with you anymore.")
            self.players = self.players.remove("computer")
            self.computer = False
            if self.players == None:
                self.players = []

    def get_player(self):
        return self.players

    def get_state(self):
        return self.state.name

    def get_computer(self):
        return self.computer

    async def get_current_player(self):
        await self.channel.send(
            f"{self.players[self.player_turn]} should make his turn...")

    async def show_field(self):
        field = ""
        for i in range(1, 10):
            if i in [3, 6, 9]:
                field += f" | {i} |\n"
            elif i in [4, 7]:
                field += f"| {i}"
            else:
                field += f" | {i}"
        await self.channel.send(field)

    async def show_current_field(self):
        field = ""
        for i in range(1, 10):
            if i in [3, 6, 9]:
                row, column = self.numb_to_row_column(i)
                if self.field[row][column] == "-":
                    field += f" |    |\n"
                else:
                    field += f" | {self.field[row][column]} |\n"
            elif i in [4, 7]:
                row, column = self.numb_to_row_column(i)
                if self.field[row][column] == "-":
                    field += f"|   "
                else:
                    field += f"| {self.field[row][column]}"
            else:
                row, column = self.numb_to_row_column(i)
                if self.field[row][column] == "-":
                    field += f" |   "
                else:
                    field += f" | {self.field[row][column]}"
        await self.channel.send(field)

    async def computer_turn(self):
        l = [1,2,3,4,5,6,7,8,9]
        tries = random.sample(l, k=9)
        i = 0
        while self.field[self.numb_to_row_column(tries[i])[0]][self.numb_to_row_column(tries[i])[1]] != "-":
            i += 1
        # gut so?
        time.sleep(2)
        await self.make_turn(str(tries[i]))

    async def show_player(self):
        txt = ""
        for i in range(len(self.players)):
            if i == 0:
                txt += f"x = {self.players[i]}"
            else:
                txt += f"o = {self.players[i]}"
        self.channel.send("txt")

    def numb_to_row_column(self, n: int):
        if n in [1, 4, 7]:
            row = 0
        elif n in [2, 5, 8]:
            row = 1
        elif n in [3, 6, 9]:
            row = 2
        if n >= 1 and n <= 3:
            column = 0
        elif n >= 4 and n <= 6:
            column = 1
        elif n >= 7 and n <= 9:
            column = 2
        return (row, column)

    async def play(self, channel):
        self.state = self.GameState.RUNNING
        if self.match == 0:
            txt = ":tada: Lasst die Spiele beginnen! :confetti_ball:\nZu Beginn wähle ich die Reihenfolge der Spieler aus.\n(Außerdem kannst du dir mit 'cf' das aktuelle Spielfeld ausgeben lassen und mit 'field', die Numerierung des Spielfeldes und mit 'mitspieler', die Spieler)."
            # auch smileys möglich?
            await channel.send(txt)

            x = random.randint(0, 1)
            o = abs(x - 1)

            if x != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[
                    1], self.players[0]

            await self.channel.send(
                f"x = {self.players[0]}\no = {self.players[1]}. \n\nPlayer x write a number from 1-9, to make the first turn. (With '?' you can get the Player of the current turn)"
            )

            await self.show_current_field()

            if self.players[0] == 'computer':
                await self.computer_turn()
        else:
            self.field = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
            self.player_turn = 0
            await channel.send(f"Let's start the {self.match+1}. match!")
            x = random.randint(0, 1)
            o = abs(x - 1)

            if x != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[1], self.players[0]

            await self.channel.send(
                f"x = {self.players[0]}\no = {self.players[1]}. \n\nPlayer x write a number from 1-9, to make the first turn. (with '?' you can get the Player of the current turn)"
            )

            if self.players[0] == 'computer':
                await self.computer_turn()

    async def make_turn(self, content):
        try:
            pos = int(content)
            if pos >= 1 and pos <= 9:
                row, column = self.numb_to_row_column(pos)
                if self.field[row][column] == "-":
                    sign = ["x", "o"][self.player_turn]
                    self.field[row][column] = sign
                    await self.channel.send(
                        f"{self.players[self.player_turn]} has taken {pos}."
                    )
                    await self.show_current_field()
                    await self.check_winning()
                    if self.get_state(
                    ) == "RUNNING":  # wenn spiel nicht fertig ist
                        self.player_turn = abs(self.player_turn - 1)
                        await self.channel.send(
                            f"{self.players[self.player_turn]} make your turn")
                        if self.players[self.player_turn] == 'computer':
                            await self.computer_turn()
            else:
                await self.channel.send(
                    "You have to call a number between [1-9].")
        except:
            print("It wasn't a number.")

    async def check_winning(self):
        # check if x win
        # ----> check rows
        for row in self.field:
            if row[0] == "x" and row[1] == "x" and row[2] == "x":
                self.state = self.GameState.COMPLETED
                await self.channel.send(
                    f":tada: {self.players[0]} hat gewonnen :tada:")
                self.match += 1
                return
        # ----> check columns
        for column in range(3):
            if self.field[0][column] == "x" and self.field[1][
                column] == "x" and self.field[2][column] == "x":
                self.state = self.GameState.COMPLETED
                await self.channel.send(
                    f":tada: {self.players[0]} hat gewonnen :tada:")
                self.match += 1
                return
        # ----> check quer
        if self.field[0][0] == "x" and self.field[1][1] == "x" and self.field[
            2][2] == "x":
            self.state = self.GameState.COMPLETED
            await self.channel.send(
                f":tada: {self.players[0]} hat gewonnen :tada:")
            self.match += 1
            return
        if self.field[0][2] == "x" and self.field[1][1] == "x" and self.field[
            2][0] == "x":
            self.state = self.GameState.COMPLETED
            await self.channel.send(
                f":tada: {self.players[0]} hat gewonnen :tada:")
            self.match += 1
            return
        # check if o win
        # ----> check rows
        for row in self.field:
            if row[0] == "o" and row[1] == "o" and row[2] == "o":
                self.state = self.GameState.COMPLETED
                await self.channel.send(
                    f":tada: {self.players[1]} hat gewonnen :tada:")
                self.match += 1
                return
        # ----> check columns
        for column in range(3):
            if self.field[0][column] == "o" and self.field[1][
                column] == "o" and self.field[2][column] == "o":
                self.state = self.GameState.COMPLETED
                await self.channel.send(
                    f":tada: {self.players[1]} hat gewonnen :tada:")
                self.match += 1
                return
        # ----> check quer
        if self.field[0][0] == "o" and self.field[1][1] == "o" and self.field[
            2][2] == "o":
            self.state = self.GameState.COMPLETED
            await self.channel.send(
                f":tada: {self.players[1]} hat gewonnen :tada:")
            self.match += 1
            return
        if self.field[0][2] == "o" and self.field[1][1] == "o" and self.field[
            2][0] == "o":
            self.state = self.GameState.COMPLETED
            await self.channel.send(
                f":tada: {self.players[1]} hat gewonnen :tada:")
            self.match += 1
            return
        # check if the field is full
        free = 0
        for row in self.field:
            if "-" in row:
                free += 1
        if free == 0:
            self.state = self.GameState.COMPLETED
            await self.channel.send(f"Untenschieden!")
            self.match += 1


class FourWins():
    def __init__(self, bot, channel):
        self.GameState = Enum("GameState", "PLAYERCHOICE RUNNING COMPLETED")
        self.state = self.GameState.PLAYERCHOICE
        self.turn = 0
        self.player_turn = 0
        self.players = []
        self.match = 0
        self.computer = False
        self.channel = channel
        self.bot = bot
        self.make_field()
        self.win_pos = []
        self.x = ":cat:"
        self.x = ":blue_circle:"
        self.o = ":dog:"
        self.o = ":red_circle:"
        self.nothing = ":fog:"
        self.nothing = ":white_medium_square:"
        self.nothing = ":black_medium_square:"
        self.win = ":dizzy:"
        self.random_icons = False

    def make_field(self):
        field = []
        for i in range(6):
            row = []
            for j in range(7):
                row += ["-"]
            field += [row]
        self.field = field

    async def commander(self, message):
        if str(message.guild) == "None" and message.author != self.bot.user:  #bot.user
            pass
        elif str(message.guild) != "None" and message.author != self.bot.user:
            if message.content.lower().split()[0] == "ich":
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_player(str(message.author), message.channel)
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower().split(" ")[0] in [
                "begin", "play", "start"
            ]:
                if len(self.get_player()) == 2:
                    if self.get_state() == "PLAYERCHOICE" or self.get_state(
                    ) == "COMPLETED":
                        await self.play(message.channel)
                else:
                    await message.channel.send("There are not enough players.")
            elif message.content.lower() in [
                "ki on", "ai on", "bot on", "com", "player too"
            ]:
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_self()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["current field", "cf", "field", "f"]:
                if self.get_state() == "RUNNING":
                    await self.show_current_field()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["player", "mitspieler"]:
                if self.get_state() == "RUNNING":
                    await self.show_player()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["?", "cp"]:
                if self.get_state() == "RUNNING":
                    await self.get_current_player()
            elif message.content.lower() in ["icon", "icons", "i", "crazy mode", "i mode"]:
                if self.get_state() == "PLAYERCHOICE":
                    self.random_icons = True
                    await message.channel.send("Crazy mode activated :zany_face:. The Icons will be random.")
            elif len(message.content.lower()) == 1 and message.content.lower().isdigit():
                if self.get_state() == "RUNNING":
                    if self.players[self.player_turn] == str(message.author)[:-5]:
                        await self.make_turn(message.content)
                    else:
                        await message.channel.send(f"chill {str(message.author)[:-5]}... it's not your turn!")

    async def add_player(self, name, channel):
        name = name[:-5]
        if name not in self.players:
            if len(self.players) < 2:
                if name not in self.players:
                    await channel.send(f"{name} has joined the game :tickets:")
                    self.players += [name]
            else:
                await self.channel.send("There are to enough player.")
        else:
            await self.channel.send(f"{name} don't play with you anymore.")
            self.players = self.players.remove(name)
            if self.players == None:
                self.players = []

    async def add_self(self):
        if self.computer != True:
            if len(self.players) < 2:
                self.computer = True
                self.players += ["computer"]
                await self.channel.send("I'm playing with you.")
            else:
                await self.channel.send("There are to enough player.")
        else:
            await self.channel.send("Computer don't play with you anymore.")
            self.players = self.players.remove("computer")
            self.computer = False
            if self.players == None:
                self.players = []

    #async def set_icon(self, message):
    #    author = str(message.author)[:-5]
    #    icon = message.content.split(" ")[2]
    #    if icon in discord.emoji:
    #        pass

    async def set_random_icon(self, message):
        x, o = random.sample(emojis, 2)
        self.x = x
        self.o = o
        await message.channel.send(f"x = {x}\no = {o}")

    async def set_random_background(self, message):
        bg = random.sample(emojis, 1)
        self.nothing = bg
        await message.channel.send(f"background = {bg}")

    async def set_random_icons(self, channel):
        x, o = random.sample(emojis, 2)
        bg = random.choice(bg_emojis)
        win = random.choice(win_emojis)
        self.x = x
        self.o = o
        self.nothing = bg
        self.win = win
        await channel.send(f"x = {x}\no = {o}\nbackground = {bg}\nwin emojis = {win}")

    def get_player(self):
        return self.players

    def get_state(self):
        return self.state.name

    def get_computer(self):
        return self.computer

    async def get_current_player(self):
        await self.channel.send(
            f"{self.players[self.player_turn]} should make his turn...")

    async def show_current_field(self):
        field = f"Turn: {self.turn}\n"
        
        x = self.x
        o = self.o
        nothing = self.nothing
        win = self.win
        
        for i in range(6):
            for j in range(7):
                if j == 6:
                    if (i,j) in self.win_pos:
                        field += f"{win}\n"
                    elif self.field[i][j] == "-":
                        field += f"{nothing}\n"
                    elif self.field[i][j] == "x":
                        field += f"{x}\n"
                    elif self.field[i][j] == "o":
                        field += f"{o}\n"
                elif j == 0:
                    if (i,j) in self.win_pos:
                        field += f"{win}"
                    elif self.field[i][j] == "-":
                        field += f"{nothing}"
                    elif self.field[i][j] == "x":
                        field += f"{x}"
                    elif self.field[i][j] == "o":
                        field += f"{o}"
                else:
                    if (i,j) in self.win_pos:
                        field += f"{win}"
                    elif self.field[i][j] == "-":
                        field += f"{nothing}"
                    elif self.field[i][j] == "x":
                        field += f"{x}"
                    elif self.field[i][j] == "o":
                        field += f"{o}"

        #for i in range(7):
        #    field += f"  {i+1}  "
        field += ":one::two::three::four::five::six::seven:"
        await self.channel.send(field)

    async def computer_turn(self):
        l = [1,2,3,4,5,6,7]
        tries = random.sample(l, k=7)
        i = 0
        while self.is_column_full(tries[i]-1):
            i += 1
        # gut so?
        time.sleep(2)
        await self.make_turn(str(tries[i]))

    async def show_player(self):
        txt = ""
        for i in range(len(self.players)):
            if i == 0:
                txt += f"x = {self.players[i]}"
            else:
                txt += f"o = {self.players[i]}"
        self.channel.send("txt")

    def is_column_full(self, n: int) -> bool:
        if self.field[0][n] == "-":
            return False
        else:
            return True

    def get_pos(self, n:int) -> tuple:
        for i in range(5, -1, -1):
            if self.field[i][n] == "-":
                return (i, n)

    async def play(self, channel):
        self.state = self.GameState.RUNNING
        if self.random_icons:
            await self.set_random_icons(channel)
        if self.match == 0:
            txt = ":tada: Lasst das 4 gewinnt battle starten! :confetti_ball:\nZu Beginn wähle ich die Reihenfolge der Spieler aus.\n(Außerdem kannst du dir mit 'cf' das aktuelle Spielfeld ausgeben lassen und mit 'mitspieler', die Spieler)."
            # auch smileys möglich?
            await channel.send(txt)

            x = random.randint(0, 1)
            o = abs(x - 1)

            if x != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[
                    1], self.players[0]

            await self.channel.send(
                f"x = {self.players[0]}\no = {self.players[1]}. \n\nPlayer x write a number from 1-7, to make the first turn. (With '?' you can get the Player of the current turn)"
            )

            await self.show_current_field()

            if self.players[0] == 'computer':
                await self.computer_turn()
        else:
            self.make_field()
            self.win_pos = []
            self.player_turn = 0
            await channel.send(f"Let's start the {self.match+1}. match!")
            x = random.randint(0, 1)
            o = abs(x - 1)

            if x != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[1], self.players[0]

            await self.channel.send(
                f"x = {self.players[0]}\no = {self.players[1]}. \n\nPlayer x write a number from 1-7, to make the first turn. (With '?' you can get the Player of the current turn)"
            )

            await self.show_current_field()

            if self.players[0] == 'computer':
                await self.computer_turn()

    async def make_turn(self, content):
        #try:
        pos = int(content)-1
        if pos >= 0 and pos <= 6:
            if not(self.is_column_full(pos)):
                sign = ["x", "o"][self.player_turn]
                row, column = self.get_pos(pos)
                self.field[row][column] = sign
                await self.channel.send(
                    f"{self.players[self.player_turn]} has taken {pos+1}."
                )
                self.turn += 1
                await self.show_current_field()
                await self.check_winning()
                if self.get_state(
                ) == "RUNNING":  # wenn spiel nicht fertig ist
                    self.player_turn = abs(self.player_turn - 1)
                    await self.channel.send(
                        f"{self.players[self.player_turn]} make your turn")
                    if self.players[self.player_turn] == 'computer':
                        await self.computer_turn()
            else:
                await self.channel.send("The Column is full!")
        else:
            await self.channel.send(
                "You have to call a number between [1-9].")
        #except:
        #    print("It wasn't a number.")

    async def check_winning(self):
        # check if x win
        # ----> check row win
        for column in range(7):
            for row in range(3):
                if self.field[row][column] == "x" and self.field[row+1][column] == "x" and self.field[row+2][column] == "x" and self.field[row+3][column] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row+1, column), (row+2, column), (row+3, column)]
                    await self.show_current_field()
                    return
        # ----> check column win
        for row in range(6):
            for column in range(4):
                if self.field[row][column] == "x" and self.field[row][column+1] == "x" and self.field[row][column+2] == "x" and self.field[row][column+3] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row, column+1), (row, column+2), (row, column+3)]
                    await self.show_current_field()
                    return
        # ----> check quer -> braucht man noch zwei prüfungen?
        # nach rechts unten
        for column in range(4):  #-> row and colum richtig herum?
            for row in range(3):
                if self.field[row][column] == "x" and self.field[row+1][column+1] == "x" and self.field[row+2][column+2] == "x" and self.field[row+3][column+3] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row+1, column+1), (row+2, column+2), (row+3, column+3)]
                    await self.show_current_field()
                    return
        # nach rechts oben
        for column in range(4):  #-> row and colum richtig herum?
            for row in range(5, 2, -1):
                if self.field[row][column] == "x" and self.field[row-1][column+1] == "x" and self.field[row-2][column+2] == "x" and self.field[row-3][column+3] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column+1), (row-2, column+2), (row-3, column+3)]
                    await self.show_current_field()
                    return
        # nach links oben
        for column in range(6,2,-1):
            for row in range(5, 2, -1):
                if self.field[row][column] == "x" and self.field[row-1][column-1] == "x" and self.field[row-2][column-2] == "x" and self.field[row-3][column-3] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column-1), (row-2, column-2), (row-3, column-3)]
                    await self.show_current_field()
                    return
        # nach links unten
        for column in range(6,2,-1):
            for row in range(5, 2, -1):
                if self.field[row][column] == "x" and self.field[row-1][column-1] == "x" and self.field[row-2][column-2] == "x" and self.field[row-3][column-3] == "x":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[0]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column-1), (row-2, column-2), (row-3, column-3)]
                    await self.show_current_field()
                    return
        # check if o win
        # ----> check row win
        for column in range(7):
            for row in range(3):
                if self.field[row][column] == "o" and self.field[row+1][column] == "o" and self.field[row+2][column] == "o" and self.field[row+3][column] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row+1, column), (row+2, column), (row+3, column)]
                    await self.show_current_field()
                    return

        # ----> check column win
        for row in range(6):
            for column in range(4):
                if self.field[row][column] == "o" and self.field[row][column+1] == "o" and self.field[row][column+2] == "o" and self.field[row][column+3] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row, column+1), (row, column+2), (row, column+3)]
                    await self.show_current_field()
                    return
        # ----> check quer
        # nach rechts unten
        for column in range(4):  #-> row and colum richtig herum?
            for row in range(3):
                if self.field[row][column] == "o" and self.field[row+1][column+1] == "o" and self.field[row+2][column+2] == "o" and self.field[row+3][column+3] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row+1, column+1), (row+2, column+2), (row+3, column+3)]
                    await self.show_current_field()
                    return
        # nach rechts oben
        for column in range(4):  #-> row and colum richtig herum?
            for row in range(5, 2, -1):
                if self.field[row][column] == "o" and self.field[row-1][column+1] == "o" and self.field[row-2][column+2] == "o" and self.field[row-3][column+3] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column+1), (row-2, column+2), (row-3, column+3)]
                    await self.show_current_field()
                    return
        # nach links oben
        for column in range(6,2,-1):
            for row in range(5, 2, -1):
                if self.field[row][column] == "o" and self.field[row-1][column-1] == "o" and self.field[row-2][column-2] == "o" and self.field[row-3][column-3] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column-1), (row-2, column-2), (row-3, column-3)]
                    await self.show_current_field()
                    return
        # nach links unten
        for column in range(6,2,-1):
            for row in range(5, 2, -1):
                if self.field[row][column] == "o" and self.field[row-1][column-1] == "o" and self.field[row-2][column-2] == "o" and self.field[row-3][column-3] == "o":
                    self.state = self.GameState.COMPLETED
                    await self.channel.send(
                        f":tada: **{self.players[1]}** hat gewonnen :tada:")
                    self.match += 1
                    self.win_pos = [(row, column), (row-1, column-1), (row-2, column-2), (row-3, column-3)]
                    await self.show_current_field()
                    return
        # check if the field is full
        full = 0
        for i in range(7):
            if self.is_column_full(i) == True:
                full += 1
        if full >= 7:
            self.state = self.GameState.COMPLETED
            await self.channel.send(f"**Untenschieden!**")
            self.match += 1


class Chess():
    def __init__(self, bot, channel):
        self.GameState = Enum("GameState", "PLAYERCHOICE RUNNING COMPLETED")
        self.state = self.GameState.PLAYERCHOICE
        self.turn = 0
        self.players = []
        self.player_turn = 0
        self.match = 0
        self.computer = False
        self.channel = channel
        self.bot = bot
        self.game = None

    async def commander(self, message):
        if str(message.guild) == "None" and message.author != self.bot.user:  #bot.user
            pass
        elif message.author != self.bot.user and str(message.guild) != "None":
            if message.content.lower().split()[0] == "ich":
                if self.get_state() == "PLAYERCHOICE":
                    if (len(self.players) < 2 and self.computer == False) or (len(self.players) < 1):
                        await self.add_player(str(message.author), message.channel)
                    else:
                        await message.channel.send("There are enough player!")
                else:
                    await message.channel.send("You are not in the right phase to enter this game.")
            elif message.content.lower().split(" ")[0] in [
                "begin", "play", "start"
            ]:
                if len(self.get_player()) == 2:
                    if self.get_state() == "PLAYERCHOICE" or self.get_state(
                    ) == "COMPLETED":
                        await self.play(message.channel)
                else:
                    await message.channel.send("There are not enough players.")
            elif message.content.lower() in ["ki on", "ai on", "bot on", "com", "player too"]:
                if self.get_state() == "PLAYERCHOICE":
                    await self.add_self()
                else:
                    await message.channel.send("You are not in the right phase to enter this game.")
            elif message.content.lower() in ["current field", "cf", "field", "f"]:
                if self.get_state() == "RUNNING":
                    await self.show_current_field()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["player", "mitspieler"]:
                if self.get_state() == "RUNNING":
                    await self.show_player()
                else:
                    await message.channel.send(
                        "You are not in the right phase to enter this game.")
            elif message.content.lower() in ["?", "cp", "player"]:
                if self.get_state() == "RUNNING":
                    await self.get_current_player()
            elif len(message.content.lower().split(" ")) == 3 and message.content.lower().split(" ")[0] in ["move"]:
                if self.get_state() == "RUNNING":
                    if self.players[self.player_turn] == str(message.author)[:-5]:
                        await self.make_turn(message)
                    else:
                        await message.channel.send(f"chill {str(message.author)[:-5]}... it's not your turn!")
            elif len(message.content.lower().split(" ")) == 2 and message.content.lower().split(" ")[0] in ["move"]:
                if self.get_state() == "RUNNING":
                    if self.players[self.player_turn] == str(message.author)[:-5]:
                        await self.get_valid_moves(message)
                    else:
                        await message.channel.send(f"chill {str(message.author)[:-5]}... it's not your turn!")


    async def add_player(self, name, channel):
        name = name[:-5]
        if name not in self.players:
            if len(self.players) < 2:
                if name not in self.players:
                    await channel.send(f"{name} has joined the game :tickets:")
                    self.players += [name]
            else:
                await self.channel.send("There are to enough player.")
        else:
            await self.channel.send(f"{name} don't play with you anymore.")
            self.players = self.players.remove(name)
            if self.players == None:
                self.players = []

    async def add_self(self):
        if self.computer != True:
            if len(self.players) < 2:
                self.computer = True
                self.players += ["computer"]
                await self.channel.send("I'm playing with you.")
            else:
                await self.channel.send("There are to many player.")
        else:
            await self.channel.send("Computer don't play with you anymore.")
            self.players = self.players.remove("computer")
            self.computer = False
            if self.players == None:
                self.players = []

    def get_player(self):
        return self.players

    def get_state(self):
        return self.state.name

    def get_computer(self):
        return self.computer

    async def get_current_player(self):
        await self.channel.send(
            f"{self.players[self.player_turn]} should make his turn...")

    async def show_current_field(self):
        field = self.game.get_field()
        show_field = ""
        for row in range(8, 0, -1):
            for line in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                pos = f"{line}{row}"

                if pos[0] == "a":
                    show_field += f"{self.number_to_str(pos[1])} |"

                if field[pos] == None:
                    show_field += "      "
                elif type(field[pos]) == pieces.Pawn:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":mechanic:"
                    else:
                        show_field += ":mechanic_tone5:"
                elif type(field[pos]) == pieces.Rook:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":cop:"
                    else:
                        show_field += ":cop_tone5:"
                elif type(field[pos]) == pieces.Knight:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":ninja:"
                    else:
                        show_field += ":ninja_tone5:"
                elif type(field[pos]) == pieces.Bishop:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":detective:"
                    else:
                        show_field += ":detective_tone5:"
                elif type(field[pos]) == pieces.Queen:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":blond_haired_woman:"
                    else:
                        show_field += ":blond_haired_woman_tone5:"
                elif type(field[pos]) == pieces.King:
                    if field[pos].site == engine.site.WHITE:
                        show_field += ":man_mage:"
                    else:
                        show_field += ":man_mage_tone5:"
                
                if pos[0] == "h":
                    show_field += "\n"

        show_field += "      -------------------------------\n"
        show_field += "        :regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:\n\n"

        await self.channel.send(show_field)

    def number_to_str(self, num:int) -> str:
        if num == "1":
            return ":one:"
        elif num == "2":
            return ":two:"
        elif num == "3":
            return ":three:"
        elif num == "4":
            return ":four:"
        elif num == "5":
            return ":five:"
        elif num == "6":
            return ":six:"
        elif num == "7":
            return ":seven:"
        elif num == "8":
            return ":eight:"

    async def show_player(self):
        txt = ""
        for i in range(len(self.players)):
            if i == 0:
                txt += f"White = {self.players[i]}"
            else:
                txt += f"Black = {self.players[i]}"
        await self.channel.send("txt")

    async def play(self, channel):
        self.state = self.GameState.RUNNING
        self.game = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)

        if self.match == 0:
            txt = ":tada: Lasst das Schach Battle starten! :confetti_ball:\nZu Beginn wähle ich die Reihenfolge der Spieler aus.\n(Außerdem kannst du dir mit 'cf' das aktuelle Spielfeld ausgeben lassen und mit 'mitspieler', die Spieler)."
            await channel.send(txt)

            white = random.randint(0, 1)
            black = abs(white - 1)

            if white != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[
                    1], self.players[0]

            self.player_turn = 0

            await self.channel.send(
                f":white_circle:White = {self.players[0]}\n:black_circle:Black = {self.players[1]}. \n\nPlayer white write 'move' and from position and the new position, to make the first turn. Example: move a2 a3.\n(With '?' you can get the Player of the current turn)"
            )

            await self.show_current_field()

            if self.players[0] == 'computer':
                await self.computer_turn(self.channel)
        else:
            self.game = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)
            self.turn = 0
            self.player_turn = 0
            await channel.send(f"Let's start the {self.match+1}. match!")
            white = random.randint(0, 1)
            black = abs(white - 1)

            if white != 0:  # spieler andersherum, müssen getauscht werden
                self.players[0], self.players[1] = self.players[1], self.players[0]

            self.player_turn = self.players[0]

            await self.channel.send(
                f"White = {self.players[0]}\nBlack = {self.players[1]}. \n\nPlayer white write 'move' and from position and the new position, to make the first turn. Example: move a2 a3.\n(With '?' you can get the Player of the current turn)"
            )

            await self.show_current_field()

            if self.players[0] == 'computer':
                await self.computer_turn(self.channel)

    def update_player(self):
        if self.game != None:
            player = self.game.turn.name.upper()
            if player == "WHITE":
                self.player_turn = 0
            elif player == "BLACK":
                self.player_turn = 1

    async def make_turn(self, message):
        content = message.content.lower()
        if self.game != None and self.state == self.GameState.RUNNING:
            from_pos, to_pos = content.split(" ")[1], content.split(" ")[2]
            result = self.game.run_move(from_pos, to_pos)
            if len(result[1]) > 0:
                # check if win
                if "checkmate" in result[1]:
                    self.state = self.GameState.COMPLETED
                    self.match += 1
                    if self.game.winner == engine.site.WHITE:
                        await message.channel.send(":black_circle:Black is checkmate!\n:white_circle:White wins!")
                    else:
                        await message.channel.send(":white_circle:White is checkmate!\n:black_circle:Black wins!")
                    return
                if "Patt" in result[1]:
                    self.state = self.GameState.COMPLETED
                    self.match += 1
                    if self.game.winner == engine.site.WHITE:
                        await message.channel.send("It's Patt! Black can't make a legal move and is not in check.")
                    else:
                        await message.channel.send("It's Patt! White can't make a legal move and is not in check.")
                    return
                await message.channel.send(result[1])
            if self.player_turn == 0 and result[0] == 1:
                await self.channel.send(f":white_circle:White moved from **{from_pos}** to **{to_pos}**")
            elif self.player_turn == 1 and result[0] == 1:
                await self.channel.send(f":black_circle:Black moved from **{from_pos}** to **{to_pos}**")
            await self.show_current_field()
            self.update_player()
            if self.computer and self.players[self.player_turn] == "computer":
                await self.computer_turn(message.channel)
        else:
            await message.channel.send("You have to start a Game!")

    async def get_valid_moves(self, message):
        if self.game != None and self.state == self.GameState.RUNNING:
            from_pos = message.content.lower().split(" ")[1]
            result = self.game.get_moves(from_pos)
            if type(result) == str:
                await message.channel.send(result)

    async def computer_turn(self, channel):
        if self.player_turn == 0:
            site = "WHITE"
        else:
            site = "BLACK"
        result = self.game.run_random_move(site)
        while result[0] == 0:
            result = self.game.run_random_move(site)
        if self.player_turn == 0:
            await channel.send(f":white_circle:White moved from **{result[2][0]}** to **{result[2][1]}**")
        else:
            await channel.send(f":black_circle:Black moved from **{result[2][0]}** to **{result[2][1]}**")
        if len(result[1]) > 0:
            await channel.send(result[1])
        await self.show_current_field()
        self.update_player()


class Bot_xX_Player_Xx(discord.Client):
    WINS = dict()
    GAME = None
    MAIN_CHANNEL = None
    WORDS = dict()

    # log in
    async def on_ready(self):
        date = datetime.now().strftime('Datum: %d.%m.%Y')
        time = datetime.now().strftime('Zeit: %H:%M Uhr')
        print(f"\nPlayer is now online!\n    {time}\n    {date}")

    # a message is posted
    async def on_message(self, message):
        try:
            private_ = str(message.guild).split(" ")[0] == "None"
            if private_ and Bot_xX_Player_Xx.GAME != None:
                await Bot_xX_Player_Xx.GAME.commander(message)
            if message.author == self.user:  # bot.user
                return

            Bot_xX_Player_Xx.MAIN_CHANNEL = message.channel
            self.count_words(message.content.lower())
            if message.content.lower().split()[0] in ["play"]:
                if len(message.content.lower().split()
                        ) == 1 and Bot_xX_Player_Xx.GAME != None:
                    await Bot_xX_Player_Xx.GAME.commander(message)
                elif Bot_xX_Player_Xx.GAME != None:
                    await message.channel.send(
                        "We are still playing a game!\nStop the current game tostart a new one."
                    )
                else:
                    # püfen, was für ein spiel gestartet werden soll
                    if message.content.lower().split()[1] in ["schere", "ssp"]:
                        Bot_xX_Player_Xx.GAME = SchereSteinPapier(
                            self, message.channel)
                        await message.channel.send(
                            "Zum Mitspielen 'ich' schreiben. Falls ich mitspielen soll, dann 'player too' schreiben."
                        )
                        await Bot_xX_Player_Xx.GAME.add_player(
                            str(message.author), message.channel)
                    elif ' '.join(message.content.lower().split()[1:]) in [
                        "ttt", "tic tac toe"
                    ]:
                        Bot_xX_Player_Xx.GAME = TicTacToe(
                            self, message.channel)
                        await message.channel.send(
                            "Zum Mitspielen 'ich' schreiben. Falls ich mitspielen soll, dann 'player too' schreiben."
                        )
                        await Bot_xX_Player_Xx.GAME.add_player(
                            str(message.author), message.channel)
                    elif ' '.join(message.content.lower().split()[1:]) in [
                        "4g", "4w", "4gewinnt", "4 gewinnt", "4 win"
                    ]:
                        Bot_xX_Player_Xx.GAME = FourWins(
                            self, message.channel)
                        await message.channel.send(
                            "Zum Mitspielen 'ich' schreiben. Falls ich mitspielen soll, dann 'player too' schreiben."
                        )
                        await Bot_xX_Player_Xx.GAME.add_player(
                            str(message.author), message.channel)
                    elif ' '.join(message.content.lower().split()[1:]) in ["chess", "schach"]:
                        Bot_xX_Player_Xx.GAME = Chess(
                            self, message.channel)
                        await message.channel.send("Zum Mitspielen 'ich' schreiben. Falls ich mitspielen soll, dann 'player too' schreiben.")
                        await Bot_xX_Player_Xx.GAME.add_player(str(message.author), message.channel)
            elif message.content.lower().split()[0] in [
                "shut up", "exit", "stop"
            ]:
                #if str(message.author).split("#")[0] not in ["Mistery09", "Gott"]:
                if Bot_xX_Player_Xx.GAME != None:
                    Bot_xX_Player_Xx.GAME = None
                    await message.channel.send(
                        "The current Game has been stopped.")
                    with open('./GIFs/ai_bot/ai5.gif', 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)
                else:
                    await message.channel.send("There is no current Game.")
            elif self.check_startswith(message.content.lower(), [
                "bot switch", "switch", "grogu, get over here",
                "get over here", "grogu get over here",
                "destroyer, get over here", "destroyer get over here"
            ]):
                #if self.check_startswith(message.content.lower(), [
                #"grogu, get over here",
                #"get over here", "grogu get over here",
                #"destroyer, get over here", "destroyer get over here"]):
                    #with open("./GIFs/mk_gifs/mk_1.gif", "r") as f:
                        #picture = discord.File(f)
                        #await message.channel.send(file=picture)
                # Player beenden
                if Bot_xX_Player_Xx.GAME != None:
                    Bot_xX_Player_Xx.GAME = None
                date = datetime.now().strftime('Datum: %d.%m.%Y')
                time = datetime.now().strftime('Zeit: %H:%M Uhr')
                print(f"\nPlayer is now offline!\n    {time}\n    {date}")
                await message.channel.send(
                    "Ok...I'm looking for Grogu...bye...")
                await self.close()
            elif message.content.lower().split()[0] in [
                "help", "help bot", "hey bot help", "info", "bot?", "i"
            ]:
                txt = "Hey there, I'm Alino! Alias the Player. :slot_machine: \n\n"
                txt += "You can play Games with me or with your friends, if you want. These are the current games:"
                txt += "\n----> Schere, Stein, Papier (type: 'SSP', 'Schere')\n"
                txt += "\n----> TicTacToe (type: 'ttt')\n"
                txt += "\n----> 4 gewinnt (type: '4g')\n"
                txt += "\n----> Schach (type: 'chess')\n"
                txt += "\n\nTo play a game, you have to:\n    1. initialize the game with **play (gamename)**\n    2. Now all players have to join with **ich**\n    3. At least you start the game with **start** (or begin or play)"
                await message.channel.send(txt)
            #elif message.content.lower() == "send gif":
            #    rand = random.randint(0, 1)
            #    if rand == 0:
            #        path = os.getcwd() + "/GIFs/mk_gifs"
            #    else:
            #        path = os.getcwd() + "/GIFs/ai_bot"
            #    files = os.listdir(path)
            #    file = random.choice(files)
            #    file_path = path + "/" + file
            #    while not (file.endswith(".gif")):
            #        file = random.choice(files)
            #        file_path = path + "/" + file
            #    with open(file_path, 'rb') as f:
            #        picture = discord.File(f)
            #        await message.channel.send(file=picture)
            elif Bot_xX_Player_Xx.GAME != None:
                await Bot_xX_Player_Xx.GAME.commander(message)
        except IndexError:
            pass

    def check_startswith(self, l1: list, l2: list):
        for i in l2:
            if l1.startswith(i):
                return True
        return False

    def save_words(self):
        print("\nsaving typed words...\n")
        txt = ""
        for i in Bot_xX_Player_Xx.WORDS.items():
            key = i[0]
            value = i[1]
            txt += f"{key},{value}\n"
        # findig txt name
        now = datetime.now()
        name = f"words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_01"
        path = os.getcwd() + "/DATA"
        files = os.listdir(path)
        i = 2
        while name in files:
            name = f"words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_{i:02d}"
            i += 1
        file = path + "/" + name
        with open(file, "w") as f:
            f.write(txt[:-1])

    def count_words(self, input: str):
        # Reset alter wörter, wurden schon gespeichert
        Bot_xX_Player_Xx.WORDS = dict()
        # Cleaning
        words = input.replace(",", "").replace(".", "").replace(
            "?",
            "").replace("!", "").replace(";", "").replace("%", "").replace(
                ":",
                "").replace("/", "").replace("=", "").replace("+", "").replace(
                    "-", "").replace("*", "").replace("#", "")
        # Splitting
        words = words.split(" ")
        # Saving
        for i in words:
            if len(i) > 0:
                if Bot_xX_Player_Xx.WORDS.get(i) == None:
                    Bot_xX_Player_Xx.WORDS[i] = 1
                else:
                    Bot_xX_Player_Xx.WORDS[i] += 1
        print("\nWords:\n", Bot_xX_Player_Xx.WORDS, "\n")
        # save words after each message
        self.save_words()
