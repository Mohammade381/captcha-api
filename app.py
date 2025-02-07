from flask import Flask, request, render_template, jsonify
import pytesseract
import cv2
import numpy as np
import sympy as sp
from PIL import Image

app = Flask(__name__)

# تنظیم مسیر Tesseract برای OCR (در ویندوز باید مسیر دقیق داده شود)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# بهینه‌سازی تصویر قبل از OCR
def preprocess_image(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)  # تبدیل به تصویر خاکستری
    image = cv2.GaussianBlur(image, (5, 5), 0)  # کاهش نویز با بلور گوسی
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # باینری‌سازی تصویر
    return Image.fromarray(image)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    lang = request.form['lang']
    if file:
        image = Image.open(file)
        image = preprocess_image(image)  # پردازش تصویر قبل از OCR
        text = pytesseract.image_to_string(image, lang=lang)
        return jsonify({'extracted_text': text})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    try:
        result = sp.sympify(expression)
        return jsonify({'result': str(result)})
    except Exception:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=True)
