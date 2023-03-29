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
    print(request.values['token'])
    file = request.files['file']
    file_path = f"./unprocessed/{secure_filename(file.filename)}"
    file.save(file_path)
    processedImagePath = processImage(file_path)
    text = predictText(processedImagePath)
    os.remove(processedImagePath)

    return make_response({"text": text}, 200)

if __name__ == "__main__":
    app.run()