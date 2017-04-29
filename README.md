# CLPsych 2017 Challenge

To construct the full dataset. The last one is optional (only if you want the parse):

```
python -m scripts.sample -n 1000 -d "./**/**/TRAIN.txt"
python -m scripts.build
python -m scripts.parse
```

Yes, the quotes are necessary. It has to be a mask that accesses both the
positive indices and the negative indices.

## Using the Parse

The parse consists of 2 dictionaries:

```
parsed_docs = {
  'post_id': [token1, token2, ...],
  'post_id': [token1, token2, ...],
  ...
}

parsed_titles = {
  'post_id': [token1, token2, ...],
  'post_id': [token1, token2, ...],
  ...
}
```

When you call

```
store.parse
```

you get the dictionaries back in the above order. You can think of the tokens as classes with the
following attributes:
- token.i --- the position in the document
- token.sent --- the sentence number in the document
- token.tok --- the base form
- token.lemma --- the lemmatized word
- token.head --- the index of the head
- token.pos --- the part of speech of the token
- token.dep --- the label of the dependency relation
