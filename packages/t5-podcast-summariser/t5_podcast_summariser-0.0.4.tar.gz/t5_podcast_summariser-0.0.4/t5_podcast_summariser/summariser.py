from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelWithLMHead, AutoConfig, AutoModel
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import string
from summarizer import Summarizer

class Summariser:

    def __init__(self, model='paulowoicho/t5-podcast-summarisation', use_extractive=False):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelWithLMHead.from_pretrained(model)
        self.use_extractive = use_extractive
    
    def clean_up(self, summary):
        head, _ , _ = summary.partition(' ---')
        head = head.strip()
        first_letter = head[0].capitalize()
        head = first_letter + head[1:]
        if head[-1] in string.punctuation:
            pass
        else:
            head += '.'
        return head
    
    def extract_top_sentences(self, model, num_sentences):
        custom_config = AutoConfig.from_pretrained(model)
        custom_config.output_hidden_states=True
        custom_tokenizer = AutoTokenizer.from_pretrained(model)
        custom_model = AutoModel.from_pretrained(model, config=custom_config)

        extractive_model = Summarizer(custom_model = custom_model, custom_tokenizer=custom_tokenizer)
        
        result = extractive_model(transcript, min_length=60, num_sentences=num_sentences)
        return ''.join(result)

    
    def summarise(self, transcript, model="SpanBERT/spanbert-base-cased", num_sentences=15):
        input_transcript = None
        
        if self.use_extractive:
            input_transcript = self.extract_top_sentences(transcript, model=model, num_sentences=num_sentences)
        else:
            input_transcript = 'summarize: ' + transcript

        tokenized_transcript = self.tokenizer.encode(input_transcript, return_tensors="pt")
        if len(tokenized_transcript[0]) > 6500:
            #crashes on more than 6500 tokens
            sentence_list = sent_tokenize(transcript)
            length = len(sentence_list)
            truncated_transcript = sentence_list[:int(length/2)] #maybe they talk about content in the first half? find proof
            transcript = ' '.join(truncated_transcript)
            return self.summarise(transcript)
        summary_ids = self.model.generate(tokenized_transcript, max_length=150, num_beams=2, repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary = self.clean_up(summary)
        return summary