import os
import whisper
from flask import Flask, request, render_template, redirect, url_for
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load Whisper model
model = whisper.load_model("small")  # Options: 'base', 'medium', 'large'

def extract_audio(video_path):
    """Extracts audio from the video and saves it as a .wav file."""
    audio_path = video_path.replace(".mp4", ".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # Ensure correct format
    return audio_path

def transcribe_audio(audio_path):
    """Transcribes audio using Whisper and returns the text."""
    result = model.transcribe(audio_path)
    return result["text"]
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        action = request.form.get("action")  # Check whether login or signup
        if action == "login":
            email = request.form["email"]
            password = request.form["password"]
            return redirect(url_for('home'))
        elif action == "signup":
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            return redirect(url_for('home'))
    
    return render_template("index.html")
@app.route("/home", methods=["GET", "POST"])
def home():
    transcript = None
    if request.method == "POST":
        if "video" not in request.files:
            return redirect(request.url)
        
        file = request.files["video"]
        if file.filename == "":
            return redirect(request.url)
        
        # Save uploaded file
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(video_path)
        # print(video_path)

        # Extract audio and transcribe
        # audio_path = extract_audio(video_path)
        # transcript = transcribe_audio(audio_path)
        # print(transcript)
        # Clean up extracted audio
        # os.remove(audio_path)
        transcript = 'नानी तेरी मोरनी को मोर ले गए बाकी जो बचा था काले चोर ले गए'
        # transcript = 'Welcome to Kids Academy! One, two, three! Look! Here come two more! How many penguins are there in all? Everybody counts! One, two, three! Plus two more makes four, five little penguins!'
        # Redirect to Angular app with transcript text
        # return redirect(f"http://localhost:4200/?text={transcript}")
        return redirect(f"http://localhost:4200/?text={transcript}")
        


    return render_template("home.html", transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
