import os
import pytube
import ffmpeg
import whisper
from googletrans import Translator

def download_video(url):
    yt = pytube.YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    output_file = stream.download()
    return output_file

def convert_audio_to_wav(input_file):
    output_file = "audio.wav"
    ffmpeg.input(input_file).output(output_file, format='wav').run()
    return output_file

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path, verbose=True)
    return result

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def generate_smi(transcript, target_language='en'):
    smi_content = "<SAMI>\n<HEAD>\n<TITLE>Translated Subtitles</TITLE>\n</HEAD>\n<BODY>\n"
    
    for segment in transcript['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        translated_text = translate_text(text, target_language)
        
        start_time_str = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}.{int((start_time % 1) * 100):02}"
        end_time_str = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02}.{int((end_time % 1) * 100):02}"
        
        smi_content += f"<SYNC Start={int(start_time*1000)}><P Class=ENCC>\n{translated_text}\n"
        
    smi_content += "</BODY>\n</SAMI>"
    return smi_content

def save_smi_file(smi_content, file_name):
    with open(file_name, "w", encoding='euc-kr') as file:
        file.write(smi_content)

def main():
    youtube_url = "https://www.youtube.com/watch?v=your_video_id"
    target_language = "ko"  # 원하는 언어 코드 (예: 'es'는 스페인어)

    video_file = download_video(youtube_url)
    audio_file = convert_audio_to_wav(video_file)
    transcript = transcribe_audio(audio_file)
    smi_content = generate_smi(transcript, target_language)
    save_smi_file(smi_content, "output.smi")
    print("SMI file generated successfully.")

if __name__ == "__main__":
    main()
