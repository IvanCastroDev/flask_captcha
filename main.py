from model import model, predictText
from flask import Flask, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from images import processImage
import json
import  os

UPLOAD_FOLDER = '/captchas'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
@app.route('/test')
def test():
    return '<p>Test</p>'

@app.route('/captcha', methods=['POST'])
def resolve_captcha():
    file = request.files['file']
    file_path = f"./captchas/{secure_filename(file.filename)}"
    file.save(file_path)
    text = predictText(file_path)
    os.remove(file_path)
    return make_response({"text": text}, 200)

@app.route('/mayaCaptcha', methods=['POST'])
def processAndResolveCaptcha():
    file = request.files['file']
    token = request.values['token']

    if token != 'xeNqzRVoamixNAcp.B7$dkE$$Mx*#C9ZIHtz3#4IYabhzU/GA.xkSduW5mMg4sH1aQYjGiAu2RYyN1uVcuy33%bmBJksHY27Wv-h5CFlQOL/RIgUHcj4xum%kK-$n.bxbv-GYr*DD8r3yh5jC7SLkHU!#SyJMMoejw-!hPEp9wIk5#sU8N$YEV1UJ-90Js6IS$vwSK.C/':
        return make_response({"error": 'Token no autorizado'}, 401)

    file_path = f"./unprocessed/{secure_filename(file.filename)}"
    file.save(file_path)
    processedImagePath = processImage(file_path)
    text = predictText(processedImagePath)
    os.remove(processedImagePath)

    return make_response({"text": text}, 200)

if __name__ == "__main__":
    app.run()