from clpsych.data import read_indices

import pandas as pd
import argparse
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='dataset', default='**/**/TRAIN.txt')
    parser.add_argument('-n', dest='n', type=int, default=5000)
    args = parser.parse_args()

    train_indices = read_indices(args.dataset)
    # randomly sample n indices
    sample = random.sample(train_indices.user_id, k=args.n)
    # save it to a text file
    sample_df = pd.DataFrame(sample, columns=['user_id'])
    sample_df['user_id'].to_csv('SAMPLE.txt', header=False, index=False)

    positive_count = len(sample_df[sample_df['user_id'] > 0])
    controls_count = len(sample_df[sample_df['user_id'] < 0])

    print('Sampled {0} elements, with:'.format(args.n))
    print('\t{0} from the positive class, and'.format(positive_count))
    print('\t{0} from the controls'.format(controls_count))
