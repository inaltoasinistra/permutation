"""Convert mnemonic to integer back and forth.
Remove the checksum if possible.
Must support Electrum, Mycelium (bip44 wallet) and GreenAddress"""
import os

WORDS_NUMBER = (3, 6, 9, 12, 15, 18, 21, 24)
BASE = 2048


def detect_wordlist(words):
    """Select the appropriare wordlist"""
    words_set = set(words)
    directory = os.path.join(os.path.dirname(__file__), 'data', 'wordlist')
    files = os.listdir(directory)
    # English first
    files.remove('english.txt')
    files.insert(0, 'english.txt')
    for fname in files:
        if fname.endswith('.txt'):
            with open(os.path.join(directory, fname), 'rt') as f:
                wordlist = ([w.strip() for w in f.readlines()])
            assert len(wordlist) == BASE
            if words_set <= set(wordlist):
                return wordlist
    else:
        raise ValueError('Wordlist not found')

def get_wordlist(language):
    """Get the wordlist"""
    directory = os.path.join(os.path.dirname(__file__), 'data', 'wordlist')
    with open(os.path.join(directory, language + '.txt'), 'rt') as f:
        wordlist = ([w.strip() for w in f.readlines()])
    assert len(wordlist) == BASE
    return wordlist


def mnemonic_to_integer(words):
    """Convert words to integer"""
    if len(words) not in WORDS_NUMBER:
        raise ValueError(
            'Number of words must be one of the following: [%s], but it is not'
            ' (%d).' % (', '.join(map(str, WORDS_NUMBER)), len(words)))

    # Detect memonic
    wordlist = detect_wordlist(words)
    base = 1
    integer = 0
    for word in reversed(words):
        integer += wordlist.index(word) * base
        base *= BASE
    return integer


def integer_to_mnemonic(integer, language='english'):
    """Convert integer to words. Infer the entropy."""
    words = []
    for n in WORDS_NUMBER:
        if integer < BASE ** n:
            break
    else:
        raise ValueError('integer is too big')

    wordlist = get_wordlist(language)

    for _ in range(n):
        words.append(wordlist[integer % BASE])
        integer //= BASE

    return words[::-1]


__all__ = ['mnemonic_to_integer', 'integer_to_mnemonic']
