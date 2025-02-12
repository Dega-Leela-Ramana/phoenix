import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import threading
import whisper

# --- Configuration ---
MODEL_SIZE = "base"  # Choose from "tiny", "base", "small", "medium", "large"
# "tiny" is fastest, "large" is most accurate, but slower. "base" is a good starting point.

# --- Functions ---

def load_model():
    global model
    model = whisper.load_model(MODEL_SIZE)
    status_text.insert(tk.END, f"Model '{MODEL_SIZE}' loaded.\n")
    status_text.see(tk.END)  # Scroll to end

def transcribe_audio(audio_path):
    try:
        status_text.insert(tk.END, f"Transcribing '{audio_path}'...\n")
        status_text.see(tk.END)
        result = model.transcribe(audio_path)
        transcription = result["text"]
        transcription_text.delete("1.0", tk.END)  # Clear previous transcription
        transcription_text.insert("1.0", transcription)
        status_text.insert(tk.END, "Transcription complete.\n")
        status_text.see(tk.END)


    except Exception as e:
        status_text.insert(tk.END, f"Error during transcription: {e}\n")
        status_text.see(tk.END)

def browse_file():
    filename = filedialog.askopenfilename(
        initialdir=".",
        title="Select an Audio File",
        filetypes=(("Audio Files", "*.wav;*.mp3;*.m4a"), ("All Files", "*.*")),
    )
    if filename:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filename)


def start_transcription():
    audio_path = file_path_entry.get()
    if not audio_path:
        status_text.insert(tk.END, "Please select an audio file.\n")
        status_text.see(tk.END)
        return

    if not os.path.exists(audio_path):
        status_text.insert(tk.END, "File not found.\n")
        status_text.see(tk.END)
        return
    # Run transcription in a separate thread to prevent UI freezing
    threading.Thread(target=transcribe_audio, args=(audio_path,), daemon=True).start()


# --- UI Setup (Tkinter) ---

root = tk.Tk()
root.title("Whisper Audio Transcription")

# File Selection
file_path_label = tk.Label(root, text="Audio File:")
file_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Transcription Button
transcribe_button = tk.Button(root, text="Transcribe", command=start_transcription)
transcribe_button.grid(row=1, column=1, padx=5, pady=5)

# Transcription Text Area
transcription_label = tk.Label(root, text="Transcription:")
transcription_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

transcription_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
transcription_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Status / Log Area
status_label = tk.Label(root, text="Status:")
status_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

status_text = scrolledtext.ScrolledText(root, height=5, width=60)
status_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
status_text.config(state=tk.NORMAL)  # Allow text insertion

# --- Initialization ---
status_text.insert(tk.END, "Loading model in background...\n")
status_text.see(tk.END)
threading.Thread(target=load_model, daemon=True).start()  # Load model in background

root.grid_columnconfigure(1, weight=1)  # Make the entry field expandable

root.mainloop()