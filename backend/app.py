from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

#KHOI TAO FLASK APP
#Backend su dung Python Flask
app = Flask(__name__)

# Cho phep Frontend goi vao API nay (Tranh loi bao mat CORS)
CORS(app)

#TAI MO HINH DA HUAN LUYEN
print("Dang khoi dong Server va tai Model...")

# 1. Tai file model.pkl (Bo nao AI)
model = joblib.load('model/diabetes_model.pkl')

# 2. Tai nguong cat toi uu (threshold.txt) ma ban vua tim duoc
# Neu khong co file thi dung mac dinh 0.5
try:
    with open('model/threshold.txt', 'r') as f:
        THRESHOLD = float(f.read().strip())
    print(f"-> Da tai nguong quyet dinh toi uu: {THRESHOLD}")
except:
    THRESHOLD = 0.5
    print("-> Khong tim thay file nguong, su dung mac dinh 0.5")

#DINH NGHIA API (Cac cong ket noi)

# 1. API Kiem tra hoat dong (Health Check)
@app.route('/', methods=['GET'])
def home():
    return "He thong du doan Tieu duong dang hoat dong tot!"

# 2. API Du doan (Predict) - QUAN TRONG NHAT
#Phat trien API du doan endpoint /predict
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Nhan du lieu JSON tu Frontend gui len
        data = request.json
        print("-> Nhan du lieu tu nguoi dung:", data)
        
        # Chuyen du lieu thanh DataFrame (Bang 1 dong)
        df = pd.DataFrame([data])
        
        #TIEN XU LY
        # Quy doi thong tin hut thuoc cho khop voi quy tac cua Model
        if 'smoking_history' in df.columns:
            df['smoking_history'] = df['smoking_history'].replace({
                'No Info': 'never', 
                'current': 'current', 
                'ever': 'former', 
                'former': 'former', 
                'not current': 'former'
            })
        
        #DU DOAN BANG AI
        # Lay xac suat mac benh (0.0 den 1.0)
        prob_sick = model.predict_proba(df)[0, 1]
        
        # So sanh voi Nguong toi uu (0.3712)
        if prob_sick >= THRESHOLD:
            prediction = 1 # Du doan: CO BENH
            result_text = "Nguy co CAO"
        else:
            prediction = 0 # Du doan: KHOE MANH
            result_text = "Nguy co THAP"
            
        # Tra ket qua ve cho Frontend
        return jsonify({
            'status': 'success',
            'prediction': prediction,       # 0 hoac 1
            'result_text': result_text,     # Chu de hien thi
            'probability': float(prob_sick), # Xac suat thuc te (vd: 0.45)
            'threshold': THRESHOLD          # Nguong da dung de so sanh
        })

    except Exception as e:
        # Neu co loi thi bao lai
        print("LOI:", str(e))
        return jsonify({'status': 'error', 'message': str(e)})

# --- CHAY SERVER ---
if __name__ == '__main__':
    # Chay tren cong 5000
    app.run(host='0.0.0.0', port=5000, debug=True)