import argparse
import pickle

from spacy.en import English
from clpsych.store import Store
from clpsych import Token

indices_dispatch = {
    'train': lambda x: x.train_indices,
    'test': lambda x: x.test_indices,
    'dev': lambda x: x.dev_indices,
    'sample': lambda x: x.sample_indices
}

def process_doc(parsed):
    doc = []
    for i, sent in enumerate(parsed.sents):
        for tok in sent:
            doc.append(Token(tok.i, i, tok.text, tok.lemma_, tok.head.i, tok.pos_, tok.dep_))
    return doc

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='dataset', default='data.h5')
    parser.add_argument('-i', dest='indices', default='')
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
        processed = nlp.pipe(unicode_posts, batch_size=16, n_threads=3)
        processed = [process_doc(d) for d in processed]
        docs = dict(zip(data['post_id'], processed))

        unicode_titles = data['title'].str.decode('utf8')
        processed = nlp.pipe(unicode_titles, batch_size=16, n_threads=3)
        processed = [process_doc(d) for d in processed]
        titles = dict(zip(data['post_id'], processed))

        print('Saving documents and titles.')
        pickle.dump([docs, titles], open('parse.pkl', 'wb'))
