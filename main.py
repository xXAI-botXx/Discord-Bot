import discord
from discord.utils import get
from datetime import datetime
import sys
import os
import random
from youtube_dl import YoutubeDL
import youtube_dl
import time
import threading
import asyncio
from bot_player import Bot_xX_Player_Xx
import enum
import word_zipper
import matplotlib.pyplot as plt
from sympy import *
import math
import numpy as np
import pandas as pd
#import pynacl


class Bot_xX_Destroyer_Xx(discord.Client):
    PLAYER = None
    LAST_MESSAGE = None
    PLAYLIST = True
    GREETING = False
    LOOP = None
    VOICE_NAME = "Versammlung der Mächtigen"
    WORDS = dict()
    LAST_SAVE = None

    # log in
    async def on_ready(self):
        date = datetime.now().strftime('Datum: %d.%m.%Y')
        time = datetime.now().strftime('Zeit: %H:%M Uhr')
        print(f"\nGrogu is now online!\n    {time}\n    {date}")

    # a message is posted
    async def on_message(self, message):
        message.content = message.content.replace("```", "")
        who_ai = [
            "who is ai-bot", "who is ai_bot", "who is <<ai_bot>>",
            "who is ai-bot?", "who is ai_bot?", "who is <<ai_bot>>?"
        ]

        if message.author == bot.user:
            if message.content.lower().split(" ")[0] == "play":
                self.play_music(message)
            else:
                return

        self.count_words(message.content.lower())

        # proof if keyword is in:
        await self.greeting_event(message)
        await self.how_are_you_event(message)

        if message.content.lower() in ["help", "help bot", "hey bot help", "bot?", "info", "i"]:
            txt = "Welcome " + str(
                message.author).split("#")[0] + "!:raised_hands:"
            txt += "\nI'm Grogu, the algorithm based helper:robot: on this shitti Discord Server. \nI think the Members using this Server to learn something...or something else...whatever."
            txt += "\nWatch here for more personally infos about me: https://jedipedia.fandom.com/wiki/Grogu"
            txt += "\nYes...there is a Wikipedia article about me. Absolutly normal for a Bot, which programmed by a stupid human.\n"
            txt += "\nNow you think: ..okei...weird..and what can you do?:thinking:\n"
            txt += "I can do following things:\n"
            txt += "\n----> help (for this message here)"
            txt += "\n-------------> or info, bot?, i"
            txt += "\n----> neues (shows latest change)"
            txt += "\n----> updates (shows updates)"
            txt += "\n----> time (get the current time)"
            txt += "\n----> date (get the current date)"
            txt += "\n----> hey bot (polite conversation) -> you can answer me, if you want."
            txt += "\n----> exit (deactivates me):shushing_face:"
            txt += "\n----> tut + text (i will get some tutorials for you)"
            txt += "\n----> münzwurf (lässt Grogu eine Münze werfen)"
            txt += "\n-------------> oder coinflip, flip, coin oder münze"
            txt += "\n----> play (playing music) -> use 'play ?' or 'play help' for more informations"
            txt += "\n----> send gif (Grogu will send a random GIF of himself)"
            txt += "\n----> calc expression (Grogu will calculate the expression)"
            txt += "\n----> f(x) = function (Grogu will draw and informate about the fnction)"
            txt += "\n-------------> for more information type 'math help'"
            txt += "\n\n----> switch (i change with Alino)\n-------------> also 'come over here' or 'player come over here' are accepted\n-------------> There you can play games :video_game:"
            await message.channel.send(txt)
        elif self.check_startswith(message.content.lower(), [
            "bot switch", "switch", "player, get over here", "get over here",
            "player get over here", "alino get over here",
            "alino, get over here"
        ]):
            # Grogu beenden
            date = datetime.now().strftime('Datum: %d.%m.%Y')
            time = datetime.now().strftime('Zeit: %H:%M Uhr')
            print(f"\nGrogu is now offline!\n    {time}\n    {date}")
            if Bot_xX_Destroyer_Xx.PLAYER != None:
                Bot_xX_Destroyer_Xx.PLAYER.stop()
                await Bot_xX_Destroyer_Xx.PLAYER.disconnect(force=True)
            await message.channel.send(
                "Ok...I'm looking for the Player...bye...")
            await bot.close()
            # Player starten
            #bot_2.run_bot()
        elif message.content.lower() in ["time", "zeit"]:
            time = datetime.now().strftime('Zeit: %H:%M Uhr')
            await message.channel.send(time)
        elif message.content.lower() in ["date", "datum"]:
            date = datetime.now().strftime('Datum: %d.%m.%Y')
            await message.channel.send(date)
        elif message.content.lower() in ["shut up", "exit"]:
            if str(message.author).split("#")[0] not in ["Mistery09", "Gott"]:
                await message.channel.send("OK...")
                await message.channel.send("bye")
                date = datetime.now().strftime('Datum: %d.%m.%Y')
                time = datetime.now().strftime('Zeit: %H:%M Uhr')
                print(f"\nGrogu is now offline!\n    {time}\n    {date}")
                #await bot.logout()
                if Bot_xX_Destroyer_Xx.PLAYER != None:
                    Bot_xX_Destroyer_Xx.PLAYER.stop()
                    await Bot_xX_Destroyer_Xx.PLAYER.disconnect(force=True)
                await bot.close()
                sys.exit()
            else:
                with open('./GIFs/yoda_overheat.gif', 'rb') as f:
                    picture = discord.File(f)
                    await message.channel.send(file=picture)
        elif message.content.lower().split(" ")[0] in [
            "tutorial", "tut", "tuts", "help"
        ]:
            tut_str = message.content.lower().split(' ')[1:]
            url = f"https://www.youtube.com/results?search_query={'+'.join(tut_str)}"
            await message.channel.send("You may look here: " + url)
        elif message.content.lower().split(" ")[0] == "play":
            await self.play_music(message)
        elif message.content.lower() in [
            "stop music", "stop playing", "stop play", "stop"
        ]:
            if Bot_xX_Destroyer_Xx.PLAYER != None:
                await message.channel.send("Wait...I'm stopping this!")
                Bot_xX_Destroyer_Xx.PLAYER.stop()
                await Bot_xX_Destroyer_Xx.PLAYER.disconnect(force=True)
                Bot_xX_Destroyer_Xx.PLAYER = None
            else:
                await message.channel.send("Nothing to stop here.")
        elif message.content.lower() == "send gif":
            path = os.getcwd() + "/GIFs"
            files = os.listdir(path)
            file = random.choice(files)
            file_path = path + "/" + file
            if not (file.endswith(".gif")):
                files = os.listdir(path + "/ai_bot")
                file = random.choice(files)
                file_path = path + "/ai_bot" + "/" + file
            with open(file_path, 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        elif message.content.lower() == "wer hat den olymp geschaffen?":
            await message.channel.send("Syon hat als Zeichen für seine Dankbarkeit den Olymp für die mächtigen Götter geschaffen.")
        elif message.content.lower() in who_ai:
            await message.channel.send(
                "Praise the Creator of all and nothing!\n\nWith him the World and all of its began and with him all will end..."
            )
            path = os.getcwd() + "/GIFs/ai_bot"
            files = os.listdir(path)
            file = random.choice(files)
            file_path = path + "/" + file
            with open(file_path, 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        elif message.content.lower().split(" ")[0] in ["rechne", "calc"]:
            await self.calc(" ".join(message.content.lower().split(" ")[1:]), message.channel)
        elif message.content.lower().startswith("f(x) =") or message.content.lower().startswith("f(x)="):
            if len(message.content.lower().split("=")) == 2:
                await self.draw_func(message.content.lower().split("=")[1], None,message.channel)
            elif len(message.content.lower().split("=")) == 3:
                await self.draw_func(message.content.lower().split("=")[1], message.content.lower().split("=")[2],message.channel)
        elif message.content.lower() == "math help":
            txt = "Willkommen zur Hilfe für das Mathe Modul von mir, Grogu."
            txt += "\nZum einen kann ich dir Dinge ausrechen (1+3 oder 35%23...). Hierfür gibt es das Schlüsselwort **calc** und anschließend die Rechnung. Außerdem kannst du auch sin und cos ganz normal verwenden :)"
            txt += "\n\nSpannender wird es bei meiner anderen Funktion. Ich kann dir nämlich Funktionen plotten lassen und dir Informationen über sie ausgeben lassen. Hierzu schreibe beispielsweise f(x) = x^2. Probiere es einmal aus!\n"
            txt += "Tatsächlich kannst du noch ein paar Parameter bestimmen. Diese Parameter werden hinter der Funktion nach einem weiteren = geschrieben. Dabei musst du 'key':'value' und bei mehreren eingaben, kannst du sie einfach mit einem Leerzeichen trennen. Die verfügbaren Parameter nenne ich dir nun:\n\n"
            txt += "----> color (für die Axen -> Farbangabe flexibel möglich)\n"
            txt += "----> bgcolor (für den Hintergund -> Farbangabe flexibel möglich)\n"
            txt += "----> functioncolor (für die Funktion -> Farbangabe flexibel möglich)\n"
            txt += "----> transparent (Hintergund ein/aus -> True oder False)\n"
            txt += "----> lim (Grenzen der X-Werte -> z.B. 10)\n"
            txt += "----> xlim (x Grenzen z.B. 3,9)\n"
            txt += "----> ylim (y Grenzen z.B. -1,1)\n"
            txt += "----> coordinate,c (Kooridnatensystem True/False)\n"
            txt += "----> n (Anzahl an X-Werte -> normal = 100)\n"
            txt += "----> linestyle (Stil der Funktionslinie -> siehe https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html )\n"
            txt += "----> marker (wie die Punkte geplottet werden -> siehe: https://matplotlib.org/stable/api/markers_api.html )\n"
            txt += "----> grid (grid an/aus -> True oder False)\n"
            txt += "----> aufleitung (Anzahl an Stammfunktionen)\n"
            txt += "----> ableitung (Anzahl an Ableitungen)\n"
            txt += "----> size (Größe des plots 4,8)\n"
            txt += "----> small (Größe des Randes => True/False)\n"
            await message.channel.send(txt)
        elif message.content.lower() in ["bot updates", "updates"]:
            txt = "-> Es werden hier nicht alle Updates und keine Bugs gezeigt. Man sieht eigentlich nur neu eingeführte Features."
            txt += "\n\n----> **v2.0** <----"
            txt += "\n----> Schach hinzugefügt"
            txt += "\n----> Cleaning"
            txt += "\n----> Musik Deleted (YouTube ohne y möglich)"
            txt += "\n----> Flask Server deaktiviert"
            txt += "\n----> Münzwurf hinzugefügt"
            txt += "\n----> Benutzerfreundlichkeit verbessert"
            txt += "\n--------> mehr Keywords zur Hilfe, Hilfe wurde verbessert"
            txt += "\n\n----> **v1.2** <----"
            txt += "\n----> 4 Gewinnt hinzugefügt"
            txt += "\n\n----> **v1.1** <----"
            txt += "\n----> Mehr Optionen zum Zeichnen von Funktionen"
            txt += "\n\n----> **v1.0** <----"
            txt += "\n----> Mathe Update"
            txt += "\n----> Funktionen Zeichnen"
            txt += "\n----> Berechnunungen von Ableitungen und Aufleitungen "
            txt += "\n----> Berechnung von Rechnung"
            txt += "\n\n----> **v0.8** <----"
            txt += "\n----> TicTacToe added"
            txt += "\n\n----> **v0.7** <----"
            txt += "\n----> Bot benutzt nun GIF's"
            txt += "\n\n----> **v0.6** <----"
            txt += "\n----> Es kann immer nur ein Bot online sein"
            txt += "\n----> Wechsel durch Keyword"
            txt += "\n\n----> **v0.5** <----"
            txt += "\n----> Entstehung des Player Bot's"
            txt += "\n----> Schere, Stein, Papier hinzugefügt"
            txt += "\n\n----> **v0.4** <----"
            txt += "\n----> Bot Höflichkeitsfloskel hinzugefügt"
            txt += "\n\n----> **v0.3** <----"
            txt += "\n----> YouTube MP3 abspielen"
            txt += "\n\n----> **v0.2** <----"
            txt += "\n----> Musik abspielen hinzugefügt"
            txt += "\n\n----> **v0.1** <----"
            txt += "\n----> Bot Begrüßung hinzugefügt"
            txt += "\n\n----> **v0.0** <----"
            txt += "\n----> Bot Entstehung"
            await message.channel.send(txt)
        elif message.content.lower() in ["bot news", "news", "bot neues", "neues"]:
            txt = "Ich habe kürzlich Ändertungen bei dem Abspielen von Musik vorgenommen :musical_note:. Zudem gab es interne Änderungen, ich wohne nun wo anders :relaxed:\nAußerdem hat mein Kumpel der Player nun Schach im Angebot :shushing_face: :chess_pawn:\n\nFür mehr Informationen gib **updates** ein oder frage meinen Erschaffer."
            await message.channel.send(txt)
        elif message.content.lower() in ["münze", "flip", "coin", "münzwurf", "coinflip"]:
            txt = "Ok ich werfe eine Münze..."
            await message.channel.send(txt)
            txt = f"--> {random.choice(['Kopf', 'Zahl'])} <--"
            await message.channel.send(txt)

    async def greeting_event(self, message):
        greeting = [
            "hey", "hello", "hallo", "moin", "hi", "tach", "tag", "moinchen"
        ]
        bot_names = ["bot", "destroyer", "grogu", "xx_destroyer_xx"]
        txt = message.content.lower().split(" ")
        if len(txt) >= 2:
            if txt[0] in greeting and txt[1] in bot_names:
                if len(txt) >= 3:
                    if txt[2] == "help":
                        return
                author = str(message.author).split("#")[0]
                await message.channel.send("Hey " + author +
                                            ", how are you today?")
                num = random.randint(0, 7)
                if num == 0:
                    await message.channel.send("Schreib **updates** um eine Übersicht über meine Updates/Features in Erfahrung zu bringen :face_in_clouds:")
                elif num == 1:
                    await message.channel.send("Schreib **neues** um das neuste zu erfahren :newspaper2:")
                elif num == 2:
                    await message.channel.send("Schreib **help** um alle Informationen über mich zu erhalten :heart_on_fire:")
                elif num == 3:
                    await message.channel.send("Wusstest du, dass ich sehr begabt in Mathe bin? :sunglasses:\n\nSchreibe **math help** für mehr Informationen :1234:")
                elif num == 4:
                    await message.channel.send("Wenn du Lust auf Spielen hast, sprich doch mit dem Player! Er freut sich immer, wenn sich Spielkameraden finden lassen.\n\nSchreibe **switch**, um ihn Online zu holen.")
                elif num == 5:
                    await message.channel.send("Es ist eindeutig zu ruhig hier. Schreibe **play https://www.youtube.com/watch?v=lEeMjXOqM64** um die Hütte brennen zu lassen :sunglasses:")
                Bot_xX_Destroyer_Xx.GREETING = True
                #await message.channel.send(file="./GIFs/yoda_greeting.gif")
                rand = random.randint(0, 1)
                if rand == 1:
                    with open('./GIFs/yoda_greeting.gif', 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)

    async def how_are_you_event(self, message):
        try:
            txt = message.content.lower()
            #question_word = ["how", "wie", "was", "and"]
            #between_word = ["are", "geht", "gehts"]
            #end_word = ["dir?", "dir", "you?", "you"]
            formulations = [
                "und dir?", "how are you?", "and you?", "du?", "dir?", "you?",
                "und wie gehts dir?", "und wie geht es dir?"
            ]
            if Bot_xX_Destroyer_Xx.GREETING == True and self.check_endswith(
                txt, formulations):
                await message.channel.send("I'm fine, thanks for asking!")
                rand = random.randint(0, 1)
                if rand == 1:
                    with open('./GIFs/yoda_tea_drink_high.gif', 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)
                Bot_xX_Destroyer_Xx.GREETING = False
        except:
            pass

    def check_endswith(self, l1: list, l2: list):
        for i in l2:
            if l1.endswith(i):
                return True
        return False

    def check_startswith(self, l1: list, l2: list):
        for i in l2:
            if l1.startswith(i):
                return True
        return False

    def check_one_elem_in_both(self, l1: list, l2: list):
        for i in range(len(l1)):
            for j in range(len(l2)):
                if l1[i] == l2[j]:
                    return True
        return False

    def save_words(self):
        print("\nsaving typed words...\n")
        txt = ""
        for i in Bot_xX_Destroyer_Xx.WORDS.items():
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
        Bot_xX_Destroyer_Xx.WORDS = dict()
        # Cleaning
        words = input.replace(",", "").replace(".", "").replace(
            "?",
            "").replace("!", "").replace(";", "").replace("%", "").replace(
                ":",
                "").replace("/", "").replace("=", "").replace("+", "").replace(
                    "-", "").replace("*", "").replace("#",
                                                        "").replace("\n", "")
        # Splitting
        words = words.split(" ")
        # Saving
        for i in words:
            if len(i) > 0:
                if Bot_xX_Destroyer_Xx.WORDS.get(i) == None:
                    Bot_xX_Destroyer_Xx.WORDS[i] = 1
                else:
                    Bot_xX_Destroyer_Xx.WORDS[i] += 1
        print("\nWords:\n", Bot_xX_Destroyer_Xx.WORDS, "\n")
        # save words after each message
        self.save_words()

    def is_str_float(self, numb:str) -> bool:
        if numb.isdigit():
            return False

        try:
            float(numb)
            return True
        except:
            return False

    def is_expr_calc(self, expr:str) -> bool:
        # prüfe, ob auch echt math expr
        test_expr = expr.replace("(", "").replace(")", "").replace(" ", "").replace(",", ".").replace("sin", "").replace("cos", "").replace("sqrt", "").replace("e", "").replace("pi", "").replace("tan", "")
        operators = ["+", "*", "**", "/", "//", "%", "-"]
        last_ops = ["/", "*"]

        # str / einzelne Wörte trennen
        expressions = []
        cur_int = False
        cur_elem = ""
        for char in test_expr:
            if char.isdigit() or (cur_int == True and char == "."):
                if cur_int:
                    cur_elem += char
                else:
                    cur_int = True
                    if len(cur_elem) > 0:
                        expressions += [cur_elem]
                        cur_elem = char
                    else:
                        cur_elem = char
            elif char in operators:
                cur_int = False
                if char in ["+", "-"] and (cur_elem in operators or cur_elem == ""):     # wird nicht gespeichert
                    pass
                else:
                    if cur_elem in last_ops:
                        cur_elem += char
                    elif cur_elem.isdigit() or self.is_str_float(cur_elem):
                        expressions += [cur_elem]
                        cur_elem = char
                    else:
                        return False
            else:
                return False
        # speichere letztes Element falls verfügbar
        if len(cur_elem) > 0:
            expressions += [cur_elem]
            cur_elem = ""
                    
        # its right?
        for i, v in enumerate(expressions):
            if i%2 == 0:
                if not(v.isdigit()) and not(self.is_str_float(v)):
                    return False
            else:
                if v not in operators:
                    return False
        if len(expressions) < 1:
            return False
        return True

    async def calc(self, expr:str, channel):
        expr = expr.replace("^", "**").replace(":", "/")

        # prüfe, ob auch echt math expr
        #if self.is_expr_calc(expr):
        try:
            result = sympify(expr).evalf()
        except Exception as e:
            await channel.send(f"Fehler:\n{e}")
            return

        # calc + message
        await channel.send(f"{expr} = {result}")

    async def build_func(self, func:str, channel, n=100, xlim=[-10, 10], ylim=None) -> list:
        func = func.replace("^", "**").replace(":", "/")

        # testing
        expr = func.replace("x", "1")
        try:
            result = sympify(expr).evalf()
        except Exception as e:
            await channel.send(f"Fehler:\n{e}")
            return

        # build results
        func = func.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan").replace("e", "np.e").replace("pi", "np.pi").replace("sqrt", "np.sqrt")

        x = np.linspace(xlim[0], xlim[1], n)
        #y = sympify(func).subs({'x': x}).evalf()
        y = eval(func)    # -> x wird zu Varable x -> mit Vido sicherer machen?

        # ylim
        if ylim != None:
            df = pd.DataFrame({"x":x, "y":y})
            df = df[(df.y > ylim[0]) & (df.y < ylim[1])]
            x, y = (df.x.to_numpy(), df.y.to_numpy())

        return (x, y)

    # funktionen zeichnen? -> als img speichern und dann hochladen
    async def draw_func(self, func, args, channel):
        # auswertung der args -> liste -> muss erst noch erstell werden
        transparent = True
        color = 'white'
        bg_color = 'white'
        function_color = "steelblue"
        linestyle='-'
        linewidth = 2.0 
        marker='None'
        lim = 10
        n = 100
        x_size = 15
        y_size = 10
        grid = False
        ableitungs_grad = 3
        aufleitungs_grad = 1
        xlim = None
        ylim = None
        coordinate = False
        small = False
        if args != None:
            for i in args.split(" "):
                try:
                    if len(i) > 3:
                        key, value = i.split(":")
                        if key == "color":
                            color = value
                        elif key == "transparent":
                            transparent = (value.title() == "True")
                        elif key == "lim":
                            if value.isdigit():
                                lim = int(value)
                        elif key == "n":
                            if value.isdigit():
                                n = int(value)
                        elif key in ["bg", "bgcolor"]:
                            bg_color = value
                        elif key in ["linestyle"]:
                            linestyle = value
                        elif key in ["linewidth"]:
                            linewidth = value
                        elif key in ["marker"]:
                            marker = value
                        elif key in ["functioncolor", "function"]:
                            function_color = value
                        elif key in ["grid"]:
                            grid = (value.title() == "True")
                        elif key in ["aufleitung", "integration", "stammfunktion"]:
                            if value.isdigit():
                                aufleitungs_grad = int(value)
                        elif key in ["ableitung"]:
                            if value.isdigit():
                                ableitungs_grad = int(value)
                        elif key in ["size"]:
                            if value.startswith("("):
                                value = value.replace("(", "")
                            if value.endswith(")"):
                                value = value.replace(")", "")
                            if value.count(",") == 1:
                                x, y = value.split(",")
                                if x.isdigit() and y.isdigit():
                                    x_size = int(x)
                                    y_size = int(y)
                            else:
                                if value.isdigit():
                                    x_size = int(value)
                                    y_size = int(value)
                        elif key in ["xsize", "x_size"]:
                            if value.isdigit():
                                x_size = int(value)
                        elif key in ["ysize", "y_size"]:
                            if value.isdigit():
                                y_size = int(value)
                        elif key in ["ylim"]:
                            if value.startswith("["):
                                value = value.replace("[", "")
                            if value.endswith("]"):
                                value = value.replace("]", "")
                            if value.count(",") == 1:
                                value = value.split(",")
                                ylim = [int(value[0]), int(value[1])]
                        elif key in ["xlim"]:
                            if value.startswith("["):
                                value = value.replace("[", "")
                            if value.endswith("]"):
                                value = value.replace("]", "")
                            if value.count(",") == 1:
                                value = value.split(",")
                                xlim = [int(value[0]), int(value[1])]
                        elif key in ["coordinate", "c"]:
                            coordinate = (value.title() == "True")
                        elif key in ["small"]:
                            small = (value.title() == "True")
                except:
                    await channel.send(f"Die Argumente der Funktion wurden teilweise falsch eingegeben. Denke daran: 'key':'value'")

        if xlim == None:
            xlim = [-lim, lim]
        # auswertung der funktion
        result = await self.build_func(func, channel, n, xlim, ylim)
        if xlim == None:
            xlim = [-lim, lim]
        elif ylim == None:
            ylim = [result[1].min(), result[1].max()]
        if result == "None":
            await channel.send("I have problems to draw this function. Are you shure, that this function is correct?")
        else:
            try:
                with plt.rc_context({'axes.edgecolor':color, 'xtick.color':color, 'ytick.color':color, 'figure.facecolor':bg_color, 'axes.facecolor':bg_color}):
                    cm = 1/2.54  # centimeters in inches
                    plt.figure(figsize=((x_size*cm, y_size*cm)))
                    plt.plot(result[0], result[1], color=function_color, linestyle=linestyle, marker=marker, linewidth=linewidth)
                    plt.grid(grid)
                    plt.xlim(xlim)
                    plt.ylim(ylim)
                    if small:
                        plt.tight_layout()
                    if coordinate:
                        ax = plt.gca()
                        ax.spines['top'].set_color('none')
                        ax.spines['bottom'].set_position('zero')
                        ax.spines['left'].set_position('zero')
                        ax.spines['right'].set_color('none')
                    #plt.show()
                    path = os.getcwd()+"/functions"
                    filename = "function_001.png"
                    files = os.listdir(path)
                    i = 2
                    while filename in files:
                        filename = f"function_{i:03d}.png"
                        i += 1
                    file = path+"/"+filename
                    plt.savefig(file, transparent=transparent)
                    picture = discord.File(path+"/"+filename)
                    await channel.send(file=picture)
            except Exception as e:
                print(f"Error during drawing:\n{e}")
            # send informations
            x = symbols('x')
            f = func
            txt = ""
            txt += f"**Funktion:**\n```f(x) = {f}```\n\n"
            if aufleitungs_grad > 0:
                txt += f"**Stammfunktionen:**\n```"
            last_func = f
            for i in range(aufleitungs_grad):
                last_func = integrate(last_func, x)
                txt += f"Grad {i+1}: F(x) = {last_func}\n".replace("**", "^")
            txt += "```\n"
            if ableitungs_grad > 0:
                txt += f"\n**Ableitungen:**\n```"
            last_func = f
            for i in range(ableitungs_grad):
                last_func = diff(last_func, x)
                txt += f"Grad {i+1}: f'(x) = {last_func}\n".replace("**", "^")
            txt += "```"
            await channel.send(txt)
            
    async def play_music(self, message):
        Bot_xX_Destroyer_Xx.LOOP = asyncio.get_event_loop()
        Bot_xX_Destroyer_Xx.LAST_MESSAGE = message
        if Bot_xX_Destroyer_Xx.PLAYER != None:
            Bot_xX_Destroyer_Xx.PLAYER.stop()
            await Bot_xX_Destroyer_Xx.PLAYER.disconnect(force=True)
            Bot_xX_Destroyer_Xx.PLAYER = None

        if len(message.content.lower().split(" ")) == 2:
            if message.content.lower().split(" ")[1] == "help" or message.content.lower().split(" ")[1] == "?":
                await message.channel.send("You want to play music and don't know how?:poop:\nLet me help you!")
                txt = "I'm sorry...this area has been shortened. Now you only can use Youtube Videos.\n\n-> For that type 'play y youtubelink*'"
                await message.channel.send(txt)
            else:
                try:
                    await message.channel.send("Let's go!\nIt could take a moment.")
                    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                    FFMPEG_OPTIONS = {
                        'before_options':
                        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn'
                    }
                    channel = get(message.guild.channels,
                                    name=Bot_xX_Destroyer_Xx.VOICE_NAME)
                    voice = await channel.connect()
                    link = message.content.split(" ")[1]
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(link, download=False)
                    URL = info['formats'][0]['url']
                    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    Bot_xX_Destroyer_Xx.PLAYER = voice
                except youtube_dl.utils.DownloadError:
                    await message.channel.send("Video don't found. Link was '" +
                                                link + "'")
                    await voice.disconnect()
                    Bot_xX_Destroyer_Xx.PLAYER = None
        elif message.content.lower().split(" ")[1] in ["youtube", "y"]:
            try:
                await message.channel.send("Let's go!\nIt could take a moment.")
                YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                FFMPEG_OPTIONS = {
                    'before_options':
                    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }
                channel = get(message.guild.channels,
                                name=Bot_xX_Destroyer_Xx.VOICE_NAME)
                voice = await channel.connect()
                link = message.content.split(" ")[2]
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(link, download=False)
                URL = info['formats'][0]['url']
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                Bot_xX_Destroyer_Xx.PLAYER = voice
            except youtube_dl.utils.DownloadError:
                await message.channel.send("Video don't found. Link was '" + link + "'")
                await voice.disconnect()
                Bot_xX_Destroyer_Xx.PLAYER = None


if __name__ == '__main__':
	Modes = enum.Enum("Modes", "BOT_RUNNING WORDS_SAVING")
	mode = Modes.WORDS_SAVING
	mode = Modes.BOT_RUNNING

	if mode == Modes.BOT_RUNNING:
		running = True
		n_loop = 0
		loop = asyncio.get_event_loop()

		while running:
			print("\nnext loop", n_loop)

			if loop.is_closed():
				print("Old Eventloop is closed. \nCreating a new one...\n")
				loop = asyncio.new_event_loop()

			if n_loop % 2 == 0:
				bot = Bot_xX_Destroyer_Xx()
				loop.run_until_complete(bot.start(os.environ['token_1']))
			else:
				bot_2 = Bot_xX_Player_Xx()
				loop.run_until_complete(bot_2.start(os.environ['token_2']))

			n_loop += 1
	elif mode == Modes.WORDS_SAVING:
		word_zipper.run()
