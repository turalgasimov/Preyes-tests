import ollama
import re

def extract_price_from_image(image_path: str):
    """
    Uses LLaMA 3.2 Vision to extract a product price in X.XX format from the given image.
    Returns the price as a string or an error dictionary.
    """
    try:
        response = ollama.chat(
            model="llama3.2-vision",
            messages=[
                {
                    "role": "user",
                    "content": "Extract price in X.XX format only.",
                    "images": [image_path]
                }
            ]
        )

        content = response['message']['content']
        match = re.search(r"\d+\.\d{2}", content)

        if match:
            return [match.group()]
        else:
            return {"error": "Price not found in the image."}

    except Exception as e:
        return {"error": str(e)}
