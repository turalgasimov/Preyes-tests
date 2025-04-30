# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from sdp_app import SDPAPP

app = FastAPI()
sdp_app = SDPAPP()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    sdp_app.process_image(file)
    return {"status": "image processed"}

@app.get("/price/")
async def get_price():
    return {"price": sdp_app.get_price()}

@app.get("/audio/")
async def get_audio():
    audio_stream = sdp_app.generate_audio()
    return StreamingResponse(audio_stream, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.0.146.237", port=8000)
