from clpsych.store import Store

import os

if __name__ == '__main__':
    config = {
        'mask': './data/**/*.posts',
        'train_mask': './data/**/TRAIN.txt',
        'test_mask': './data/**/TEST.txt',
        'dev_mask': './data/**/DEV.txt',
        'sample_mask': './data/SAMPLE.txt'
    }

    try:
        os.remove('data.h5')
    except:
        print('No data file found, making a new one.')

    with Store('data.h5', config=config) as load:
        print('Store created. Exiting.')
