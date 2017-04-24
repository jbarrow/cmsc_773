from data import read_data, parse_data, read_indices

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
        # use SpaCy to parse the data (if requested)
        if config['parse']:
            print('Parsing data...')
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
    def parse(self):
        if self._config['parse']:
            return self._store['parse']
        return None

    @property
    def train_indices(self): return self._store['indices/train']
    @property
    def dev_indices(self): return self._store['indices/dev']
    @property
    def test_indices(self): return self._store['indices/test']

    @property
    def doc_features(self):
        root = self._store.get_node('documents')
        for node in root._f_list_nodes():
            yield os.path.join('/', root._v_name, node._v_name)

    @property
    def user_features(self):
        root = self._store.get_node('users')
        for node in root._f_list_nodes():
            yield os.path.join('/', root._v_name, node._v_name)

    @property
    def documents(self):
        df = self.data
        for feature in self.doc_features:
            df = df.merge(self._store[feature], on='post_id')
        return df

    @property
    def users(self):
        df = None
        for feature in self.user_features:
            if df is None:
                df = self._store[feature]
            else:
                df.merge(self._store[feature], on='post_id')
        return df
