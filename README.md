# MultiNMT
Multilingual language neural machine translation system with simple Seq2Seq model based on [OpenNMT-tf](https://github.com/OpenNMT/OpenNMT-tf).

### Usage
1.Tokenize

If you download a corpus which hasn't been tokenized, such as WMT dataset, you maybe wanted to tokenize the corpus first.
You can use [Tokenizer](https://github.com/OpenNMT/Tokenizer)
from OpenNMT community. Also, you can use <code> python -B bin/tokenize.py </code> to tokenize your corpus.

2.Byte Pair Encoding

* The most common approach to achieve open vocabulary is to use Byte Pair Encoding (BPE). The codes of BPE can be found at
[here](https://github.com/rsennrich/subword-nmt).
* You can also use third_party tool we provide under the <code>third_party</code>directory.

3.Build vocabulary

* Before building vocabuulary, you have to add artificial
token to mark the translate direction, use <code>python -B
bin/add_token.py</code>.
* We use a shared wordpiece model to build vocabulary, so we
have to merge source data and target data to a single file,
and use <code>python -B bin/build_vocab.py</code> to build
a shared vocabulary.

4.Shuffle corpus (Optional)

You can use following script to shuffle corpus, you will find "corpus.shuf" under data directory.
```
python -B bin/shuffle.py --data [data1, data2, ...]
```

5.Oversample corpus (Optional)

If one of parallel corpus is not enough, you can use this script to Oversample corpus and "corpus.sample" will be under data
directory.

```
python -B bin/sample.py --data [data1, data2,...] --repeat [number of repeat]
```

6.Train and infer

This toolkit is based on OpenNMT-tf, please read [document](https://github.com/OpenNMT/OpenNMT-tf/) to find
how to train a model with OpenNMT-tf.

### QuickStart

Here is a minimal workflow to get you started in using MultiNMT. This example uses a English-German-Spanish dataset for multilingual machine translation.

1.Byte Pair Encoding

* To encode the training corpora using BPE, you need to generate BPE operations first. The following command will create a file named "bpe32k", which contains 32k BPE operations along with two dictionaries named "vocab.en", "vocab.de" and "vocab.es".

```
python third_party/learn_joint_bpe_and_vocab.py --input data/en.train data/de.train data/es.train -s 32000 -o data/bpe32k --write-vocabulary data/en.vocab data/de.vocab data/es.vocab
```

* You still need to encode the training corpus, validation set using the generated BPE operations and dictionaries.

```
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/en.vocab --vocabulary-threshold 50 < data/en.train > data/en.bpe32k.train
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/de.vocab --vocabulary-threshold 50 < data/de.train > data/de.bpe32k.train
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/es.vocab --vocabulary-threshold 50 < data/es.train > data/es.bpe32k.train
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/en.vocab --vocabulary-threshold 50 < data/en.dev > data/en.bpe32k.dev
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/de.vocab --vocabulary-threshold 50 < data/de.dev > data/de.bpe32k.dev
python third_party/apply_bpe.py -c data/bpe32k --vocabulary data/es.vocab --vocabulary-threshold 50 < data/es.dev > data/es.bpe32k.dev
```

2.Create combine training and validation corpus

* We assume that we have two differnt translate directions: es->en and en->de, the we can use following script to add token to the head of training corpus, the token represent to translate direction. This will generate "en.bpe32k.train.2de", "es.bpe32k.train.2en", "en.bpe32k.dev.2de" and "es.bpe32k.dev.2en"

```
python -B bin/add_token.py --data data/es.bpe32k.train data/en.bpe32k.train --lang en de
python -B bin/add_token.py --data data/es.bpe32k.dev data/en.bpe32k.dev --lang en de
```

* Then we create multilingual training and validation corpus, you have to match training and validation corpus carefully.

```
cat data/en.bpe32k.train.2de data/es.bpe32k.train.2en > data/src-train.txt
cat data/de.bpe32k.train data/en.bpe32k.train > data/tgt-train.txt
cat data/en.bpe32k.dev.2de data/es.bpe32k.dev.2en > data/src-dev.txt
cat data/de.bpe32k.dev data/en.bpe32k.dev > data/tgt-dev.txt
```

3.Build vocabulary

* To train an NMT, you need to build vocabularies first. To build a shared source and target vocabulary, you can use the following script:

```
cat data/src-train.txt data/tgt-train.txt > data/train.txt
python -B -m bin.build_vocab --data data/train.txt --save_vocab data/shared.vocab --size 40000
```

4.Train and inference

Please see OpenNMT-tf [document](https://github.com/OpenNMT/OpenNMT-tf), we provide sample configure under <code>config</code>
directory and we use <code>main.py</code> from OpenNMT-tf to train and inference.

### References
Johnson M, Schuster M, Le Q V, et al. Google's Multilingual Neural Machine Translation System: Enabling Zero-Shot Translation[J]. 2016.
