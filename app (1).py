import streamlit as st
import nltk
from gtts import gTTS
import os
import tempfile

# Download necessary NLTK resources
nltk.download('punkt')

def text_to_speech(text, language='en'):
    """Converts text to speech and offers download functionality."""

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Create a temporary directory for audio files
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_files = []

        # Convert each sentence to speech and save to temporary files
        for idx, sentence in enumerate(sentences):
            tts = gTTS(text=sentence, lang=language, slow=False)
            filename = f"output_{idx}.mp3"
            filepath = os.path.join(tmpdir, filename)
            tts.save(filepath)
            audio_files.append(filepath)

        # Concatenate the audio files (optional for single sentence input)
        if len(sentences) > 1:
            output_filename = "final_output.mp3"
            output_filepath = os.path.join(tmpdir, output_filename)
            os.system(f"ffmpeg -i \"concat:{'|'.join(audio_files)}\" {output_filepath}")
            audio_to_download = output_filepath
        else:
            audio_to_download = audio_files[0]  # Use the first file for single sentence

        # Download the audio file using Streamlit download_button
        with open(audio_to_download, "rb") as f:
            st.download_button(label="Download Audio", data=f, file_name="speech.mp3")

        # Clean up temporary audio files (not strictly necessary in this case)
        for file in audio_files:
            os.remove(file)

    st.success("Text-to-speech conversion complete.")

def main():
    st.title("Text to Speech Converter")

    input_text = st.text_area("Enter text to convert to speech")

    if st.button("Convert to Speech"):
        if input_text:
            text_to_speech(input_text)
        else:
            st.warning("Please enter some text to convert.")

if __name__ == "__main__":
    main()