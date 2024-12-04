# app.py
from flask import Flask, request, jsonify
import os
import librosa
import numpy as np
import joblib
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Determine the base directory of your project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Attempt to load SVM model with robust error handling
def load_svm_model():
    model_paths = [
        os.path.join(BASE_DIR, 'SVM.pkl'),
        os.path.join(os.path.dirname(BASE_DIR), 'SVM.pkl'),
        'SVM.pkl'
    ]
    
    for path in model_paths:
        try:
            print(f"Attempting to load model from: {path}")
            if os.path.exists(path):
                model = joblib.load(path)
                print(f"Model successfully loaded from {path}")
                return model
        except Exception as e:
            print(f"Failed to load model from {path}: {e}")
    
    print("Could not load SVM model from any location")
    return None

# Load the model once when the application starts
svm_model = load_svm_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/") 
def home():
    return "Hello, Flask!"

@app.route('/uploaderSVM', methods=['POST'])
def upload_file_svm():
    # Comprehensive file validation
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .wav files are allowed."}), 400
    
    if svm_model is None:
        return jsonify({"error": "SVM model could not be loaded"}), 500
    
    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and process audio
        signal, rate = librosa.load(filepath, sr=None)
        
        if signal is None or len(signal) == 0:
            return jsonify({"error": "Failed to load audio data"}), 400
        
        # Feature extraction
        S = librosa.feature.melspectrogram(y=signal, sr=rate, n_fft=2048, hop_length=512, n_mels=128)
        S_DB = librosa.power_to_db(S, ref=np.max).flatten()[:58]
        
        # Prediction
        ans = svm_model.predict([S_DB])[0]
        music_class = str(ans)
        
        #return jsonify({"result": music_class}), 200
        return render_template("svm.html", result=music_class)
    
    except Exception as e:
        print(f"Unexpected error processing file: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
