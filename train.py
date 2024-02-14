from flair.data import Corpus
from flair.datasets import TREC_6
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.datasets import CSVClassificationCorpus
column_name_map = {0: "text", 1: "label"}
corpus: Corpus = CSVClassificationCorpus(data_folder = './data',
                                         train_file = 'train.csv',
                                         dev_file = 'dev.csv',
                                         test_file = 'test.csv',
                                         column_name_map=column_name_map,
                                         skip_header=True,
                                         delimiter=',',
                                         label_type='label')
label_type = 'label'
label_dict = corpus.make_label_dictionary(label_type=label_type)
print(label_dict)
document_embeddings = TransformerDocumentEmbeddings('distilbert-base-uncased', fine_tune=True)
classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, label_type=label_type)
trainer = ModelTrainer(classifier, corpus)
trainer.fine_tune('./model/',
                  learning_rate=5.0e-5,
                  mini_batch_size=16,
                  max_epochs=2)