from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from sdp_app import SDPAPP

app = FastAPI()

# Initialize the SDPAPP
sdp_app = SDPAPP()

@app.get("/")
async def root():
    return {"state": "running"}

@app.post("/image")
async def process_image(file: UploadFile = File(...)):
    # Process the image and store the extracted prices
    extracted_prices = sdp_app.process_image(file)
    if isinstance(extracted_prices, dict) and extracted_prices.get("error"):
        return extracted_prices
    return {"message": "Image processed successfully", "prices": extracted_prices}

@app.get("/price")
async def get_price():
    # Retrieve the formatted prices from get_price
    formatted_prices = sdp_app.get_price()
    if isinstance(formatted_prices, dict) and formatted_prices.get("error"):
        return formatted_prices
    return {"prices": formatted_prices}

@app.get("/audio")
async def generate_audio():
    # Generate the audio response using the SDPAPP method
    audio_stream = sdp_app.generate_audio()
    if isinstance(audio_stream, dict) and audio_stream.get("error"):
        return audio_stream  # Return error if any occurred

    return StreamingResponse(audio_stream, media_type="audio/wav")
