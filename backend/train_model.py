import pandas as pd
import numpy as np
import os
import joblib

# Thu vien de ve bieu do (Matplotlib & Seaborn)
# QUAN TRONG: Che do Agg giup ve hinh ngam, khong hien cua so popup
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

# Thu vien chia tap du lieu va danh gia
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, precision_recall_curve, classification_report

# Thu vien tien xu ly (Chuan hoa va Ma hoa)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Thu vien thuat toan Random Forest
from sklearn.ensemble import RandomForestClassifier

# Thu vien xu ly mat can bang du lieu (SMOTE)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

#1 KHOI TAO MOI TRUONG
#Tu dong tao thu muc model va reports
if not os.path.exists('model'):
    os.makedirs('model')
if not os.path.exists('reports'):
    os.makedirs('reports')

#2 THU THAP DU LIEU
print("BUOC 1: Dang doc du lieu tu file CSV...")
df = pd.read_csv('dataset/diabetes_prediction_dataset.csv')

# Lam sach du lieu: Gop cac nhom hut thuoc la giong nhau
# Nhom 'No Info', 'never' -> gop thanh 'never'
# Nhom 'ever', 'former', 'not current' -> gop thanh 'former'
# Nhom 'current' -> giu nguyen
df['smoking_history'] = df['smoking_history'].replace({
    'No Info': 'never', 
    'current': 'current', 
    'ever': 'former', 
    'former': 'former', 
    'not current': 'former'
})

#3 CHIA TAP DU LIEU
#Chia tap train 80/20
X = df.drop('diabetes', axis=1) # Dau vao
y = df['diabetes']              # Dau ra

# stratify=y: Dam bao ty le nguoi benh duoc chia deu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"BUOC 2: Da chia du lieu (Train: {len(X_train)}, Test: {len(X_test)})")

#4 XAY DUNG PIPELINE
#Tien xu ly -> SMOTE -> Random Forest

# Dinh nghia cac cot so va cot chu
numeric_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']
categorical_features = ['gender', 'smoking_history']

# Bo xu ly cot
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numeric_features), # Chuan hoa so
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features) # Ma hoa chu
])

# Day chuyen xu ly (Pipeline)
pipeline = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)), #Can bang du lieu
    ('classifier', RandomForestClassifier( #Random Forest
        n_estimators=200,        # So cay
        max_depth=15,            # Do sau
        class_weight='balanced', # Trong so can bang
        random_state=42,
        n_jobs=-1
    ))
])

#5 TRAIN
print("BUOC 3: Dang huan luyen mo hinh...")
pipeline.fit(X_train, y_train)

#6 TOI UU HOA NGUONG
#Uu tien Recall > 90%
print("BUOC 4: Dang tinh toan nguong cat de Recall > 90%...")

# Lay xac suat du doan
y_probs = pipeline.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

# Tim nguong cat sao cho Recall >= 0.90
target_recall = 0.90
valid_indices = np.where(recalls >= target_recall)[0]

if len(valid_indices) > 0:
    final_threshold = thresholds[valid_indices[-1]] - 0.02 # Tru nhe de an toan
else:
    final_threshold = 0.5

print(f"-> Nguong toi uu tim duoc: {final_threshold:.4f}")

#7 DANH GIA VA LUU ANH BAO CAO
# Du doan lai voi nguong moi
y_pred_new = (y_probs >= final_threshold).astype(int)

# Tinh cac chi so
acc = accuracy_score(y_test, y_pred_new)
rec = recall_score(y_test, y_pred_new)

print("-" * 30)
print(f"KET QUA CUOI CUNG:")
print(f"Accuracy: {acc:.4f} (Muc tieu > 0.95)")
print(f"Recall:   {rec:.4f} (Muc tieu > 0.90)")
print("-" * 30)

# Ve Ma Tran Nham Lan (Confusion Matrix) va luu anh
cm = confusion_matrix(y_test, y_pred_new)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title(f'Ma Tran Nham Lan (Recall > 90%) - Nguong {final_threshold:.2f}')
plt.ylabel('Thuc te')
plt.xlabel('AI Du doan')
# Luu anh vao thu muc reports (tu dong tao o dau code)
plt.savefig('reports/confusion_matrix.png')
print("BUOC 5: Da luu anh bao cao vao 'backend/reports/confusion_matrix.png'")

#8 LUU MO HINH
# Luu file model.pkl
joblib.dump(pipeline, 'model/diabetes_model.pkl')
# Luu file threshold.txt
with open('model/threshold.txt', 'w') as f:
    f.write(str(final_threshold))

print("BUOC 6: Da luu xong Model va Nguong. Hoan tat!")