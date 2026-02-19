"""Functions to help edit essay homework using string manipulation.
Consider writing a startswith/endswith custom checker/analyzer.
"""


def capitalize_title(title):

    return title.title()


def check_sentence_ending(sentence):

    # sentence.endswith(".")
    return sentence[:-1] == "."


def clean_up_spacing(sentence):
    """Trim any leading or trailing whitespace from the sentence.

    :param sentence: str - a sentence to clean of leading and trailing space characters.
    :return: str - a sentence that has been cleaned of leading and trailing space characters.
    """

    clean_sentence = sentence.strip()

    return clean_sentence


def replace_word_choice(sentence, old_word, new_word):
    """Replace a word in the provided sentence with a new one.

    :param sentence: str - a sentence to replace words in.
    :param old_word: str - word to replace.
    :param new_word: str - replacement word.
    :return: str - input sentence with new words in place of old words.
    """

    return sentence.replace(old_word, new_word)
