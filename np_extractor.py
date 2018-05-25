from nltk.tokenize import word_tokenize
from nltk import pos_tag

from np_grammar import np_rules
from rules_matcher import find_matches


def _tokenize(text):
    return pos_tag(word_tokenize(text))


def get_nps_from_text(sentece):
    result = []
    tokens = _tokenize(sentece)
    matches = get_nps_from_tokens(tokens)

    for match in matches['matches_text']:
        result.append(' '.join(match))

    return result


def get_nps_from_tokens(tokenized_sentence):
    tags = list([item[1] for item in tokenized_sentence])
    words = list([item[0] for item in tokenized_sentence])
    matches = find_matches(tags, grammar=np_rules)

    matches_texts = []

    for match in matches['matches']:
        matches_texts.append(words[match[0]:match[1]+1])

    matches['matches_text'] = matches_texts

    return matches


if __name__ == '__main__':
    text = 'What a fucking shame you do not look after the wildlife as well as a noun chunk'
    tokens = _tokenize(text)

    print(get_nps_from_tokens(tokens))
    print(get_nps_from_text(text))
