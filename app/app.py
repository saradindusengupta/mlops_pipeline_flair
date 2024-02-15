# Load the libraries.
from fastapi import FastAPI
from pydantic import BaseModel
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


# Load the model in as a global variable.
classifier = TextClassifier.load(f"{working_dir}model/final-model.pt")

# Define the prediction function.
def classify_text(classifier, sentence):

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

    sentence = Sentence(sentence)
    classifier.predict(sentence)
    return sentence.labels


# Initialize the FastAPI endpoint.
app = FastAPI()

# Set the address and await calls.
@app.post("/classify-text")
async def classify_text_endpoint(Case: Case):
    """Takes the text request and returns a record with the labels & associated probabilities."""

    # Use the pretrained model to classify the incoming text in the request.
    classified_text = classify_text(classifier, Case.text)

    return classified_text