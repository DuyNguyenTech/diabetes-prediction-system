from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

# KHOI TAO FLASK APP
app = Flask(__name__)

# Cho phep Frontend goi vao API nay (Tranh loi bao mat CORS)
CORS(app)

# TAI MO HINH DA HUAN LUYEN
print("Dang khoi dong Server va tai Model...")

# 1. Tai file model.pkl (Bo nao AI)
# Luu y: Dam bao file nay nam trong thu muc model/
model = joblib.load('model/diabetes_model.pkl')

# 2. Tai nguong cat toi uu (threshold.txt)
try:
    with open('model/threshold.txt', 'r') as f:
        THRESHOLD = float(f.read().strip())
    print(f"-> Da tai nguong quyet dinh toi uu: {THRESHOLD}")
except:
    THRESHOLD = 0.3712 # Dung con so ban da nghien cuu lam mac dinh
    print(f"-> Khong tim thay file nguong, su dung mac dinh {THRESHOLD}")

# DINH NGHIA API

# 1. API Health Check (DUNG DE FIX LOI CRON-JOB)
# Dung Endpoint nay de ping, tra ve ket qua cuc ky nhe de tranh loi "Response data too big"
@app.route('/health', methods=['GET'])
def health():
    return "ok", 200

# 2. API Trang chu (Giu nguyen cua ban)
@app.route('/', methods=['GET'])
def home():
    return "He thong du doan Tieu duong dang hoat dong tot!"

# 3. API Du doan (Predict) [cite: 407, 746, 614-617]
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Nhan du lieu JSON tu Frontend gui len
        data = request.json
        print("-> Nhan du lieu tu nguoi dung:", data)
        
        # Chuyen du lieu thanh DataFrame
        df = pd.DataFrame([data])
        
        # TIEN XU LY [cite: 615, 649, 705-706]
        # Quy doi thong tin hut thuoc cho khop voi quy tac cua Model cua ban
        if 'smoking_history' in df.columns:
            df['smoking_history'] = df['smoking_history'].replace({
                'No Info': 'never', 
                'current': 'current', 
                'ever': 'former', 
                'former': 'former', 
                'not current': 'former'
            })
        
        # DU DOAN BANG AI [cite: 616, 707-708, 818]
        # Lay xac suat mac benh (0.0 den 1.0)
        prob_sick = model.predict_proba(df)[0, 1]
        
        # So sanh voi Nguong toi uu (THRESHOLD) [cite: 302-303, 818, 908-910]
        if prob_sick >= THRESHOLD:
            prediction = 1 # Du doan: CO BENH
            result_text = "Nguy co CAO"
        else:
            prediction = 0 # Du doan: KHOE MANH
            result_text = "Nguy co THAP"
            
        # Tra ket qua ve cho Frontend [cite: 617, 650, 693]
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'result_text': result_text,
            'probability': float(prob_sick),
            'threshold': THRESHOLD
        })

    except Exception as e:
        print("LOI:", str(e))
        return jsonify({'status': 'error', 'message': str(e)})

# --- CHAY SERVER ---
if __name__ == '__main__':
    # Render se tu cap phat Port thong qua bien moi truong [cite: 1112]
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)