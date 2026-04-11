from pathlib import Path
import joblib
import pandas as pd
import streamlit as st


st.markdown("""
<style>
.big-title {
    font-size:40px;
    text-align:center;
    animation: fadeIn 2s;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Heart Disease Predictor ❤️",
    page_icon="❤️",
    layout="wide"
)

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "KNN_Heart.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
COLUMNS_PATH = BASE_DIR / "columns.pkl"

# ---------------- LOAD ----------------
@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    expected_columns = joblib.load(COLUMNS_PATH)
    return model, scaler, expected_columns

# ---------------- INPUT FRAME ----------------
def build_input_frame(expected_columns, inputs):
    data = {col: 0 for col in expected_columns}

    data["Age"] = inputs["Age"]
    data["RestingBP"] = inputs["RestingBP"]
    data["Cholesterol"] = inputs["Cholesterol"]
    data["FastingBS"] = inputs["FastingBS"]
    data["MaxHR"] = inputs["MaxHR"]
    data["Oldpeak"] = inputs["Oldpeak"]

    one_hot_map = {
        f"Sex_{inputs['Sex']}": 1,
        f"ChestPainType_{inputs['ChestPainType']}": 1,
        f"RestingECG_{inputs['RestingECG']}": 1,
        f"ExerciseAngina_{inputs['ExerciseAngina']}": 1,
        f"ST_Slope_{inputs['ST_Slope']}": 1,
    }

    for col, val in one_hot_map.items():
        if col in data:
            data[col] = val

    return pd.DataFrame([data], columns=expected_columns)

# ---------------- LOAD MODEL ----------------
try:
    model, scaler, expected_columns = load_artifacts()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("❤️ Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🧠 Prediction", "ℹ️ About"])

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown(
        """
        <h1 style='text-align:center;'>❤️ Heart Disease Predictor</h1>
        <p style='text-align:center; font-size:18px;'>
        AI-powered app to predict heart disease risk
        </p>
        """,
        unsafe_allow_html=True
    )

    st.image("https://images.unsplash.com/photo-1588776814546-ec7eec7b8a86", use_container_width=True)

    st.info("👉 Go to Prediction tab to test the model")

# ---------------- PREDICTION ----------------
elif page == "🧠 Prediction":

    st.title("🧠 Prediction Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 100, 40)
        sex = st.selectbox("Sex", ["M", "F"])
        chest_pain = st.selectbox("Chest Pain", ["ASY", "ATA", "NAP", "TA"])
        resting_bp = st.number_input("Resting BP", 80, 250, 120)
        cholesterol = st.number_input("Cholesterol", 0, 700, 200)

    with col2:
        fasting_bs = st.selectbox("Fasting BS >120", [0, 1])
        resting_ecg = st.selectbox("Resting ECG", ["LVH", "Normal", "ST"])
        max_hr = st.slider("Max HR", 60, 220, 150)
        exercise_angina = st.selectbox("Exercise Angina", ["N", "Y"])
        oldpeak = st.slider("Oldpeak", 0.0, 7.0, 1.0)
        st_slope = st.selectbox("ST Slope", ["Down", "Flat", "Up"])

    if st.button("🚀 Predict Now"):

        with st.spinner("Analyzing data..."):
            user_input = {
                "Age": age,
                "Sex": sex,
                "ChestPainType": chest_pain,
                "RestingBP": resting_bp,
                "Cholesterol": cholesterol,
                "FastingBS": fasting_bs,
                "RestingECG": resting_ecg,
                "MaxHR": max_hr,
                "ExerciseAngina": exercise_angina,
                "Oldpeak": oldpeak,
                "ST_Slope": st_slope,
            }

            input_df = build_input_frame(expected_columns, user_input)
            scaled = scaler.transform(input_df)
            prediction = int(model.predict(scaled)[0])

        st.subheader("📊 Result")

        if prediction == 1:
            st.error("⚠️ High Risk of Heart Disease")
            st.progress(90)
        else:
            st.success("✅ Low Risk")
            st.progress(30)

        st.caption("⚠️ This is not medical advice")

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":
    st.title("ℹ️ About Project")

    st.write("""
    This project uses Machine Learning to predict heart disease.
    
    🔹 Models Used:
    - KNN
    - Logistic Regression
    - SVM
    
    🔹 Built with:
    - Python
    - Streamlit
    - Scikit-learn
    """)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;'>Made with ❤️ by Satya</p>
    """,
    unsafe_allow_html=True
)