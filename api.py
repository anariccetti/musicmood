import fastapi
import uvicorn
from pydantic import BaseModel
from simpletransformers.classification import ClassificationModel
from scipy.special import softmax


# url = 'http://base_url/'

class Music(BaseModel):
    lyrics: str

api = fastapi.FastAPI()

@api.get("/")
def index():
    return {"message": "Hello World"}

@api.get("/predict-mood")
def predict_mood(music: Music) -> dict:
    model = ClassificationModel("xlnet", "models", use_cuda=False)
    predictions, raw_outputs = model.predict([music.lyrics])
    probabilities = softmax(raw_outputs, axis=1)
    
    response = f'{probabilities[0]}'

    return response
