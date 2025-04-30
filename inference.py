# inference.py
from inference_sdk import InferenceHTTPClient

def extract_price_from_image(image_path: str):
    client = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="ZVoEysGPJfyHSHE2i9UV"
    )

    result = client.run_workflow(
        workspace_name="sdp-1ds4f",
        workflow_id="sdp-model",
        images={"image": image_path},
        use_cache=True
    )

    try:
        output = result[0]["llama_vision"]["output"]
        return [output]
    except (IndexError, KeyError, TypeError):
        return ["0.00"]