## Simple guide
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
Use NLTK to obtain tagged tokens like this
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
