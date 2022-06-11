import json
import datetime
from py_console import console
from flask import Blueprint, jsonify, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db
from . import CreateDeck
from . import utils
from .models import Decks
from .models import Cards


__ERRORS = utils.messages["errors"]
__SUCCESSES = utils.messages["successes"]
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    deck_creator = CreateDeck.CreateDeck()
    
    if request.method == 'POST':
        if request.form['action'] == 'submitButton':
            native_lang = request.form.get('NL')
            target_lang = request.form.get('TL')
            if request.form.get('wordcount') == '':
                utils.display_error(__ERRORS["no_word_count_error"])
            else:
                word_count = int(request.form.get('wordcount'))
                if word_count < 1 or word_count > 50:
                    utils.display_error(__ERRORS["word_count_error"])
                else:
                    message = deck_creator.create_deck(TL=target_lang, NL=native_lang, max_words=word_count)
                    if message in __ERRORS:
                        utils.display_error(message)
                    else:
                        utils.display_success(message + " " + __SUCCESSES["deck_redirect"])
                        return redirect(url_for('views.decks'))
        elif request.form['action'] == 'decksButton':
            users_decks = Decks.query.filter_by(id=current_user.id).first()
            if users_decks:
                console.info(f"views - home - url_for('views.decks'):\n{url_for('views.decks')}")
                return redirect(url_for('views.decks'))
            else:
                utils.display_error(__ERRORS["user_not_create_deck"])
    return render_template("home.html", user=current_user)
        
@views.route('/decks')
@login_required
def decks():
    title = "Decks:"
    return render_template("decks.html", user=current_user, title=title)

@views.route('/data')
@login_required
def decks_data():
    deck_titles = []
    for item in Decks.query.filter_by(user_id=current_user.id):
        deck_titles.append(item.deck_name.replace('_','-'))
    my_data = {
        "deck_titles": deck_titles
    }
    return jsonify(my_data)

@views.route('/get-card-front/<data>')
@login_required
def get_card_front(data):
    # handle prev card
    json_data = json.loads(data)
    console.info(f"data: {json_data}")
    card_id = json_data['id']
    is_recalled = json_data['is_recalled']
    if is_recalled == 1:
        card = Cards.query.filter_by(user_id=current_user.id, id=int(card_id)).first()
        if card:
            current_interval = card.interval
            interval = 0
            match current_interval:
                case 0:
                    interval = 1
                case 1:
                    interval = 3
                case 3:
                    interval = 7
                case 7:
                    interval = 14
                case 14:
                    interval = 30
            if current_interval > 14:
                interval = current_interval + 30
            card.date = datetime.datetime.now().strftime("%x")
            card.interval = interval
            db.session.commit()
            
            
    # handle new card
    deck_name = json_data['deck_name'].replace(" ", "_")
    console.info(Decks.query.filter_by(deck_name=deck_name).first())
    deck_id = Decks.query.filter_by(deck_name=deck_name).first().id
    cards = Cards.query.filter_by(user_id=current_user.id, deck_id=deck_id).order_by(desc(Cards.interval)).order_by(desc(Cards.id))
    card = None
    for tmp in cards:
        if tmp.date != datetime.datetime.now().strftime("%x") and tmp.interval > 0:
            card_year = int("20" + tmp.date.split('/')[2])
            card_month = int(tmp.date.split('/')[0])
            card_day = int(tmp.date.split('/')[1])
            
            this_year = int(datetime.datetime.now().strftime("%Y"))
            this_month = int(datetime.datetime.now().strftime("%m"))
            this_day = int(datetime.datetime.now().strftime("%d"))
            
            d0 = datetime.date(card_year, card_month, card_day)
            d1 = datetime.date(this_year, this_month, this_day)
            delta = d1 - d0
            
            card = tmp
            card.is_recalled = 0
            if delta.days != tmp.interval:
                # if user skipped a day he needs to re-learn the card 
                card.date = datetime.datetime.now().strftime("%x")
                card.interval = 0
        elif tmp.interval == 0:
            card = tmp
            card.is_recalled = 0
    if card:
        card_id = card.id
        TL_word = card.TL_word
    else:
        card_id = "over"
        TL_word = "over"
    my_data = {
        "card_id" : card_id,
        "TL_word" : TL_word,
    }
    console.info(my_data)
    return jsonify(my_data)

@views.route('/get-card-back/<card_id>')
@login_required
def get_card_back(card_id):
    card = Cards.query.filter_by(user_id=current_user.id, id=card_id).first()
    
    NL_word = card.NL_word
    is_recalled = card.is_recalled
    interval = card.interval
    
    my_data = {
        "NL_word" : NL_word,
        "is_recalled" : is_recalled,
        "interval" : interval
    }
    console.info(my_data)
    return jsonify(my_data)

@views.route('/help')
def help():
    return redirect("https://github.com/DragonTechRoyale/Deck-Creator")