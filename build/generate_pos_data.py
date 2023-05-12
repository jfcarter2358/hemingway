import json
from nltk.corpus import treebank
from nltk.corpus import brown

with open('build/data/penn_to_universal.json', 'r', encoding='utf-8') as conversion_file:
    conversion = json.load(conversion_file)

words = {}

def add_tag_to_words(words: dict, word: str, tag: str) -> dict:
    if not word in words:
        words[word] = {tag: 1}
    else:
        if tag in words[word]:
            words[word][tag] += 1
        else:
            words[word][tag] = 1

    return words

# Penn Treebank
print('Parsing Penn treebank, 1 of 1...')
for word, tag in treebank.tagged_words():
    tag = conversion[tag]
    word = word.lower()
    words = add_tag_to_words(words, word, tag)

# Brown corpus
total = len(brown.categories())
for index, category in enumerate(brown.categories()):
    print(f'Parsing Brown category {category}, {index+1} of {total}...')
    for sents in brown.tagged_sents(categories=category, tagset='universal'):
        for word, tag in sents:
            word = word.lower()
            words = add_tag_to_words(words, word, tag)

with open('data/frequencies.json', 'w', encoding='utf-8') as output_file:
    json.dump(words, output_file, indent=4)
