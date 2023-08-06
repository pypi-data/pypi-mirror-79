import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

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

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

import copy

class TrainingDataManager:

    @staticmethod
    def apply_grouped_labels(training_data, intent_groups, intent_groups_prefix):
        
        raw_intents = [message.get(INTENT) for message in training_data.training_examples]

        for message in training_data.training_examples:
            intent = message.get(INTENT)
            for idx, group_i in enumerate(intent_groups):
                if intent in group_i:
                    if len(group_i) != 1:
                        message.set(INTENT, f'{intent_groups_prefix}{idx}')
                    break

        return raw_intents

    @staticmethod
    def recover_original_labels(training_data, raw_intents):
        for message, raw_intent in zip(training_data.training_examples, raw_intents):
            message.set(INTENT, raw_intent)

    @staticmethod
    def filter_trainingdata(training_data, filter_intents, exclude_intents=[]):
        
        # filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        # training_data.training_examples = filtered_training_examples

        filtered_training_examples = []
        if filter_intents:
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        elif exclude_intents:
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) not in exclude_intents]
        else:
            assert "No filter intent or exlcude intent" == 0
        return filtered_training_examples
        

class BackupRawData(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        training_data.raw_data = copy.deepcopy(training_data.training_examples)

class LoadData(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        dataset = self.component_config["dataset"]
        training_data.training_examples = getattr(training_data, dataset)
        
class PartitionData(Component):

    defaults = {
        "partition_intents":[],
        "exclude_intents": [],
    }

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        assert self.component_config["partition_intents"]==[] or self.component_config["exclude_intents"]==[]
        assert self.component_config["partition_name"] not in ['training_examples', 'raw_data']
        partition_training_examples = TrainingDataManager.filter_trainingdata(training_data, self.component_config["partition_intents"], self.component_config["exclude_intents"])
        setattr(training_data, self.component_config["partition_name"], partition_training_examples)
