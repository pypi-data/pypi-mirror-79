# %%
import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type

import numpy as np
from scipy.sparse import csr_matrix

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

import rasa.utils.io as io_utils
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.classifiers import LABEL_RANKING_LENGTH
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import DENSE_FEATURE_NAMES, SPARSE_FEATURE_NAMES, TEXT
from rasa.nlu.featurizers.featurizer import sequence_to_sentence_features
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    import sklearn

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import fasttext

import pickle
from sklearn.model_selection import train_test_split

from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Embedding, Bidirectional, Dropout, LSTM, Dense, TimeDistributed
from tensorflow.keras.optimizers import Adam


import typing
from typing import Any, Optional, Text, Dict, List, Type
import fasttext
import numpy as np
import os
import io
import json

from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.tokenizers.tokenizer import Tokenizer

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata
from rasa.nlu.constants import DENSE_FEATURE_NAMES, DENSE_FEATURIZABLE_ATTRIBUTES, TEXT

import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np

from rasa.nlu.constants import (
    TEXT,
    SPACY_DOCS,
    DENSE_FEATURE_NAMES,
    DENSE_FEATURIZABLE_ATTRIBUTES,
)

class FastTextBase(DenseFeaturizer):

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None, clf=None, le=None) -> None:
        super().__init__(component_config)
        self.clf = clf
        self.le = le

    def generate_fasttext_data(self, training_examples, fasttext_datapath='./fasttext_dataset.txt'):
        def write_fastext_dataset(X, y, path):
            # Create dataset
            with open(path, "w+", encoding='utf-8') as file:
                for text, label in zip(X, y):
                    file.write(f'__label__{label} {text}\n')

        labels = [e.get("intent") for e in training_examples]
        self.le = LabelEncoder()
        y = self.le.fit_transform(labels)

        # texts = [message.text for message in training_examples]
        # texts = [[t.text for t in message.data["tokens"]] for message in training_examples]
        texts = [[t.text for t in message.data["tokens"] if t.text != '__CLS__'] for message in training_examples]
        texts = [" ".join(tokens) for tokens in texts]

        write_fastext_dataset(texts, y, fasttext_datapath)
        
        return fasttext_datapath

    def train_fasttext(self, training_data):
        
        fasttext_dataset = self.generate_fasttext_data(training_data.training_examples,)
        fasttextparameters = {
            'epoch' : self.component_config["epoch"],
            'dim' : self.component_config["dim"],
            'minn' : self.component_config["minn"],
            'maxn' : self.component_config["maxn"],
            # 'lr' : self.component_config["lr"],
            'wordNgrams' : self.component_config["wordNgrams"],
        }
        self.clf = fasttext.train_supervised(input=fasttext_dataset, **fasttextparameters)
   
    def set_fasttext_embeddings(self, message: Message, attribute: Text = TEXT):
        text_vector = self.clf.get_word_vector(message.text)
        word_vectors = [
            self.clf.get_word_vector(t.text)
            for t in message.data["tokens"]
            if t.text != "__CLS__"
        ]
        X = np.array(word_vectors + [text_vector])  # remember, we need one for __CLS__

        features = self._combine_with_existing_dense_features(message, additional_features=X, feature_name=DENSE_FEATURE_NAMES[attribute])
        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def predict_fasttext(self, message):

        X = [message.text]
        
        sorted_indices, probabilities = self.clf.predict(X, k=-1)

        sorted_indices = [int(i.replace('__label__','')) for i in sorted_indices[0]]
        intent_ids = sorted_indices
        intents = self.le.inverse_transform(np.ravel(intent_ids))
        
        probabilities = probabilities[0]
        probabilities = probabilities.flatten()

        intent, intent_ranking = self.generate_prediction_outputs(intents, probabilities)

        return intents, probabilities, intent, intent_ranking

    @staticmethod
    def generate_prediction_outputs(intents, probabilities):
        
        if intents.size > 0 and probabilities.size > 0:
            ranking = list(zip(list(intents), list(probabilities)))[
                :LABEL_RANKING_LENGTH
            ]

            intent = {"name": intents[0], "confidence": float(probabilities[0])}

            intent_ranking = [
                {"name": intent_name, "confidence": float(score)}
                for intent_name, score in ranking
            ]
        else:
            intent = {"name": None, "confidence": 0.0}
            intent_ranking = []

        
        intent = json.loads(json.dumps(intent))
        intent_ranking = json.loads(json.dumps(intent_ranking))

        return intent, intent_ranking

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        
        classifier_file_name = file_name + "_classifier.bin"
        
        self.clf.save_model( os.path.join(model_dir, classifier_file_name) ) 

        preprocessing_file_name = file_name + "_preprocessing.pkl"
        preprocessing_variables = self.le.classes_
        
        with open(os.path.join(model_dir, preprocessing_file_name), 'wb') as f:
            pickle.dump(preprocessing_variables, f)

        return {"classifier": classifier_file_name, "preprocessing": preprocessing_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        preprocessing_file = os.path.join(model_dir, meta.get("preprocessing"))

        clf = fasttext.load_model(classifier_file)
        
        with open(preprocessing_file, 'rb') as f:
            classes = pickle.load(f)

        le = LabelEncoder()
        le.classes_ = classes

        return cls(meta, clf, le,)

class TrainingDataManager:

    @staticmethod
    def apply_grouped_labels(training_data, intent_groups):
        
        raw_intents = [message.get(INTENT) for message in training_data.training_examples]

        for message in training_data.training_examples:
            intent = message.get(INTENT)
            for idx, group_i in enumerate(intent_groups):
                if intent in group_i:
                    message.set(INTENT, f'prior_group_{idx}')
                    break

        return raw_intents

    @staticmethod
    def recover_original_labels(training_data, raw_intents):
        for message, raw_intent in zip(training_data.training_examples, raw_intents):
            message.set(INTENT, raw_intent)

    @staticmethod
    def filter_trainingdata(training_data, filter_intents):
        
        filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        training_data.training_examples = filtered_training_examples

class FastText(FastTextBase):
    # varying batch size
    # stratified batch
    # batch normalization layer
    # tqdm callback
    """
        unsupervised_default = {
            'model': "skipgram",
            'lr': 0.05,
            'dim': 100,
            'ws': 5,
            'epoch': 5,
            'minCount': 5,
            'minCountLabel': 0,
            'minn': 3,
            'maxn': 6,
            'neg': 5,
            'wordNgrams': 1,
            'loss': "ns",
            'bucket': 2000000,
            'thread': multiprocessing.cpu_count() - 1,
            'lrUpdateRate': 100,
            't': 1e-4,
            'label': "__label__",
            'verbose': 2,
            'pretrainedVectors': "",
            'seed': 0,
            'autotuneValidationFile': "",
            'autotuneMetric': "f1",
            'autotunePredictions': 1,
            'autotuneDuration': 60 * 5,  # 5 minutes
            'autotuneModelSize': ""
        }
    """
    defaults = {
        'epoch' : 50,
        'dim' : 300,
        'minn' : 2,
        'maxn' : 6,
        # 'lr' : 0.01,
        'wordNgrams': 1,
    }

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,) -> None:
        self.train_fasttext(training_data)

        
    def process(self, message: Message, **kwargs: Any) -> None:

        intents, probabilities, intent, intent_ranking = self.predict_fasttext(message)

        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)


class FastTextEmbedding(FastTextBase):

    defaults = {
        'epoch' : 50,
        'dim' : 300,
        'minn' : 2,
        'maxn' : 6,
        'wordNgrams': 1,

        'print_count': 5,
    }
        
    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        
        self.train_fasttext(training_data)

        for example in training_data.training_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_embeddings(example, attribute)


    def process(self, message: Message, **kwargs: Any) -> None:
        self.set_fasttext_embeddings(message)


class FastTextLayer(FastTextBase):

    defaults = {
        'epoch' : 80,
        'dim' : 20,
        'minn' : 3,
        'maxn' : 6,
        'wordNgrams': 2,

        'intent_groups': False,

        'embedding_features': True,
        'intent_classification': False,
        'intent_classification_features': False,
    }
        
    def train(self,training_data: TrainingData,config: Optional[RasaNLUModelConfig] = None,**kwargs: Any,) -> None:

        if self.component_config["intent_groups"] != False:
            raw_examples = training_data.training_examples
            TrainingDataManager.filter_trainingdata(training_data, sum(self.component_config["intent_groups"],[]))
            raw_intents = TrainingDataManager.apply_grouped_labels(training_data, self.component_config["intent_groups"])
        
        self.train_fasttext(training_data)

        if self.component_config["intent_groups"] != False:
            TrainingDataManager.recover_original_labels(training_data, raw_intents)
            training_data.training_examples = raw_examples


        if self.component_config["embedding_features"]:
            for example in training_data.training_examples:
                for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                    self.set_fasttext_embeddings(example, attribute)

        
    def process(self, message: Message, **kwargs: Any) -> None:
        
        if self.component_config["embedding_features"]:
            self.set_fasttext_embeddings(message)

        if self.component_config["intent_classification"]:
            intents, probabilities, intent, intent_ranking = self.predict_fasttext(message)
            message.set("intent", intent, add_to_output=True)
            message.set("intent_ranking", intent_ranking, add_to_output=True)

