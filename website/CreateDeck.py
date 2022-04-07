import genanki # There's a wild story that in earlier commits of this code on a private repo this app could generate Anki decks 👀
import pathlib;
import os
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from os.path import expanduser
from py_console import console
from flask_login import current_user
from . import Translate
from . import utils
from . import db
from .models import Decks
from .models import Cards


class CreateDeck():
    supported_langs = []


    def __init__(self, supported_langs = ["Japanese", "English"]) -> None:
        self.supported_langs = supported_langs
         
    def get_freq_list(self, TL, max_words) -> list:
        if TL == "Japanese":
            request = urllib.request.Request('https://www.manythings.org/japanese/words/leeds/words.html', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
            word_list_html = urllib.request.urlopen(request).read()
            soup = BeautifulSoup(word_list_html, 'html.parser')
        else:
            utils.display_error(f"get_freq_list() - TL {TL} not supported, returning empty list")
            return []
        # save all the letters of the alphabets to a string
        letters = ""
        try:
            for path in pathlib.Path(f"./website/required_files/Letters/{TL}").iterdir():
                if path.is_file():
                    current_file = open(path, "r")
                    console.log(f"current file: {current_file}")
                    if os.path.basename(path) != ".DS_Store":
                        letters += current_file.read()
                    current_file.close()
        except FileNotFoundError:
            utils.display_error(utils.messages["errors"]["lang_not_supported"])

        # Save all "b" items to the list
        words_list = soup.find_all("b")
        for i in range(len(words_list)):
            words_list[i] = str(words_list[i])
            words_list[i] = words_list[i].replace('<b>', '')
            words_list[i] = words_list[i].replace('</b>', '')
            for char in words_list[i]:
                if char not in letters:
                        words_list[i] = words_list[i].replace(char, '')

        # remove empty items from the list
        while("" in words_list):
            words_list.remove("")
        
        # Shave list to the requested lengths
        new_list = words_list[:max_words]

        return new_list

    def create_deck(self, TL, NL, max_words) -> str:
        # TODO: create databases for freq lists to be local so deck creation will be faster
        # arabic freq list (with meanings!): https://talkinarabic.com/arabic-words/
        deck_name = f"{TL}_to_{NL}_{max_words}_words"
        users_decks = Decks.query.filter_by(id=current_user.id, deck_name=deck_name).first()
        msg = ""

        if users_decks:
            err_msg = utils.messages["errors"]["deck_exists"]
            msg = err_msg
        else:
            utils.display_success(utils.messages["successes"]["making_deck"])

            words_list = self.get_freq_list(TL, max_words)
            translator = Translate.Translate()
            
            new_deck = Decks(deck_name=deck_name, user_id=current_user.id)
            db.session.add(new_deck)
            db.session.commit()

            is_window_closed = False
            for i in tqdm (range(len(words_list)), desc="create_deck() - Adding words..."):
                translated_word = translator.translate(TL, NL, words_list[i])
                if translated_word == None:
                    is_window_closed = True
                    break
                new_card = Cards(NL=NL, TL_word=words_list[i], NL_word=translated_word, interval=0,deck_id=new_deck.id ,user_id=current_user.id, date="") 
                db.session.add(new_card)
            db.session.commit()
            console.success("create_deck() - Done!")
            
            if is_window_closed:
                console.warn(utils.messages["warns"]["window_closed"])
            success_msg = utils.messages["successes"]["created_deck"]
            console.success(f"{success_msg} {deck_name}")
            msg = success_msg
            translator.exit()
        return msg
