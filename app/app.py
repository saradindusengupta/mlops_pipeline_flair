# Load the libraries.
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
# Load the required modules from Flair.
from flair.models import TextClassifier
from flair.data import Sentence

stage = os.getenv("STAGE")
working_dir = "/root/"
if(stage == "dev"):
    working_dir = "/home/saradindu/dev/mlops_pipeline_flair/"

# Set up the schema & input validation for the inputs.
class Case(BaseModel):
    text: str


# Define the prediction function.
def text_classifier(classifier, text: str):
    """
    A small function to classify the incoming string.
    ------------------------
    Params:
    classifier: The loaded model object.
    sentence: A string to classify.
    ------------------------
    Output:
    A list of tuples containing labels & probabilities.
    """
    try:
        sentence = Sentence(text)
        classifier.predict(sentence)
        return sentence.to_dict()
    except Exception as e:
        print(e)

# Initialize the FastAPI endpoint.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Set the address and await calls.
@app.post("/classify-text")
async def classify_text_endpoint(body: Case):
    """Takes the text request and returns a record with the labels & associated probabilities."""
    
    classifier = TextClassifier.load(f"{working_dir}model/final-model.pt")
    # Use the pretrained model to classify the incoming text in the request.
    classified_text = text_classifier(classifier, body.text)

    return classified_text
@app.get("/info")
def info():
    """General Information"""
    
    response = {'version': '0.0.1', 'author': 'saradindu'}

    return response
