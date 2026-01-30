import enchant

def is_english_word(word):
    dictionary = enchant.Dict("en_US")
    dictionary_uk = enchant.Dict("en_GB")
    # Check if the word exists in the dictionary
    return dictionary.check(word) or dictionary_uk.check(word)