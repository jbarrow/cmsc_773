from clpsych.store import Store

import os

if __name__ == '__main__':
    config = {
        'mask': './**/**/*.posts',
        'train_mask': './**/**/TRAIN.txt',
        'test_mask': './**/**/TEST.txt',
        'dev_mask': './**/**/DEV.txt',
        'sample_mask': './SAMPLE.txt'
    }

    try:
        os.remove('data.h5')
    except:
        print('No data file found, making a new one.')

    with Store('data.h5', config=config) as load:
        print('Store created. Exiting.')
