from data import read_data, read_indices

import pickle
import pandas as pd
import os

class Store(object):
    """
    A wrapper for the HDF5 file that holds all the data. It maintains all the
    features and such.
    """

    def __init__(self, filename, overwrite=False, config={}):
        if not overwrite and os.path.isfile(filename):
            self.load(filename)
        else:
            print('Populating data, this may take some time...')
            self._create_dataframe(config, filename)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.finalize()

    def finalize(self):
        self._store.close()

    def load(self, filename):
        self._store = pd.HDFStore(filename)
        self._config = self._store.get_storer('config').attrs.metadata

    def _create_dataframe(self, config, filename):
        """
        Creates the initial blank dataframe
        """
        self._store = pd.HDFStore(filename)
        # read all the data from the given mask
        print('Reading data from disk...')
        self._store['data'] = read_data(mask=config['mask'])
        # read the train/dev/test indices
        print('Reading indices...')
        self._store['indices/train'] = read_indices(mask=config['train_mask'])
        self._store['indices/test'] = read_indices(mask=config['test_mask'])
        self._store['indices/dev'] = read_indices(mask=config['dev_mask'])
        if 'sample_mask' in config:
            self._store['indices/sample'] = read_indices(mask=config['sample_mask'])
        # use SpaCy to parse the data (if requested)
        if 'parsed' in config:
            print('Loading parsed data...')
            self._doc_parse, self._title_parse = read_parse(mask=config['parse'])
        # save the configuration data
        self._store['config'] = pd.DataFrame()
        self._store.get_storer('config').attrs.metadata = config
        self._config = config

    def create_document_feature(self, name, dataframe):
        self._store['documents/'+name] = dataframe

    def create_user_feature(self, name, dataframe):
        self._store['users/'+name] = dataframe

    @property
    def data(self):
        return self._store['data']

    @property
    def train_indices(self): return self._store['indices/train']
    @property
    def test_indices(self): return self._store['indices/test']
    @property
    def dev_indices(self): return self._store['indices/dev']
    @property
    def sample_indices(self): return self._store['indices/sample']

    def select(self, indices, df=None):
        """
        indices : pd.DataFrame, with one column labeled 'user_id'
        """
        if df is None:
            df = self._store['data']
        return df.merge(indices, on='user_id')

    @property
    def doc_features(self):
        root = self._store.get_node('documents')
        for node in root._f_list_nodes():
            yield '/{0}/{1}'.format(root._v_name, node._v_name)

    @property
    def user_features(self):
        root = self._store.get_node('users')
        for node in root._f_list_nodes():
            yield '/{0}/{1}'.format(root._v_name, node._v_name)

    @property
    def documents(self):
        df = self.data
        for feature in self.doc_features:
            df = df.merge(self._store[feature], on='post_id')
        return df

    @property
    def parse(self):
        return [self._doc_parse, self._title_parse]

    @property
    def users(self):
        df = None
        for feature in self.user_features:
            if df is None:
                df = self._store[feature]
            else:
                df.merge(self._store[feature], on='post_id')
        return df
