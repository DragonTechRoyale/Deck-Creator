$(document).ready(function() {
    localStorage.clear();

    if (window.location.pathname == '/decks') {
        $.ajax({
            type: 'GET',
            url: 'data',
            success: function (reponse) {
                localStorage.setItem('profile', JSON.stringify(reponse));
                showDecks();
            }
        });
    
        function showDecks()
        {
            let data = JSON.parse(localStorage.getItem('profile'));
            let titlesList = data.deck_titles;
            let buttonsDiv = document.createElement('div');
            buttonsDiv.id = "titles";
            for (let i = 0; i < titlesList.length; i++)
            {
                let title = document.createElement('button');
                title.setAttribute("id", titlesList[i].replaceAll('-', ' '));
                title.textContent = titlesList[i].replaceAll('-', ' ');
                title.className = "btn btn-primary";
                title.setAttribute("name", "helloButton");
                title.formAction = "title-button";
                title.onclick = function () {
                    learnDeck(title);
                };
                buttonsDiv.appendChild(title);
            }      
            let hanger = document.getElementsByClassName('hanger');
            hanger[0].appendChild(buttonsDiv);
        }

        function learnDeck(deckButton){
            $('#title').hide();
            deckButton.parentNode.style.visibility = "hidden";
            localStorage.setItem('currentDeck', deckButton.textContent)
            let deckDiv = document.createElement('div');
            let deckTitle = document.createElement('h2');

            deckTitle.textContent = deckButton.textContent;
            deckTitle.id = deckButton.id + " Title";

            displayCard(false);

            let hanger = document.getElementsByClassName('hanger');
            deckDiv.appendChild(deckTitle);
            hanger[0].appendChild(deckDiv);
        }

        function displayCard(is_recalled){
            let currentItem = localStorage.getItem('currentCardFront');
            let data = JSON.stringify({"is_recalled" : is_recalled, "id" : "1", "deck_name" : localStorage.getItem('currentDeck')});
            if (currentItem)
            {
                data = JSON.stringify({"is_recalled" : is_recalled, "id" : JSON.parse(currentItem).card_id, "deck_name" : localStorage.getItem('currentDeck')});
            }

            $.ajax({
                type: 'GET',
                url: '/get-card-front/'+data,
                success: function (reponse) {
                    localStorage.setItem('currentCardFront', JSON.stringify(reponse));
                    let cardData = JSON.parse(localStorage.getItem('currentCardFront'));
                    let cardDiv = document.createElement('div');
                    cardDiv.id = "cardDiv";
                    if (cardData.card_id == "over")
                    {
                        if ($("#cardDiv") !== undefined) {
                            $("#cardDiv").hide();;
                        }
                        let deckTitleId = localStorage.getItem('currentDeck') + " Title";
                        let deckTitle = document.getElementById(deckTitleId);
                        let deckTitleText = deckTitle.textContent;
                        deckTitle.setAttribute("name", "おめでとうシンジ");
                        deckTitle.textContent = "Congrats! " + deckTitleText + " is learned for today";

                        let goBackButton = document.createElement('button');
                        goBackButton.textContent = "Go Back";
                        goBackButton.setAttribute("name", "逃げちゃだめだ");
                        goBackButton.className = "btn btn-primary";
                        goBackButton.onclick = function () {
                            location.reload();
                        };
                        cardDiv.appendChild(goBackButton);
                    }
                    else if (document.getElementById("TL-word") == null || document.getElementById("answer-button") == null)
                    {   
                        if ($("#cardDiv") !== undefined) {
                            $("#cardDiv").show();;
                        }
                        let TL_word = document.createElement('h3');
                        let showAnswerButton = document.createElement('button');
    
                        TL_word.textContent = "TL word: " + cardData.TL_word;
                        showAnswerButton.textContent = "Show Answer";
    
                        showAnswerButton.className = "btn btn-primary";
    
                        showAnswerButton.onclick = function () {
                            showBack(cardData.card_id);
                        };
    
                        TL_word.id = "TL-word";
                        showAnswerButton.id = "answer-button";

                        cardDiv.appendChild(TL_word);
                        cardDiv.appendChild(showAnswerButton);
                    }
                    else
                    {
                        if ($("#cardDiv") !== undefined) {
                            $("#cardDiv").show();
                        }
                        document.getElementById("TL-word").textContent = "TL word: " + cardData.TL_word;
                    }
                    if (document.getElementById("good-button") != null &&
                    document.getElementById("again-button") != null &&
                    document.getElementById("NL-word") != null &&
                    document.getElementById("interval") != null)
                    {
                        document.getElementById("good-button").style.visibility = "hidden";
                        document.getElementById("again-button").style.visibility = "hidden";
                        document.getElementById("NL-word").style.visibility = "hidden";
                        document.getElementById("interval").style.visibility = "hidden";
                    }
                    let hanger = document.getElementsByClassName('hanger');
                    hanger[0].appendChild(cardDiv);
                }
            });
        }

        function showBack(){
            $.ajax({
                type: 'GET',
                url: '/get-card-back/' + JSON.parse(localStorage.getItem('currentCardFront')).card_id,
                success: function (reponse) {
                    localStorage.setItem('currentCardBack', JSON.stringify(reponse));
                    let cardData = JSON.parse(localStorage.getItem('currentCardBack'));
                    let cardDiv = document.createElement('div');
                    cardDiv.id = "cardDiv" + JSON.parse(localStorage.getItem('currentCardFront')).card_id;

                    if (document.getElementById("good-button") == null ||
                        document.getElementById("again-button") == null ||
                        document.getElementById("NL-word") == null ||
                        document.getElementById("interval") == null)
                    {
                        goodButton = document.createElement('button');
                        againButton = document.createElement('button');
                        NL_word = document.createElement('h3');
                        is_recalled = document.createElement('h3');
                        interval =document.createElement('h3');
    
                        goodButton.textContent = "Good";
                        againButton.textContent = "Again";
                        NL_word.textContent = "NL word: " + cardData.NL_word;
                        is_recalled.textContent = cardData.isRecalled;
                        interval.textContent = "Interval: " + cardData.interval + " days";
    
                        goodButton.id = "good-button";
                        againButton.id = "again-button";
                        NL_word.id = "NL-word";
                        interval.id = "interval";
    
                        goodButton.onclick = function () {
                            displayCard(true);
                        };

                        againButton.onclick = function () {
                            displayCard(false);
                        };
    
                        cardDiv.appendChild(NL_word);
                        cardDiv.appendChild(is_recalled);
                        cardDiv.appendChild(interval);
                        cardDiv.appendChild(goodButton);
                        cardDiv.appendChild(againButton);
                    }
                    else
                    {
                        if (document.getElementById("good-button") != null &&
                        document.getElementById("again-button") != null &&
                        document.getElementById("NL-word") != null &&
                        document.getElementById("interval") != null)
                        {
                            document.getElementById("good-button").style.visibility = "visible";
                            document.getElementById("again-button").style.visibility = "visible";
                            document.getElementById("NL-word").style.visibility = "visible";
                            document.getElementById("interval").style.visibility = "visible";
                        }

                        document.getElementById("NL-word").textContent = "NL word: " + cardData.NL_word;
                        document.getElementById("interval").textContent = "Interval: " + cardData.interval + " days";
                    }

                    let hanger = document.getElementsByClassName('hanger');
                    hanger[0].appendChild(cardDiv);
                }
            });
        }
    }
});