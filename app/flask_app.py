from flask import abort, Flask, jsonify, request
from flair.models import TextClassifier
from flair.data import Sentence
import os

stage = os.getenv("STAGE")
working_dir = "/root/"
if(stage == "dev"):
    working_dir = "/home/saradindu/dev/mlops_pipeline_flair/"
app = Flask(__name__)
 
classifier = TextClassifier.load(f"{working_dir}model/final-model.pt")
 
@app.route('/api/v1/text-classify', methods=['POST'])
def text_classify():
    if not request.json or not 'message' in request.json:
        abort(400)
    message = request.json['message']
    sentence = Sentence(message)
    classifier.predict(sentence)
    #print('Sentence sentiment: ', sentence.labels)
    label = sentence.to_dict()
    return jsonify(label), 200
 
if __name__ == "__main__":
    app.run()