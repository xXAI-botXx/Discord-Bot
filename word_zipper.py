import os
from datetime import datetime
import unittest

def zip_words() -> str:
    words = ""
    path = os.getcwd()+"/DATA"
    files = os.listdir(path)
    for file in files:
        with open(path+"/"+file, "r") as f:
            words += f.read()+"\n"
        os.remove(path+"/"+file)
    return words.split("\n")

def words_to_dict(words:str) -> dict:
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
                print(f"Error during word to dict transformation.\nEntry: {word}\n\nError:\n{e}")
    return w_dict

def dict_to_words(w_dict:dict) -> str:
    words = ""
    for key, value in w_dict.items():
        words += f"{key},{value}\n"
    return words


def run():
    print("Summerize Data...")
    # collect all words -> and delete these datas
    words = zip_words()
    # make a dict
    w_dict = words_to_dict(words)
    # make txt_words
    txt_words = dict_to_words(w_dict)
    # save in a new txt
    print("Save summerized data...")
    now = datetime.now()
    name = f"sum_words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_01.txt"
    path = os.getcwd()+"/DATA"
    files = os.listdir(path)
    i = 2
    while name in files:
        name = f"sum_words_{now.day}.{now.month}.{now.year}_{now.hour}:{now.minute}_{i:02d}.txt"
        i += 1
    file = path+"/"+name
    with open(file, "w") as f:
        f.write(txt_words)
    print("Process is finish.")

class Test(unittest.TestCase):
    def test_words_to_dict(self):
        words = ["hallo,2", "moin,1"]
        self.assertEqual(words_to_dict(words), {"hallo":2, "moin":1})

    def test_dict_to_words(self):
        word_dict = {"hallo":2, "moin":1}
        self.assertEqual(dict_to_words(word_dict), "hallo,2\nmoin,1")

if __name__ == "__main__":
    unittest.main(verbosity=2)