import pyaudio
import wave
import whisper
import json
import time
import openai 
from datetime import datetime
import os

model=whisper.load_model("base")
open_ai_key = os.getenv("open_ai_key")

def get_response_from_chat_gpt(prompt):
    
    start_time = datetime.now()
    # import openai

    # Set your OpenAI API key
    openai.api_key_path = open_ai_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = [
            {"role":"user", "content":prompt},
            {"role":"system","content":"You are chatting with a 7 year old kid. Do not use complex words, and simplify sentences. Keep in mind that you are serving as a companion and a personal tutor for the kid."}
        ]
    )
    end_time = datetime.now()
    
    print("============================================================")
    
    # Print the generated text
    print(response['choices'][0]['message']['content'])
    print('\n')
    print("Time taken for CHAT GPT Response",end_time-start_time)
# get_response_from_chat_gpt('What is the difference between apples and oranges')

def record_audio(output_file, duration=5, chunk_size=1024, sample_format=pyaudio.paInt16, channels=1, sample_rate=44100):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=sample_rate,
                        frames_per_buffer=chunk_size,
                        input=True)
    
    print("Recording...")
    frames = []
    
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
        
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    start_time = datetime.now()
    # Save the recorded audio to a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(sample_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        print("File has been saved")
    
    result=model.transcribe("output.wav")
    end_time = datetime.now()
    print("=========================================")
    voice_input = result['text']
    print(voice_input)
    print('\n')
    print("Time taken for converting speech to text",end_time-start_time)
    

    get_response_from_chat_gpt(voice_input)
    
# Example usage:
record_audio("output.wav", duration=15)

#shashin