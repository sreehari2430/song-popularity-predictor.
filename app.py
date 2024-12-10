import streamlit as st
import pickle
import shap
import matplotlib.pyplot as plt

# Load pre-trained pipeline
pp = pickle.load(open(r'C:\LUMINAR\PROJECT\song\pipeline (1).sav', 'rb'))

# Metadata
MODEL_VERSION = "1.0.0"
TRAINING_DATE = "2024-11-01"

# Custom CSS
def inject_css():
    """Inject custom CSS for better UI."""
    st.markdown(
        """
        <style>
            /* Main Page Styling */
            body {
                background-color: #f4f4f4;
                font-family: 'Arial', sans-serif;
            }

            /* Header and Subheader Styling */
            h1, h2, h3, h4, h5 {
                color: #4a4a4a;
            }

            /* Buttons */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                padding: 8px 15px;
            }
            .stButton>button:hover {
                background-color: #45a049;
                transition: 0.3s;
            }

            /* Tabs Styling */
            .stTabs [role="tablist"] {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }

            /* Footer Styling */
            footer {
                visibility: hidden;
            }

            /* Input Field Styling */
            input, textarea, select {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;
            }

            /* Success and Error Messages */
            .stSuccess {
                background-color: #e7f5e6;
                color: #2e7d32;
                border-radius: 5px;
                padding: 10px;
            }
            .stError {
                background-color: #fbe9e7;
                color: #c62828;
                border-radius: 5px;
                padding: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def predict_popularity(features):
    """Predict the popularity of a song based on input features."""
    try:
        prediction = pp.predict([features])
        return prediction[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None


def display_pipeline_components():
    """Display the components of the pipeline."""
    st.subheader("🔧 Pipeline Components")
    for name, step in pp.steps:
        st.markdown(f"- **{name.capitalize()}**: {step}")


def download_results(song_name, prediction):
    """Allow users to download results."""
    result_data = f"Song Name: {song_name if song_name else 'Unnamed Song'}\nPredicted Popularity: {prediction}"
    st.download_button(
        label="📥 Download Results",
        data=result_data,
        file_name="prediction_results.txt",
        mime="text/plain",
    )


def prediction_tab():
    """Prediction functionality."""
    with st.form("song_details_form"):
        st.header("🎤 Enter Song Details")

        # Inputs for song features
        song_name = st.text_input("🎵 Song Name", help="Enter the name of the song (optional).")
        song_duration_ms = st.slider(
            "📏 Song Duration (ms)",
            min_value=100,
            max_value=300000,
            step=1,
            help="Duration of the song in milliseconds.",
        )
        acousticness = st.slider(
            "🎻 Acousticness", 
            min_value=0.0, 
            max_value=1.0, 
            step=0.0001,
            format="%.6f",
            help="Measure of the acoustic sound in the song.",
        )
        danceability = st.slider(
            "💃 Danceability", 
            min_value=0.0, 
            max_value=1.0, 
            step=0.001, 
            format="%.3f", 
            help="How suitable the song is for dancing.",
        )
        liveness = st.slider(
            "🎙️ Liveness", 
            min_value=0.0, 
            max_value=1.0, 
            step=0.0001, 
            format="%.4f", 
            help="Presence of an audience in the recording.",
        )
        loudness = st.slider(
            "🔊 Loudness (dB)", 
            min_value=-60.0, 
            max_value=1.0, 
            step=0.001, 
            format="%.3f", 
            help="Overall loudness of the song.",
        )
        tempo = st.slider(
            "🎶 Tempo (BPM)", 
            min_value=50.0, 
            max_value=300.0, 
            step=0.1, 
            format="%.1f", 
            help="Tempo of the song in beats per minute (BPM).",
        )
        audio_valence = st.slider(
            "🎧 Audio Valence", 
            min_value=0.0, 
            max_value=1.0, 
            step=0.001, 
            format="%.3f", 
            help="Musical positivity of the track.",
        )

        # Submit Button
        submit_button = st.form_submit_button(label="Predict Popularity 🎯")

    # Prediction logic
    if submit_button:
        # Collect features into a list
        features = [
            song_duration_ms,
            acousticness,
            danceability,
            liveness,
            loudness,
            tempo,
            audio_valence,
        ]
        
        if all(f is not None for f in features):
            prediction = predict_popularity(features)
            
            st.write("---")
            st.subheader(f"Results for: **{song_name if song_name else 'Unnamed Song'}**")

            if prediction is not None:
                st.success(f"The predicted popularity score is **{prediction}** 🎉")

                # Allow results download
                download_results(song_name, prediction)

            else:
                st.error("Could not generate a prediction. Please try again.")
        else:
            st.error("Please ensure that all fields (except Song Name) are filled in correctly.")


def information_tab():
    """App information and instructions."""
    st.header("ℹ️ About the App")
    st.info(
        """
        **Song Popularity Predictor** is a machine learning application that predicts the popularity score 
        of a song based on various musical and audio features.  

        ---  
        **Features Considered**: 
        - **Song Duration (ms)** Total duration of the song in milliseconds. 
        - **Acousticness** Measure of the acoustic sound level in the track (0.0–1.0).
        - **Danceability** Evaluates how suitable the track is for dancing (0.0–1.0).
        - **Liveness** Detects audience presence in the recording (0.0–1.0).
        - **Loudness (dB)** Overall volume of the track in decibels.
        - **Tempo (BPM)** Tempo of the song in beats per minute.
        - **Audio Valence** Reflects musical positivity or mood (0.0–1.0).
        """
    )
    display_pipeline_components()
    st.markdown(
        f"""
        - **Model Version**: {MODEL_VERSION}  
        - **Training Date**: {TRAINING_DATE}
        """
    )
    st.markdown("---")
    st.markdown("Developed by: **Sreehari V** 🎓")


# Main function to handle tabs
def main():
    
    st.set_page_config(
        page_title="🎵 Advanced Song Popularity Predictor",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    # Display tabs
    tab1, tab2 = st.tabs(["🎤 Prediction", "ℹ️ Information"])

    with tab1:
        prediction_tab()

    with tab2:
        information_tab()


main()
