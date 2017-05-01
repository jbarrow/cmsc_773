import argparse
import codecs
import os

from spacy.en import English
from clpsych.store import Store
from clpsych import Token

indices_dispatch = {
    'train': lambda x: x.train_indices,
    'test': lambda x: x.test_indices,
    'dev': lambda x: x.dev_indices,
    'sample': lambda x: x.sample_indices
}

def write_line(fp, tok):
    fp.write(
        '\t'.join(
            [str(tok.i), tok.text, tok.lemma_, tok.pos_, '_', str(tok.head.i), tok.dep_]
        ) + '\n'
    )

def write_conll(filename, post_id, title, doc, mode='w'):
    with codecs.open(filename, mode, encoding='utf-8') as fp:
        fp.write(post_id + '\n')
        for tok in title: write_line(fp, tok)
        for tok in doc: write_line(fp, tok)
        fp.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='dataset', default='data.h5')
    parser.add_argument('-i', dest='indices', default='')
    parser.add_argument('-o', dest='output', default='parses')
    args = parser.parse_args()

    with Store(args.dataset) as load:
        if args.indices and args.indices in indices_dispatch:
            data = load.select(indices_dispatch[args.indices](load))
        else:
            print('No valid indices selected. Continuing with all data.')
            data = load.data

        nlp = English()

        unicode_posts = data['text'].str.decode('utf8')
        print('Processing {0} posts'.format(len(unicode_posts)))
        docs = nlp.pipe(unicode_posts, batch_size=16, n_threads=3)
        unicode_titles = data['title'].str.decode('utf8')
        titles = nlp.pipe(unicode_titles, batch_size=16, n_threads=3)
        posts = zip(docs, titles)

        print('Saving documents and titles.')
        cnt, cur = 0, 0 ; mode = 'w'
        for post_id, post in zip(data['post_id'], posts):
            # unpack the post
            doc, title = post
            write_conll(os.path.join(args.output, str(cur) + '.parse'), post_id, title, doc, mode=mode)
            cnt += 1
            mode = 'a'

            if cnt > 10000:
                cnt = 0 ; mode ='w' ; cur += 1
                print '10000 documents completed'
