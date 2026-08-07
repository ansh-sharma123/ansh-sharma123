import json
import os
import hashlib
from datetime import datetime, timezone

def get_todays_quote():
    """Pick a deterministic daily quote based on today's date."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quotes_path = os.path.join(script_dir, "quotes.json")

    with open(quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    # Use today's date as a seed for deterministic daily rotation
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(quotes)
    return quotes[index]


def update_readme(quote_obj):
    """Update the README.md with today's quote between the marker comments."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(script_dir, "README.md")

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    quote_text = quote_obj["quote"]
    author = quote_obj["author"]

    new_quote_block = (
        f'<!-- QUOTE_START -->\n'
        f'> <i>"{quote_text}"</i> — **{author}**\n'
        f'<!-- QUOTE_END -->'
    )

    # Replace between markers
    import re
    pattern = r"<!-- QUOTE_START -->.*?<!-- QUOTE_END -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_quote_block, content, flags=re.DOTALL)
    else:
        print("❌ ERROR: Could not find <!-- QUOTE_START --> and <!-- QUOTE_END --> markers in README.md")
        print("Please add these markers to your README.md around the quote section.")
        return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Quote updated successfully!")
    print(f'📝 Today\'s quote: "{quote_text}" — {author}')
    return True


if __name__ == "__main__":
    quote = get_todays_quote()
    success = update_readme(quote)
    if not success:
        exit(1)
