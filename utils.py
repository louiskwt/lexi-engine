import enchant

class Dictionary:
    us_dictionary = enchant.Dict("en_US")
    uk_dictionary = enchant.Dict("en_GB")
    
    def is_english_word(this, word):
        # Check if the word exists in the dictionary
        return this.us_dictionary.check(word) or this.uk_dictionary.check(word)