from .views import detect_mode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import MarianMTModel, MarianTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM
# from transformers import MarianMTModel, MarianTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM

marian_en_uk_tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-uk')
marian_en_uk_model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-uk')

marian_uk_en_tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-uk-en')
marian_uk_en_model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-uk-en')

nllb_tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
nllb_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")


def local_translate(text, direction="en_to_uk"):
    mode = detect_mode(text)

    if mode == 'word':
        lang_map = {
            'en_to_uk': ('eng_Latn', 'ukr_Cyrl'),
            'uk_to_en': ('ukr_Cyrl', 'eng_Latn'),
        }
        src, tgt = lang_map.get(direction, ('eng_Latn', 'ukr_Cyrl'))
        nllb_tokenizer.src_lang = src
        inputs = nllb_tokenizer(text, return_tensors="pt")
        inputs["forced_bos_token_id"] = nllb_tokenizer.convert_tokens_to_ids(tgt)
        outputs = nllb_model.generate(**inputs, max_length=50, num_beams=6, early_stopping=True)
        return nllb_tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
        if direction == 'en_to_uk':
            tokenizer = marian_en_uk_tokenizer
            model = marian_en_uk_model
        else:
            tokenizer = marian_uk_en_tokenizer
            model = marian_uk_en_model

        inputs = tokenizer.encode(text, return_tensors='pt')
        translated_ids = model.generate(inputs, max_length=80, num_beams=8, no_repeat_ngram_size=2, early_stopping=True)
        return tokenizer.decode(translated_ids[0], skip_special_tokens=True)
