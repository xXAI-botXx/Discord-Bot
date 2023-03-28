import os
from datetime import datetime
import unittest
import sys


def zip_words() -> str:
    words = ""
    path = os.getcwd() + "/DATA"
    files = os.listdir(path)
    for file in files:
        with open(path + "/" + file, "r") as f:
            words += f.read() + "\n"
    return words.split("\n")


def words_to_dict(words: str) -> dict:
    w_dict = dict()
    for word in words:
        if len(word) > 2:
            try:
                key, value = word.split(",")
                if w_dict.get(key) == None:
                    w_dict[key] = int(value)
                else:
                    w_dict[key] += int(value)
            except Exception as e:
                print(
                    f"Error during word to dict transformation.\nEntry: {word}\n\nError:\n{e}"
                )
                sys.exit(0)
    return w_dict


def dict_to_words(w_dict: dict) -> str:
    words = ""
    for key, value in w_dict.items():
        words += f"{key},{value}\n"
    return words


def remove_old_ones():
    words = ""
    path = os.getcwd() + "/DATA"
    files = os.listdir(path)
    for file in files:
        with open(path + "/" + file, "r") as f:
            words += f.read() + "\n"
        os.remove(path + "/" + file)


def create_backup(target: str):
    with open(target, "r") as f:
        words = f.read() + "\n"

    backups = os.listdir("./backup")
    filename = "backup_000.txt"
    i = 0
    while filename in backups:
        i += 1
        filename = f"backup_{i:03}.txt"

    with open("./backup/" + filename, "w") as f:
        f.write(words)


def run():
    #create_backup()
    print("Summerize Data...")
    # collect all words -> and delete these datas
    words = zip_words()
    # make a dict
    w_dict = words_to_dict(words)
    # make txt_words
    txt_words = dict_to_words(w_dict)
    print("Save summerized data...")
    # remove old files
    remove_old_ones()
    # save in a new txt
    now = datetime.now()
    name = f"sum_words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_01.txt"
    path = os.getcwd() + "/DATA"
    files = os.listdir(path)
    i = 2
    while name in files:
        name = f"sum_words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_{i:02d}.txt"
        i += 1
    file = path + "/" + name
    with open(file, "w") as f:
        f.write(txt_words)
    print("Process is finish.")
    # create backup
    create_backup(file)
    print("Backup has been created.")


class Test(unittest.TestCase):
    def test_words_to_dict(self):
        words = ["hallo,2", "moin,1"]
        self.assertEqual(words_to_dict(words), {"hallo": 2, "moin": 1})

    def test_dict_to_words(self):
        word_dict = {"hallo": 2, "moin": 1}
        self.assertEqual(dict_to_words(word_dict), "hallo,2\nmoin,1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
