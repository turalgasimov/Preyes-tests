import ollama
import time
import re

start = time.time()

response = ollama.chat(
    model="llama3.2-vision",
    messages=[
        {
            "role": "user",
            "content": "Give me only product price in price tag, in X.XX format.",
            "images": ["./images/test-4.jpeg"]
        }
    ]
)

# Extract the numeric part in X.XX format from the model's response
content = response['message']['content']
match = re.search(r"\d+\.\d{2}", content)

if match:
    price = match.group()
    print(price)
else:
    print("Price not found.")

end = time.time()
print(f"Execution time: {end - start:.2f} seconds")