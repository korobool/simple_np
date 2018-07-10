## What is a Noun Phrase?
A noun phrase is a group of words that work together to name and describe a person, place, thing, or idea. 
Better to say "an entity" that behaves like a simple noun. Paraphrasing this, we can say that when 
we look at the structure of writing, we treat a noun phrase the same way we treat a common noun.
See [this](https://github.com/korobool/simple_np/blob/master/np.md) to read related grammar topic.

## Motivation
There are many modern NLP tools, like spacy that are able to find noun-phrases. 
All of them work well on a consistent text that can be parsed into a correct syntax tree. 
In cases when syntax is broken, POS and tree parsers become weak and things go worse. 
This solution has a goal to use extremely simple context free grammars on top of very 
simple and in general less accurate POS tagger consuming it's only strong side - robustness 
for noised broken text. It is expected to be much weaker on a normal text, but perform 
better on input like twitter and chats.

## Dependencies
* Python 3.5+
* NLTK (temporary dependency)

do not forget to install NLTK models by running

```bash
python -m nltk.downloader all
```
or from the code directly
```python
import nltk
nltk.download('all')
```
[See instructions](https://www.nltk.org/data.html)

## Simple guide
[here](https://github.com/korobool/simple_np/blob/master/how-to-use.ipynb) you can see a jupyter notebook with examples 
* First, ipmort required functions
```
from np_extractor import get_nps_from_text, get_nps_from_tokens
```
* If you just want to get NP groups from a text
Just call a ```get_nps_from_text()``` giving the text as an input.
```python
text = 'What a fucking shame you do not look after the wildlife as well as a noun chunk.'
print(get_nps_from_text(text))
```
```bash
>>> ['a fucking shame', 'the wildlife', 'a noun chunk']
```
* If you want get some more advanced info on rules which caused mathces and tokens indecies
Use brown-based POS tagger (for instance NLTK) to obtain tagged tokens like this
```python
from nltk.tokenize import word_tokenize
from nltk import pos_tag
pos_tag(word_tokenize(text))
```
and feed the list to ```get_nps_from_tokens()```

```python
print(get_nps_from_tokens(pos_tag(word_tokenize(text))))
```

```bash
>>> {'matches': [(1, 3), (9, 10), (14, 16)], 'rules': [('DT', 'NN'), ('DT', 'NN'), ('DT', 'JJ', 'NN')], 
'matches_text': [['a', 'fucking', 'shame'], ['the', 'wildlife'], ['a', 'noun', 'chunk']]}
```
## Current restrictions and needed improvements
1. Decectcs continious np only (sequence cannot be separated by any tokens that a not a part of detecting NP)
2. At this moment input cannot be too long. Currently it is restricted by 120 tokens. If input is longer then 120, the ```TooLongInputError``` exception rised.
