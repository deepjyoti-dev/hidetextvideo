# -*- coding: utf-8 -*-
"""
Optimized Secure Video Steganography GUI
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes, hmac
import hashlib
import os

# ----------------- Helper Functions -----------------
def text_to_bin(text_bytes):
    return ''.join(format(b, '08b') for b in text_bytes)

def bin_to_bytes(bin_str):
    chars = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
    return bytes([int(c, 2) for c in chars])

def int_to_bin32(n):
    return format(n, '032b')

# ----------------- Encryption / HMAC -----------------
def derive_keys(password):
    key = hashlib.sha256(password.encode()).digest()
    return key[:16], key[16:]

def encrypt_text(text, password):
    aes_key, hmac_key = derive_keys(password)
    padder = padding.PKCS7(128).padder()
    padded_text = padder.update(text.encode()) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    hmac_digest = h.finalize()
    return iv + ciphertext + hmac_digest

def decrypt_text(encrypted_bytes, password):
    aes_key, hmac_key = derive_keys(password)
    iv = encrypted_bytes[:16]
    hmac_digest = encrypted_bytes[-32:]
    ciphertext = encrypted_bytes[16:-32]
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    h.verify(hmac_digest)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded_text) + unpadder.finalize()).decode()

# ----------------- Optimized Hide / Extract -----------------
def hide_text_in_video(cap, out, full_bin):
    index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = frame.astype(np.uint8)

        if index < len(full_bin):
            # Only hide text in top-left 100x100 pixels
            rows, cols, _ = frame.shape
            max_row = min(100, rows)
            max_col = min(100, cols)
            for i in range(max_row):
                for j in range(max_col):
                    for k in range(3):
                        if index < len(full_bin):
                            frame[i, j, k] = np.uint8((int(frame[i, j, k]) & ~1) | int(full_bin[index]))
                            index += 1

        out.write(frame)
    return index

def extract_text_from_video(cap, text_length):
    index = 0
    text_bin = ''
    while True:
        ret, frame = cap.read()
        if not ret or index >= text_length * 8:
            break
        frame = frame.astype(np.uint8)
        rows, cols, _ = frame.shape
        max_row = min(100, rows)
        max_col = min(100, cols)
        for i in range(max_row):
            for j in range(max_col):
                for k in range(3):
                    if index < text_length * 8:
                        text_bin += str(frame[i, j, k] & 1)
                        index += 1
    return text_bin

# ----------------- GUI Functions -----------------
def hide_text():
    video_path = filedialog.askopenfilename(title="Select Video")
    if not video_path:
        return
    text_to_hide = simpledialog.askstring("Input", "Enter text to hide:")
    if not text_to_hide:
        return
    password = simpledialog.askstring("Password", "Enter password for encryption:")
    if not password:
        return

    folder = os.path.dirname(video_path)
    input_ext = os.path.splitext(video_path)[1].lower()
    default_name = "stego_video"
    file_name = simpledialog.askstring("Save As", "Enter file name for stego video:", initialvalue=default_name)
    if not file_name:
        return
    output_path = os.path.join(folder, file_name + input_ext)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if input_ext in ['.mp4', '.m4v']:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif input_ext in ['.avi']:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    elif input_ext in ['.mov']:
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        messagebox.showerror("Error", "Failed to initialize VideoWriter. Check codec and file path.")
        cap.release()
        return

    encrypted_bytes = encrypt_text(text_to_hide, password)
    text_bin = text_to_bin(encrypted_bytes)
    length_bin = int_to_bin32(len(encrypted_bytes))
    full_bin = length_bin + text_bin

    hide_text_in_video(cap, out, full_bin)

    cap.release()
    out.release()
    messagebox.showinfo("Success", f"Text encrypted and hidden in video!\nSaved as {output_path}")

def extract_text():
    video_path = filedialog.askopenfilename(title="Select Stego Video")
    if not video_path:
        return
    password = simpledialog.askstring("Password", "Enter password for decryption:")
    if not password:
        return

    cap = cv2.VideoCapture(video_path)
    # First, extract first 32 bits = length of encrypted text
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Could not read video!")
        return
    frame = frame.astype(np.uint8)
    text_length_bin = ''
    rows, cols, _ = frame.shape
    max_row = min(100, rows)
    max_col = min(100, cols)
    index = 0
    for i in range(max_row):
        for j in range(max_col):
            for k in range(3):
                if index < 32:
                    text_length_bin += str(frame[i, j, k] & 1)
                    index += 1
    text_length = int(text_length_bin, 2)

    # Extract encrypted text
    encrypted_bin = extract_text_from_video(cap, text_length)
    cap.release()
    encrypted_bytes = bin_to_bytes(encrypted_bin)
    try:
        hidden_text = decrypt_text(encrypted_bytes, password)
        messagebox.showinfo("Hidden Text", hidden_text)
    except Exception:
        messagebox.showerror("Error", "Incorrect password, HMAC failed, or video corrupted!")

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Optimized Video Steganography")
root.geometry("350x180")

tk.Button(root, text="Hide Text in Video", command=hide_text, width=30, height=2).pack(pady=10)
tk.Button(root, text="Extract Text from Video", command=extract_text, width=30, height=2).pack(pady=10)

root.mainloop()
