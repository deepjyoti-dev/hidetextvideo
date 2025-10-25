# hidetextvideo
# Optimized Secure Video Steganography GUI

A Python-based GUI application to securely hide text inside videos using AES encryption and HMAC verification. This project demonstrates video steganography optimized for speed and security, hiding data in the top-left 100x100 pixel area of video frames.

---

## Features

- **Secure Encryption:** Uses AES-128 in CBC mode to encrypt the text with a password.
- **Data Integrity:** HMAC-SHA256 ensures the hidden text is not tampered with.
- **Video Support:** Works with `.mp4`, `.avi`, `.mov`, and other common video formats.
- **Optimized Hiding:** Hides encrypted text only in the top-left 100x100 pixels to reduce processing time.
- **GUI Interface:** Simple and user-friendly interface using Tkinter.

---

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/optimized-video-steganography.git
    cd optimized-video-steganography
    ```

2. Install dependencies:
    ```bash
    pip install opencv-python cryptography numpy
    ```

3. Run the application:
    ```bash
    python stego_gui.py
    ```

---

## Usage

### Hide Text in Video
1. Click **"Hide Text in Video"**.
2. Select the video file.
3. Enter the text you want to hide.
4. Set a password for encryption.
5. Specify a name for the stego video.
6. The application will create a video with the hidden, encrypted text.

### Extract Text from Video
1. Click **"Extract Text from Video"**.
2. Select the stego video file.
3. Enter the correct password.
4. If successful, the hidden text will be displayed.

---

## Technical Details

- **Encryption:** AES-128 CBC with PKCS7 padding.
- **HMAC:** SHA-256 to verify integrity.
- **Steganography:** LSB (Least Significant Bit) method applied to RGB values.
- **Optimization:** Only hides/extracts text in the top-left 100x100 pixels to reduce processing time and memory usage.

---

## Notes

- Ensure the video is not too short; large text may not fit in smaller videos.
- If extraction fails, check:
  - Correct password was used.
  - Video is not corrupted.
  - Video has enough capacity to store hidden text.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Screenshots

*(You can add screenshots of your GUI here)*

---

## Acknowledgments

- OpenCV for video processing.
- Cryptography library for secure encryption.
- Tkinter for GUI.

