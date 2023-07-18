# Voice2Calendar

Voice2Calendar is a Python-based solution designed to address a specific personal need. This program allows users to transform voice messages into a comprehensive to-do list and then have a calendar file sent to them via email. Here are some features:

- **Voice Message Conversion**: Given the audio message from iMessage, the script converts the audio file from .caf to mp3 format using ffmpeg library.

- **Speech to Text**: Given the audio file, Whisper model performs speech-to-text to generate a transcript of the given audio file.

- **Making a to-do list**: Given the transcript, the text-davinci-003 model generates a to-do list out of it.

- **Calendar Integration**: Given the to-do list, the script converted it into a calendar file in the standard .ics format using ics library.

- **Emailing the Calendar File**: Given the ics file, the script sends an email including .ics file as attachment using EmailMessage library.

## How It Works

1. Clone the repository: `git clone https://github.com/katayoonk/Voice2Calendar`
2. Copy the voice message from iMessage to the same folder. 
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the Python script: `python voice2calendar.py`
6. The script converts the audio file format to ensure compatibility and ease of processing.
7. The voice message is transcribed into text using Whisper model.
8. Enter your openAI API key, when prompted.
9. The OpenAI api changes uses the transcript to generates a structured to-do list.
10. A calendar file in .ics format is automatically created based on the to-do list.
11. Enter your preferred email address and its password.
12. The calendar file is attached to an email and sent to the specified email address for seamless integration into popular calendar applications.
13. Open the email, download the calendar file, and import it into your preferred calendar application.

## Contributing

Contributions to Voice2Calendar are welcome! If you have any ideas, suggestions, or bug reports, please feel free to open an issue or submit a pull request. Let's collaborate to enhance the functionality and usability of this project.
