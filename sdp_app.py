# sdp_app.py
import os
import shutil
import subprocess
from llama_util import extract_price_from_image

class SDPAPP:
    def __init__(self):
        self.image_folder = "images"
        os.makedirs(self.image_folder, exist_ok=True)
        self.extracted_prices = []

    def process_image(self, file):
        image_path = os.path.join(self.image_folder, "image.jpeg")
        with open(image_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            result = extract_price_from_image(image_path)

            if isinstance(result, list) and result:
                self.extracted_prices = result
            else:
                self.extracted_prices = ["0.00"]  # fallback or signal

        except Exception:
            self.extracted_prices = ["0.00"]

    def get_price(self):
        formatted_prices = []
        for amount in self.extracted_prices:
            try:
                manat, qepik = map(int, amount.split('.'))
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
