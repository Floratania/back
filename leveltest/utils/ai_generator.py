
from openai import OpenAI

client = OpenAI(
    api_key='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',
    base_url="https://openrouter.ai/api/v1"
)

def generate_ai_questions(level="B1", count=10):
    prompt = f"""You are an English placement test generator.


Create {count} multiple-choice questions to determine the English level of a learner at CEFR level {level}.
Each question must be appropriate for evaluating level {level} and should focus on:
- Grammar
- Vocabulary
- Sentence structure
- Reading comprehension
- Everyday communication

Each question must contain:
- A clear question text
- Four answer options labeled A–D
- One correct answer label ("A", "B", "C", or "D")

Format the response as a JSON array like this:
[
  {{
    "question": "Which of these is the correct past tense of 'go'?",
    "options": {{
      "A": "goed",
      "B": "went",
      "C": "gone",
      "D": "go"
    }},
    "correct": "B",
    "source_level": "B1"
  }},
  ...
]
Only include the array, nothing else.
"""

    response = client.chat.completions.create(
        # model="nousresearch/deephermes-3-mistral-24b-preview:free",
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
