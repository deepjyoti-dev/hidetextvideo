🎥 HideTextVideo

Optimized Secure Video Steganography GUI

A Python-based GUI application to securely hide text inside videos using AES encryption and HMAC verification.
Optimized for speed and security, this project hides data in the top-left 100x100 pixel area of video frames.

✨ Features

🔒 Secure Encryption: AES-128 in CBC mode with password protection.

🛡️ Data Integrity: HMAC-SHA256 ensures hidden text is not tampered with.

🎞️ Video Support: Works with .mp4, .avi, .mov, and other common formats.

⚡ Optimized Hiding: Only top-left 100x100 pixels used to reduce processing time.

🖥️ GUI Interface: User-friendly GUI built with Tkinter.

🧩 Installation

Clone the repository:

git clone https://github.com/yourusername/optimized-video-steganography.git
cd optimized-video-steganography


Install dependencies:

pip install opencv-python cryptography numpy


Run the application:

python stego_gui.py

🛠️ Usage
Hide Text in Video

Click "Hide Text in Video"

Select a video file

Enter the text to hide

Set a password

Specify a name for the stego video

The application will generate a video with hidden, encrypted text

Extract Text from Video

Click "Extract Text from Video"

Select the stego video

Enter the password

If successful, hidden text is displayed

🧠 Technical Details

Encryption: AES-128 CBC with PKCS7 padding

HMAC: SHA-256 for integrity verification

Steganography: LSB (Least Significant Bit) applied to RGB values

Optimization: Hiding/extracting text only in top-left 100x100 pixels for faster processing

⚠️ Notes

Ensure the video is long enough; large text may not fit in short videos

Extraction may fail if:

Incorrect password

Video is corrupted

Video has insufficient capacity

🏷️ Tags

#python #tkinter #opencv #steganography #aes #hmac #videoprocessing #gui

🧑‍💻 Author

Deepjyoti Das
🔗 [LinkedIn](https://www.linkedin.com/in/deepjyotidas1)

💻 GitHub
