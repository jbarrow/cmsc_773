import pandas as pd
import glob

def load_tokens(mask='data/tokens/tokens?.txt'):
    """
    Given a mask, load all the token files into a dataframe.
    """
    dfs = []
    for f in glob.glob(mask):
        df = pd.read_csv(f, index_col=None, sep='\t', header=None, names=['post_id', 'title', 'doc'])
        dfs.append(df)
    return pd.concat(dfs)
