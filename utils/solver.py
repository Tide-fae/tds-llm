from openai import OpenAI

client = OpenAI()

def solve_questions(extracted_text: str):
    """
    Use LLM to generate quiz answers / analysis
    based on extracted page text.
    """

    if not extracted_text or extracted_text.startswith("[Error"):
        return {"error": "Invalid extracted text"}

    prompt = f"""
You are an advanced analysis model.
The user extracted the following text from a webpage.

Your job:
- Understand it
- Create a helpful summary
- Identify key points
- Generate a set of quiz-style QA pairs (minimum 5)

Extracted Text:
{extracted_text}

Now output JSON ONLY in this structure:

{{
  "summary": "...",
  "key_points": ["...", "..."],
  "quiz": [
      {{
          "question": "...",
          "answer": "..."
      }}
  ]
}}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        result = completion.choices[0].message["content"]
    except Exception as e:
        return {"error": f"LLM processing error: {e}"}

    return result
