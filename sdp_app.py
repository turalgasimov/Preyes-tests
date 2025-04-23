import os
import shutil
import subprocess
from llama_util import extract_price_from_image  # 👈 Import from new file

class SDPAPP:
    def __init__(self):
        self.image_folder = "images"
        os.makedirs(self.image_folder, exist_ok=True)
        self.extracted_prices = []  # Store extracted prices

    def process_image(self, file):
        # Save the uploaded image
        image_path = os.path.join(self.image_folder, "image.jpeg")
        with open(image_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            # Extract price from image using LLaMA
            price = extract_price_from_image(image_path)

            if price:
                self.extracted_prices = [price]
                return [price]
            else:
                return {"error": "Price not found in image."}
        except Exception as e:
            return {"error": str(e)}

    def get_price(self):
        formatted_prices = []
        for amount in self.extracted_prices:
            try:
                amount = str(amount)
                manat, qepik = amount.split('.')
                manat = int(manat)
                qepik = int(qepik)

                if manat == 0:
                    formatted_prices.append(f"{qepik} qəpik")
                elif qepik == 0:
                    formatted_prices.append(f"{manat} manat")
                else:
                    formatted_prices.append(f"{manat} manat {qepik} qəpik")
            except ValueError:
                formatted_prices.append("Invalid price format.")
        return formatted_prices

    def generate_audio(self):
        formatted_prices = self.get_price()
        prices_text = " ".join(formatted_prices)

        command = [
            "espeak-ng",
            "-v", "az",
            "-s", "180",
            "-p", "50",
            "-a", "200",
            "--stdout", prices_text
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.stdout
