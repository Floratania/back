# # translator.py
# from transformers import MarianMTModel, MarianTokenizer

# _model = None
# _tokenizer = None

# def translate(word):
#     global _model, _tokenizer
#     if _model is None or _tokenizer is None:
#         model_name = 'Helsinki-NLP/opus-mt-en-uk'
#         _tokenizer = MarianTokenizer.from_pretrained(model_name)
#         _model = MarianMTModel.from_pretrained(model_name)

#     sentence = f"{word}."
#     inputs = _tokenizer(sentence, return_tensors='pt', truncation=True, max_length=40)
#     translated = _model.generate(**inputs, max_length=40, num_beams=4, early_stopping=True)
#     return _tokenizer.decode(translated[0], skip_special_tokens=True).replace('.', '').strip()
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

# def translate(text, src_lang="eng_Latn", tgt_lang="ukr_Cyrl"):
#     inputs = tokenizer(text, return_tensors="pt")
#     inputs["forced_bos_token_id"] = tokenizer.convert_tokens_to_ids(tgt_lang)
#     outputs = model.generate(**inputs, max_length=50)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

def translate(text, src_lang="eng_Latn", tgt_lang="ukr_Cyrl"):
    # Встановлюємо мову джерела вручну для tokenizer
    tokenizer.src_lang = src_lang
    
    # Токенізуємо вхідний текст
    inputs = tokenizer(text, return_tensors="pt")
    
    # Встановлюємо мову перекладу
    inputs["forced_bos_token_id"] = tokenizer.convert_tokens_to_ids(tgt_lang)
    
    # Генеруємо переклад з додатковими параметрами
    outputs = model.generate(
        **inputs,
        max_length=60,                # трохи більша довжина
        num_beams=8,                  # більше варіантів перекладу
        no_repeat_ngram_size=2,      # уникаємо повторень
        early_stopping=True
    )
    
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Додаткове очищення результату (опціонально)
    return translated.strip()
