from clpsych.store import Store

import pandas as pd

if __name__ == '__main__':
    # only needed the first time you load the file
    config = {
        'mask': './**/**/*.posts',
        'train_mask': './**/**/TRAIN.txt',
        'test_mask': './**/**/TEST.txt',
        'dev_mask': './**/**/DEV.txt',
        'parse': False
    }

    store = Store('data.h5', config=config)

    #### CODE TO CREATE A LENGTH FEATURE
    # to create a new feature, we start with the old pandas table
    length = store.data.copy()
    length = length.assign(post_length = lambda x: x.text.str.len())

    # when the feature is done, save it to the
    store.create_document_feature('length', length[['post_id', 'post_length']])
    store.finalize()
