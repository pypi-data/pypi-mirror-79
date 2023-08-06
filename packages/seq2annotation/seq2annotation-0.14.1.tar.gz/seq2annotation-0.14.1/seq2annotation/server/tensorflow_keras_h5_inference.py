from typing import List

import keras
import tensorflow as tf

from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.offset.sequence import Sequence

from tokenizer_tools.tagset.exceptions import TagSetDecodeError

decoder = BILUOSequenceEncoderDecoder()

# don't remove this import, used for auto custom_object discover
import tf_crf_layer
from seq2annotation.input import generate_tagset, Lookuper


class Inference(object):
    def __init__(self, model_path, tag_lookup_file=None, vocabulary_lookup_file=None):
        # load model
        self.model_dir = model_path

        # TODO: temp bugfix
        self.model = tf.keras.models.load_model(model_path)
        self.predict_fn = self.model.predict

        self.tag_lookup_table = Lookuper.load_from_file(tag_lookup_file)
        self.vocabulary_lookup_table = Lookuper.load_from_file(vocabulary_lookup_file)

    def infer(self, input_text: str):
        infer_result = self._infer(input_text)
        return infer_result[0]

    def batch_infer(self, input_text: List[str]):
        return self._infer(input_text)

    def _infer(self, input_text):
        if isinstance(input_text, str):
            input_list = [input_text]
        else:
            input_list = input_text

        raw_sequences = [[i for i in text] for text in input_list]

        id_sequences = self.vocabulary_lookup_table.lookup_list_of_str_list(raw_sequences)

        sentence = keras.preprocessing.sequence.pad_sequences(
            id_sequences, maxlen=45, dtype='object',
            padding='post', truncating='post', value=0
        )

        tags_id_list = self.predict_fn(sentence)

        tags_list = self.tag_lookup_table.inverse_lookup_list_of_id_list(tags_id_list)

        infer_result = []
        for raw_input_text, raw_text, normalized_text, tags in zip(input_list, raw_sequences, sentence, tags_list):
            # decode Unicode
            tags_seq = [i for i in tags]

            # print(tags_seq)

            # BILUO to offset
            failed = False
            try:
                seq = decoder.to_offset(tags_seq, raw_text)
            except TagSetDecodeError as e:
                print(e)

                # invalid tag sequence will raise exception
                # so return a empty result
                seq = Sequence(input_text)
                failed = True

            infer_result.append((raw_input_text, seq, tags_seq, failed))

        return infer_result


if __name__ == "__main__":
    pass
