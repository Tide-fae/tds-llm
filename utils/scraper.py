import os
import requests
from openai import OpenAI

def extract_text_from_url(url: str) -> str:
    """
    Download webpage → send HTML to OpenAI → return cleaned text.
    """

    # Ensure API key exists
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[Error: OPENAI_API_KEY is missing on server]"

    # Create OpenAI client AFTER checking the API key
    client = OpenAI(api_key=api_key)

    # Step 1 — Download HTML
    try:
        response = requests.get(url, timeout=10)
        html = response.text
    except Exception as e:
        return f"[Error fetching URL: {e}]"

    # Limit HTML size so LLM doesn’t choke
    html = html[:20000]

    # Step 2 — Ask OpenAI to extract readable text
    prompt = f"""
Extract ONLY meaningful readable text from the following HTML.

Do NOT include:
- HTML tags
- CSS / JavaScript
- headers, footers, menus
- ads, buttons, navbars
- duplicate content

Return plain text only.

HTML content:
{html}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You extract visible text from webpages."},
                {"role": "user", "content": prompt}
            ]
        )

        extracted = completion.choices[0].message["content"]

        return extracted.strip()

    except Exception as e:
        return f"[LLM extraction error: {e}]"
