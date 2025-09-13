import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import style  # Import styling module

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Tkinter app
root = tk.Tk()
root.title("🎙️ Voice to Text Chat")
root.geometry("700x500")
root.minsize(500, 400)
root.configure(bg=style.BG_COLOR)

# Grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Header
header = tk.Label(root, text="Voice to Text Chat", font=style.HEADER_FONT,
                  bg=style.HEADER_BG, fg=style.TEXT_COLOR)
header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

# Chat area
chat_frame = tk.Frame(root, bg=style.BG_COLOR)
chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
chat_frame.grid_rowconfigure(0, weight=1)
chat_frame.grid_columnconfigure(0, weight=1)

chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=style.CHAT_FONT,
                                      bg=style.CHAT_BG, fg=style.TEXT_COLOR, relief=tk.FLAT)
chat_area.grid(row=0, column=0, sticky="nsew")
chat_area.configure(state='disabled')

# Status bar
status_var = tk.StringVar()
status_var.set(f"{style.EMOJI_MIC} Ready to listen...")

status_bar = tk.Label(root, textvariable=status_var, font=style.STATUS_FONT,
                      bg=style.STATUS_BG, fg=style.TEXT_COLOR, anchor="w")
status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))

def insert_text(role, text, color=None):
    chat_area.configure(state='normal')
    tag = f"{role}_tag"
    chat_area.insert(tk.END, f"{role}: {text}\n", tag)
    chat_area.tag_config(tag, foreground=color or style.TEXT_COLOR)
    chat_area.configure(state='disabled')
    chat_area.yview(tk.END)

def listen_and_recognize():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        insert_text("System", "Listening... 🎤", style.SYSTEM_COLOR)
        status_var.set(f"{style.EMOJI_LISTENING} Listening... Speak now!")

        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                insert_text("You", text, style.USER_COLOR)
                status_var.set(f"{style.EMOJI_SUCCESS} Recognized. Listening again...")

            except sr.UnknownValueError:
                insert_text("System", f"{style.EMOJI_FAIL} Sorry, I didn’t catch that.", style.SYSTEM_COLOR)
                status_var.set(f"{style.EMOJI_ERROR} Didn't catch that. Try again.")
            except sr.RequestError as e:
                insert_text("System", f"{style.EMOJI_ERROR} API error: {e}", style.SYSTEM_COLOR)
                status_var.set("🚫 API error. Stopping recognition.")
                break

# Run speech recognition in a separate thread
threading.Thread(target=listen_and_recognize, daemon=True).start()

root.mainloop()
