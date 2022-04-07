import Translate

translator = Translate.Translate()  # initialize - passing False as an argument will keep the window open
target_langage = "Japanese"  # langauge we're translating from
native_langauge = "English"  # langauge we're translating to
word_to_translate = "絶対"
translated_word = translator.translate(target_langage, native_langauge, word_to_translate)
print(translated_word)  # print's the translation of "絶対" - which is "absolutely" according to Google Translate
translator.exit()  # closes the translator window (it's hidden but still good to close it)