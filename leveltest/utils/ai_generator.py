from openai import OpenAI
import json

client = OpenAI(
    api_key='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',
    base_url="https://openrouter.ai/api/v1"
)

def generate_ai_questions(level="B1", count=7):
    prompt = f"""
You are an expert English test designer.

Generate {count} **challenging** and **realistic** multiple-choice questions in English at CEFR level {level}.

Focus on:
- Tense usage (past, present, etc.)
- Word order and grammar
- Subject-verb agreement
- Vocabulary appropriate to {level}

Each question must:
- Be concise, natural, and meaningful
- Have 4 plausible options (A–D), **only one correct**
- Avoid giving away answers through obvious errors or unnatural phrasing
- **Avoid made-up words** or incorrect conjugation forms like "readed" or "yesterday-ed"
- Use real-life context when possible

Output strictly valid JSON array of {count} questions using this format:
[
  {{
    "question": "Choose the correct sentence.",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct": "C",
    "source_level": "{level}"
  }}
]

Example:
{{
  "question": "Which sentence is correct?",
  "options": {{
    "A": "She go to work every day.",
    "B": "She goes to work every day.",
    "C": "She going to work every day.",
    "D": "She gone to work every day."
  }},
  "correct": "B",
  "source_level": "{level}"
}}

Now generate the questions only in the format above.
"""


    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise Exception("AI returned invalid JSON")
