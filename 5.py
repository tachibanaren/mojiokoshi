import os
import subprocess
import speech_recognition as sr
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar

def convert_to_wav(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path)
    audio.export(output_file_path, format="wav")

def recognize_audio(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language='ja-JP')
        return text
    except sr.UnknownValueError:
        print("音声を認識できませんでした")
        return None
    except sr.RequestError as e:
        print(f"Google Web Speech API エラー: {e}")
        return None

def open_file_dialog(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.mp4")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(tk.END, file_path)

def convert_and_display(entry_widget, output_text_widget):
    audio_file_path = entry_widget.get()

    # 拡張子が.mp4の場合、一時的なWAVファイルに変換
    if audio_file_path.lower().endswith(".mp4"):
        temp_wav_file_path = os.path.join(os.path.dirname(__file__), "temp.wav")
        convert_to_wav(audio_file_path, temp_wav_file_path)
        audio_file_path = temp_wav_file_path

    result = recognize_audio(audio_file_path)
    
    if result:
        output_text_widget.delete(1.0, tk.END)
        output_text_widget.insert(tk.END, result)

    # 一時的なWAVファイルがあれば削除
    if audio_file_path.lower().endswith(".wav") and os.path.exists(audio_file_path):
        os.remove(audio_file_path)

# GUIアプリケーションの作成
app = tk.Tk()
app.title("音声認識アプリ")

# ファイル選択ボタン
file_select_button = tk.Button(app, text="ファイル選択", command=lambda: open_file_dialog(entry))
file_select_button.pack(pady=10)

# 入力ファイルパスのエントリー
label = tk.Label(app, text="音声ファイルパス:")
label.pack(pady=5)

entry = tk.Entry(app, width=40)
entry.pack(pady=5)

# 変換ボタン
convert_button = tk.Button(app, text="変換", command=lambda: convert_and_display(entry, output_text))
convert_button.pack(pady=10)

# 出力テキストウィジェット
output_text = Text(app, height=10, width=50, wrap=tk.WORD)
output_text.pack(pady=10)

# スクロールバー
scrollbar = Scrollbar(app, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

# アプリケーションの実行
app.mainloop()
