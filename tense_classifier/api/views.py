# # tense_classifier/api/views.py
# import torch
# from transformers import BertTokenizer
# from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .model import TenseClassifier, tense_labels

# # Load model and tokenizer
# model_path = settings.BASE_DIR / "tense_classifier/model/tense_classifier_model.pth"
# tokenizer_path = settings.BASE_DIR / "tense_classifier/model/tokenizer"
# tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

# model = TenseClassifier(num_classes=len(tense_labels))
# model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
# model.eval()

# @api_view(['POST'])
# def predict_tense(request):
#     sentence = request.data.get("sentence", "").strip()
#     if not sentence:
#         return Response({"error": "Sentence is required"}, status=status.HTTP_400_BAD_REQUEST)

#     inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         logits = model(inputs['input_ids'], inputs['attention_mask'])
#         predicted_label = torch.argmax(logits, dim=1).item()
    
#     predicted_tense = [k for k, v in tense_labels.items() if v == predicted_label][0]
#     return Response({"tense": predicted_tense})
# tense_classifier/api/views.py
import torch
from transformers import BertTokenizer
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .model import TenseClassifier, tense_labels
from pathlib import Path
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt


model_dir = r"C:\Users\tania\C\backend\tense_classifier\model\tense_classifier_model"

tokenizer = BertTokenizer.from_pretrained(model_dir, local_files_only=True)
model = BertForSequenceClassification.from_pretrained(model_dir, local_files_only=True)
model.eval()


# Load model and tokenizer

# model_path = base_dir / "tense_classifier/model/tense_classifier_model.pth"
# tokenizer_path = base_dir / "tense_classifier/model/tokenizer"



@api_view(['POST'])
def predict_tense(request):
    sentence = request.data.get("sentence", "").strip()
    if not sentence:
        return Response({"error": "Sentence is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Токенізація
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        # Отримуємо вихід моделі
        outputs = model(**inputs)
        logits = outputs.logits  # Ось тут головне — отримати логіти
        predicted_label = torch.argmax(logits, dim=1).item()

    # Визначення назви часу
    predicted_tense = [k for k, v in tense_labels.items() if v == predicted_label][0]
    return Response({"tense": predicted_tense})



# MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model_3', 'tense_correctness_model_3')
# tokenizer_2 = BertTokenizer.from_pretrained(MODEL_PATH)
# model_2 = BertForSequenceClassification.from_pretrained(MODEL_PATH)
# model_2.eval()

# @csrf_exempt
# def check_grammar(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)
#         sentence = data.get("sentence")

#         if not sentence:
#             return JsonResponse({'error': 'Sentence is required.'}, status=400)

#         # Токенізація
#         inputs = tokenizer_2(sentence, return_tensors="pt", padding=True, truncation=True, max_length=64)
#         with torch.no_grad():
#             outputs = model_2(**inputs)
#             prediction = torch.argmax(outputs.logits, dim=1).item()

#         result = "correct" if prediction == 1 else "incorrect"
#         return JsonResponse({'result': result})

#     return JsonResponse({'error': 'Only POST method allowed.'}, status=405)
