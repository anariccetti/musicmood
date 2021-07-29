import fastapi
import uvicorn
from pydantic import BaseModel

# url = 'http://base_url/'

class Music(BaseModel):
    lyrics: str

api = fastapi.FastAPI()

@api.get("/")
def index():
    return {"message": "Hello World"}

@api.get("/predict-mood")
def predict_mood():
    pass
