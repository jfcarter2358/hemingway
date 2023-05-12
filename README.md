# Hemingway

## About

Hemingway is an NLP package (currently _very_ early in development) designed to explore the use of wavefront collapse for both part of speech tagging as well as parse tree generation. In addition, coref resolution and sentiment analysis are planned on eventually being added in.

## Usage

Currently you can tokenize and POS tag text by using the following syntax:

```python
import hemingway.pos

text = "the quick brown fox jumped over the lazy dog"

tokens = hemingway.pos.tokenize(text)
print(tokens)

tagged = hemmingway.pos.tag_tokens(tokens)
print(tagged)
```

This snipped of code will give you the following output:

```python
['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
[('the', 'DET'), ('quick', 'ADV'), ('brown', 'ADJ'), ('fox', 'NOUN'), ('jumped', 'VERB'), ('over', 'ADP'), ('the', 'DET'), ('lazy', 'ADJ'), ('dog', 'NOUN')]
```

For part of speech tagging Hemingway uses the universal tag set

## Contact

This software is written by John Carter. If you have any questions or concerns feel free to create an issue on GitHub or send me an email at jfcarter2358(at)gmail.com
