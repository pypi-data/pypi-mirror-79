import os
import numpy as np

import torch
from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import AutoModelForTokenClassification

from ._tokenization_kobert import KoBertTokenizer


class KoBERT_NER:
    def __init__(self, model_dir, gpu=False):
        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
        self.training_args = torch.load(os.path.join(model_dir, 'training_args.bin'))
        self.labels = [label.strip() for label in open(os.path.join(model_dir, 'label.txt'), 'r', encoding='utf-8')]
        self.tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')

        if gpu and not torch.cuda.is_available():
            self.device = "cpu"
            self.model.to(self.device)
            print("GPU is not available. Model uses cpu")
        else:
            self.device = "cuda" if torch.cuda.is_available() and gpu else "cpu"
            self.model.to(self.device)
            

    def predict(self, batch_size, sentences):
        assert self.model, "Model is not loaded"

        # Convert input lists of words to TensorDataset
        pad_token_label_id = torch.nn.CrossEntropyLoss().ignore_index
        dataset = self._convert_sentences_to_tensor_dataset(sentences, self.training_args, self.tokenizer, pad_token_label_id)
        
        # Predict
        sampler = SequentialSampler(dataset)
        data_loader = DataLoader(dataset, sampler=sampler, batch_size=batch_size)

        all_slot_label_mask = None
        preds = None

        self.model.eval()
        for batch in tqdm(data_loader, desc="Predicting"):
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    "token_type_ids": batch[2],
                    "labels": None
                    }
                outputs = self.model(**inputs)
                logits = outputs[0]

                if preds is None:
                    preds = logits.detach().cpu().numpy()
                    all_slot_label_mask = batch[3].detach().cpu().numpy()
                else:
                    preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
                    all_slot_label_mask = np.append(all_slot_label_mask, batch[3].detach().cpu().numpy(), axis=0)

        preds = np.argmax(preds, axis=2)
        slot_label_map = {i: label for i, label in enumerate(self.labels)}
        preds_list = [[] for _ in range(preds.shape[0])]

        for i in range(preds.shape[0]):
            for j in range(preds.shape[1]):
                if all_slot_label_mask[i, j] != pad_token_label_id:
                    preds_list[i].append(slot_label_map[preds[i][j]])

        predictions = []
        for i, (words, preds) in enumerate(zip(sentences, preds_list)):
            sentence_info = {
                'sentence_idx': i,
                'sentence_content':[]
                }
            for j, (word, pred) in enumerate(zip(words, preds)):
                sentence_info['sentence_content'].append({
                    'word_idx': j,
                    'word': word,
                    'tag': pred
                })
            predictions.append(sentence_info)
        
        return predictions


    def _convert_sentences_to_tensor_dataset(self, 
                                            sentences,
                                            args,
                                            tokenizer,
                                            pad_token_label_id,
                                            cls_token_segment_id=0,
                                            pad_token_segment_id=0,
                                            sequence_a_segment_id=0,
                                            mask_padding_with_zero=True):
        # Setting based on the current model type
        cls_token = tokenizer.cls_token
        sep_token = tokenizer.sep_token
        unk_token = tokenizer.unk_token
        pad_token_id = tokenizer.pad_token_id

        all_input_ids = []
        all_attention_mask = []
        all_token_type_ids = []
        all_slot_label_mask = []

        for words in sentences:
            tokens = []
            slot_label_mask = []
            for word in words:
                word_tokens = tokenizer.tokenize(word)
                if not word_tokens:
                    word_tokens = [unk_token]  # For handling the bad-encoded word
                tokens.extend(word_tokens)
                # Use the real label id for the first token of the word, and padding ids for the remaining tokens
                slot_label_mask.extend([0] + [pad_token_label_id] * (len(word_tokens) - 1))

            # Account for [CLS] and [SEP]
            special_tokens_count = 2
            if len(tokens) > args.max_seq_len - special_tokens_count:
                tokens = tokens[: (args.max_seq_len - special_tokens_count)]
                slot_label_mask = slot_label_mask[:(args.max_seq_len - special_tokens_count)]

            # Add [SEP] token
            tokens += [sep_token]
            token_type_ids = [sequence_a_segment_id] * len(tokens)
            slot_label_mask += [pad_token_label_id]

            # Add [CLS] token
            tokens = [cls_token] + tokens
            token_type_ids = [cls_token_segment_id] + token_type_ids
            slot_label_mask = [pad_token_label_id] + slot_label_mask

            input_ids = tokenizer.convert_tokens_to_ids(tokens)

            # The mask has 1 for real tokens and 0 for padding tokens. Only real tokens are attended to.
            attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

            # Zero-pad up to the sequence length.
            padding_length = args.max_seq_len - len(input_ids)
            input_ids = input_ids + ([pad_token_id] * padding_length)
            attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
            token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)
            slot_label_mask = slot_label_mask + ([pad_token_label_id] * padding_length)

            all_input_ids.append(input_ids)
            all_attention_mask.append(attention_mask)
            all_token_type_ids.append(token_type_ids)
            all_slot_label_mask.append(slot_label_mask)

        # Change to Tensor
        all_input_ids = torch.tensor(all_input_ids, dtype=torch.long)
        all_attention_mask = torch.tensor(all_attention_mask, dtype=torch.long)
        all_token_type_ids = torch.tensor(all_token_type_ids, dtype=torch.long)
        all_slot_label_mask = torch.tensor(all_slot_label_mask, dtype=torch.long)

        dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_slot_label_mask)

        return dataset
        
            

