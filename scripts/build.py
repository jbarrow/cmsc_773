from clpsych.store import Store

if __name__ == '__main__':
    config = {
        'mask': './**/**/*.posts',
        'train_mask': './**/**/TRAIN.txt',
        'test_mask': './**/**/TEST.txt',
        'dev_mask': './**/**/DEV.txt',
        'sample_mask': './SAMPLE.txt'
    }


    with Store('data.h5', config=config, overwrite=True) as load:
        print 'Store created. Exiting.'
