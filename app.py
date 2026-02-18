import streamlit as st
import joblib
import os
import pandas as pd
from datetime import datetime

# load model
model = joblib.load("stress_prediction.pkl")

scale = pd.DataFrame({
    'answer': ['Tidak sama sekali', 'Sangat jarang', 'Jarang', 'Cukup', 'Cukup sering', 'Sangat sering']
})

scale_2 = pd.DataFrame({
    'answer': ['Sangat buruk', 'Buruk', 'Normal', 'Baik', 'Cukup baik', 'Sangat baik']
})

scale_3 = pd.DataFrame({
    'answer': ['Sangat tidak terpenuhi', 'Tidak terpenuhi', 'Kurang terpenuhi', 'Cukup', 'Cukup terpenuhi', 'Sangat terpenuhi']
})

scale_4 = pd.DataFrame({
    'answer': ['Sangat buruk', 'Buruk', 'Baik', 'Sangat baik']
})

scale_5 = pd.DataFrame({
    'answer': ['Tidak', 'Iya']
})

scale_list = scale['answer'].tolist()
scale_2_list = scale_2['answer'].tolist()
scale_3_list = scale_3['answer'].tolist()
scale_4_list = scale_4['answer'].tolist()
scale_5_list = scale_5['answer'].tolist()

def encode(answer, scale_list):
    return scale_list.index(answer)


def save_numeric(data_input, pred):
    file_path = "numeric_inputs.csv"

    data_input = data_input.copy()
    data_input["predicted_stress"] = pred

    if not os.path.isfile(file_path):
        data_input.to_csv(file_path, index=False)
    else:
        data_input.to_csv(file_path, mode="a", header=False, index=False)

def save_data(data_input):
    file_path = "data_input.csv"

    if not os.path.isfile(file_path):
        data_input.to_csv(file_path, index=False)
    else:
        data_input.to_csv(file_path, mode="a", header=False, index=False)

st.set_page_config(page_title="Kita Waras", layout="wide")

st.title("Kita Waras")

st.write("")

st.subheader("Data Diri")

col1, col2 = st.columns(2, gap="large")

with col1:
    name_ans = st.text_input("Nama")
    age_ans = st.number_input("Umur", min_value=0, max_value=100, step=1)

st.write("")

st.subheader("Pertanyaan")

col1, col2 = st.columns(2, gap="large")

def col1_builder(input, mode):
    with col1:
        if (mode == 1) :
            select = st.selectbox(input, scale, key=input)
        elif (mode == 2) :
            select = st.selectbox(input, scale_2, key=input)
        elif (mode == 3) :
            select = st.selectbox(input, scale_3, key=input)
        elif (mode == 4) :
            select = st.selectbox(input, scale_4, key=input)
        elif (mode == 5) :
            select = st.selectbox(input, scale_5, key=input)
        st.write("")
        return select

def col2_builder(input, mode):
    with col2:
        if (mode == 1) :
            select = st.selectbox(input, scale, key=input)
        elif (mode == 2) :
            select = st.selectbox(input, scale_2, key=input)
        elif (mode == 3) :
            select = st.selectbox(input, scale_3, key=input)
        elif (mode == 4) :
            select = st.selectbox(input, scale_4, key=input)
        elif (mode == 5) :
            select = st.selectbox(input, scale_5, key=input)
        st.write("")
        return select


mental_health_history_ans = col1_builder("Apakah kamu pernah punya masalah kesehatan mental sebelumnya?", 5)
sleep_quality_ans = col2_builder("Bagaimana kualitas tidurmu (sulit mulai tidur, sering terbangun)?", 2)
headache_ans = col1_builder("Apakah kamu akhir-akhir ini lebih sering sakit kepala dari biasanya?", 1)
breathing_problem_ans = col2_builder("Apakah kamu pernah merasa sesak atau sulit bernapas belakangan ini?", 1)
living_conditions_ans = col1_builder("Apakah kondisi rumah atau tempat tinggalmu bikin kamu kurang nyaman?", 2)
safety_ans = col2_builder("Apakah kamu merasa kurang aman di lingkungan tempat tinggal atau tempat kamu beraktivitas?", 2)
basic_needs_ans = col1_builder("Apakah kebutuhan dasarmu (makan, istirahat, keuangan) akhir-akhir ini terasa sulit terpenuhi?", 3)
academic_performance_ans = col2_builder("Apakah kamu kesulitan fokus atau konsentrasi saat mengerjakan tugas kuliah?", 2)
study_load_ans = col1_builder("Seberapa sering kamu merasa kewalahan dengan tugas dan beban kuliah?", 1)
teacher_student_relationship_ans = col2_builder("Bagaimana hubungan kamu dengan dosen atau pengajarmu?", 2)
future_career_concerns_ans = col1_builder("Apakah kamu sering kepikiran atau khawatir soal karier di masa depan?", 1)
social_support_ans = col2_builder("Bagaimana hubungan kamu dengan orang sekitarmu?", 4)
peer_pressure_ans = col1_builder("Seberapa sering kamu merasa tertekan oleh teman kampusmu?", 1)
extracurricular_activities_ans = col2_builder("Seberapa sering perkuliahanmu teganggu oleh ekstrakurikuler atau kegiatan organisasi?", 1)
bullying_ans = col1_builder("Seberapa sering kamu mengalami perundungan atau pelecehan?", 1)

st.write("")

is_clicked = st.button("Prediksi",)

def clicked():
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if name_ans == "" or age_ans == 0:
        st.warning("Mohon isi nama dan umur terlebih dahulu.")
        return

    model_input = pd.DataFrame({
        'mental_health_history': [encode(mental_health_history_ans, scale_5_list)],
        'headache': [encode(headache_ans, scale_list)],
        'sleep_quality': [encode(sleep_quality_ans, scale_2_list)],
        'breathing_problem': [encode(breathing_problem_ans, scale_list)],
        'living_conditions': [encode(living_conditions_ans, scale_2_list)],
        'safety': [encode(safety_ans, scale_2_list)],
        'basic_needs': [encode(basic_needs_ans, scale_3_list)],
        'academic_performance': [encode(academic_performance_ans, scale_2_list)],
        'study_load': [encode(study_load_ans, scale_list)],
        'teacher_student_relationship': [encode(teacher_student_relationship_ans, scale_2_list)],
        'future_career_concerns': [encode(future_career_concerns_ans, scale_list)],
        'social_support': [encode(social_support_ans, scale_4_list)],
        'peer_pressure': [encode(peer_pressure_ans, scale_list)],
        'extracurricular_activities': [encode(extracurricular_activities_ans, scale_list)],
        'bullying': [encode(bullying_ans, scale_list)]
    })

    pred = model.predict(model_input)[0]

    data_input = pd.DataFrame({
        'name': [name_ans],
        'age': [age_ans],
        'mental_health_history': [mental_health_history_ans],
        'headache': [headache_ans],
        'sleep_quality': [sleep_quality_ans],
        'breathing_problem': [breathing_problem_ans],
        'living_conditions': [living_conditions_ans],
        'safety': [safety_ans],
        'basic_needs': [basic_needs_ans],
        'academic_performance': [academic_performance_ans],
        'study_load': [study_load_ans],
        'teacher_student_relationship': [teacher_student_relationship_ans],
        'future_career_concerns': [future_career_concerns_ans],
        'social_support': [social_support_ans],
        'peer_pressure': [peer_pressure_ans],
        'extracurricular_activities': [extracurricular_activities_ans],
        'bullying': [bullying_ans]
    })

    numeric_data = model_input.copy()
    numeric_data.insert(0, "age", age_ans)
    numeric_data.insert(0, "name", name_ans)
    numeric_data.insert(0, "timestamp", timestamp)
    save_numeric(numeric_data, pred)

    st.subheader("Hasil Prediksi")
    st.write(f"Jenis stres apa yang paling sering kamu rasakan : ")

    output = 'Tidak diketahui'
    if (pred == 0) :
        output = "Tidak merasa Stress - Saat ini mengalami stress yang sangat minimal atau tidak mengalami stress"
        st.info(output)
    elif (pred == 1) :
        output = "Eustres (Stres Positif) – Stres yang bikin kamu jadi lebih termotivasi dan meningkatkan performamu."
        st.success(output)
    else :
        output = "Distres (Stres Negatif) – Stres yang menimbulkan kecemasan dan menggangu kondisi mental."
        st.error(output)

    data_input['predicted_stress'] = output
    data_input.insert(0, "timestamp", timestamp)
    save_data(data_input)

if (is_clicked) :
    clicked()