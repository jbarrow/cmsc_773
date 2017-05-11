import pandas as pd
import numpy as np
import glob
import codecs

from collections import namedtuple

Token = namedtuple('Token', ['i', 'tok', 'lemma', 'pos', 'head', 'sent', 'rank', 'dep'])

def read_broken_tsv(filename):
    """
    Reads a (potentially malformated) TSV file and returns a
    pandas dataframe with the contents.
    """
    data = []
    with open(filename, 'r') as fp:
        for line in fp:
            item = line.strip().split('\t')
            # image/title-only
            if len(item) == 5:
                data.append(item + [''])
            # content post
            elif len(item) == 6:
                data.append(item)
            # formatting error
            elif len(item) > 6:
                item[5] = '__TAB__'.join(item[5:])
                item = item[:6]

    return pd.DataFrame(data,
        columns=['post_id', 'user_id', 'time', 'subreddit', 'title', 'text']
    )

def read_data(mask='./controls/suicidewatch_controls/*.posts'):
    """
    Reads all the posts from a given mask into one large dataframe.
    """
    # load in all the applicable data files
    df = pd.concat((read_broken_tsv(f) for f in glob.glob(mask)))
    # do the necessary type conversions for usability
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['user_id'] = pd.to_numeric(df['user_id'])
    return df

def read_indices(mask):
    """
    Take in a mask to a file that is a list of indices, and return a numpy
    array with those indices
    """
    indices = []
    for index_file in glob.glob(mask):
        with open(index_file, 'r') as ix:
            for line in ix:
                if not line.strip(): continue
                try:
                    indices.append(int(line.strip()))
                except ValueError:
                    continue
    return pd.DataFrame(indices, columns=['user_id'])

def parse_line(line):
    line = line.split('\t')
    if len(line) == 6:
        line.append('_')
    elif len(line) < 6:
        return None
    sent, rank = line[4].split(',')
    return Token(int(line[0]), line[1], line[2], line[3], int(line[5]), int(sent), int(rank), line[6])

def read_parses(mask):
    """
    Hideously ugly function to read in the parses.
    """
    docs, titles = {}, {}
    for f in glob.glob(mask):
        with codecs.open(f, 'r', encoding='utf-8') as fp:
            doc, title = [], []
            post = ''
            cur_title = False
            for line in fp:
                if not line.strip():
                    # if we encounter a blank line, insert the previous post and
                    # keep going
                    docs[post] = doc
                    titles[post] = title
                    doc, title = [], []
                    post = ''
                    cur_title = False
                    continue

                if not post:
                    # if we don't have a post, that means that the next line is
                    # the new post title
                    post = line.strip()
                    continue

                # make sure that we have a token
                token = parse_line(line.strip())
                if token is None:
                    continue
                # does it belong to a document or a title?
                if token.i == 0:
                    if len(title) == 0:
                        title.append(token)
                        cur_title = True
                    else:
                        doc.append(token)
                        cur_title = False
                    continue

                # append it to the correct list depending on what we're reading
                if cur_title:
                    title.append(token)
                else:
                    doc.append(token)

    return docs, titles
