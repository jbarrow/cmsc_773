import pandas as pd
import numpy as np
import glob

def read_broken_tsv(filename):
    """
    Reads a (potentially malformated) TSV file and returns a
    pandas dataframe with the contents.
    """
    data = []
    with open(filename) as fp:
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
    return pd.DataFrame(indices, columns=['post_id'])

def parse_data():
    pass
