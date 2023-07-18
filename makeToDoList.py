import os
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
import whisper
import subprocess
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from pyicloud import PyiCloudService
from datetime import datetime
import smtplib
import ssl
from email.message import EmailMessage
from ics import Calendar, Event

# Step 1 - Call Whisper to transcribe audio
print("Calling Whisper to transcribe audio...\n")

pydub.AudioSegment.converter = r"C:/Users/kavia/anaconda3/Library/bin/ffmpeg.exe"

# convert .caf to .mp#
# ffmpeg -i voice.caf voice.mp3
def convertCAF2MP3(input, output):
    command = []
    command.append("ffmpeg -i ")
    command.append(input)
    # command.append(" -ac 2 -f wav -map_metadata 0 - | lame -V 2 -")
    command.append(output)
    command.append(".mp3 >/dev/null 2>&1")
    return command
subprocess.check_output(['ffmpeg','-i', 'voice.caf', 'voice.mp3'], shell=True)
print('.caf file converted to .mp3')

# Input the voice
audio_file = "./voice.mp3"

# Chunk up the audio file 
sound_file = AudioSegment.from_mp3(audio_file)
audio_chunks = split_on_silence(sound_file, min_silence_len=1000, silence_thresh=-40 )
count = len(audio_chunks)
print("Audio split into " + str(count) + " audio chunks")

#Call Whisper to transcribe audio
model = whisper.load_model("base")
transcript = ""
for i, chunk in enumerate(audio_chunks):
    # If you have a long audio file, you can enable this to only run for a subset of chunks
    if i < 10 or i > count - 10:
        out_file = "chunk{0}.wav".format(i)
        print("Exporting", out_file)
        chunk.export(out_file, format="wav")
        result = model.transcribe(out_file)
        transcriptChunk = result["text"]
        print(transcriptChunk)
        
        # Append transcript in memory if you have sufficient memory
        transcript += " " + transcriptChunk
        
# make a to-do-list using gpt3
# importing openai api key

os.environ["OPENAI_API_KEY"] = input("enter your OpenAI API Key: ")

# give gpt a prompt
prompt = PromptTemplate(
    input_variables=["transcript"],
    template="Make a to-do list from {transcript} in a way that gmail recognizes it as a today's event and add the whole list to my calendar",
)

# print(f'prompt message: {prompt.format(message=transcript)}')

# generating the answer
llm = OpenAI(
          model_name="text-davinci-003", # default model
          temperature=0.9) #temperature dictates how whacky the output should be
llmchain = LLMChain(llm=llm, prompt=prompt)
todolist = llmchain.run(transcript)

#make ics file from the to-do list
c = Calendar()
e = Event()
e.name = f"{datetime.now().day}'s to-do list"
e.begin = datetime.now()
e.description = todolist
c.events.add(e)
# c.events
with open('my.ics', 'w') as my_file:
    my_file.writelines(c.serialize_iter())
    
#email the to-do list to myself
email_sender = input('enter your email address: ')
email_password = input('enter your password: ')
email_receiver = email_sender
subject = "Today's To-do List"
body = todolist
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

#adding attachment
# Open the .ics file in binary mode and read its content
with open('./my.ics', 'rb') as f:
    file_data = f.read()

em.add_attachment(file_data, maintype = 'ics', subtype = 'ics', filename = 'my.ics')

#add SSL
context = ssl.create_default_context()

#Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
    
print('\n Email sent successfully!')