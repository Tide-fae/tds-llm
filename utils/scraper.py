import requests
from openai import OpenAI

client = OpenAI()

def extract_text_from_url(url: str) -> str:
    """
    Fetch HTML → send to OpenAI → return cleaned readable text.
    """

    # Step 1: Download webpage
    try:
        response = requests.get(url, timeout=10)
        html = response.text
    except Exception as e:
        return f"[Error fetching URL: {e}]"

    # Step 2: Use LLM to convert HTML → visible text
    prompt = f"""
You are an expert content extractor.
Given HTML content, extract ONLY meaningful visible text.

Do NOT include:
- HTML tags
- CSS
- JS
- menus, footers, contact info
- irrelevant repeated sections

Return only clean readable text:

HTML:
{html[:200000]}   # safety limit
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Extract clean text from HTML."},
                {"role": "user", "content": prompt}
            ]
        )

        extracted = completion.choices[0].message["content"]
    except Exception as e:
        return f"[LLM extraction error: {e}]"

    return extracted.strip()
