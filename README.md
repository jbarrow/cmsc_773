# CLPsych 2017 Challenge

## Installing the necessary packages

Most of this is built on top of a few core python packages: `sklearn`, `spacy`, `numpy`, and `scipy`. Most other code that is needed is included in the repository.

## Constructing the Data

To construct the full dataset. The last one is optional (only if you want the parse):

```
python -m scripts.sample -n 1000 -d "./**/**/TRAIN.txt"
python -m scripts.build
python -m scripts.parse
```

Yes, the quotes are necessary. It has to be a mask that accesses both the
positive indices and the negative indices.

## Building and Classifying

Much of our building process was done in iPython notebooks, which output CSVs. To align all the indices with their category, first run al the code in `Statistics.ipynb`. This will also output a `lemmas.txt` file, which has the tokenized and lemmatized data that the following notebooks depend on.

Once you've run the above code, to generate the following features that we used, run the chosen iPython notebooks.
  - **sentence features** - this includes avg. sentence length, etc. Run the code in `SentenceFeatures.ipynb`, which will generate a csv.
  - **LIWC topics** - to generate the topic models, run the code in `LIWC.ipynb`, which will also generate a csv.
  - **bag of words features** - to generate the bag of words features, run the code in `Bag_of_Words.ipynb`. You can change the number of output features in the notebook (it's defaulted to 100).

Finally, all of the readability/sentence features are created by running the following files:

```
python features_jeff.py
```

## Using the Parse

Once laded, the the parse consists of 2 dictionaries:

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
