import requests
import json
import tempfile
import os
import wave
import glob
import ast

def get_audio(text, speakerID):
    # audio_query (音声合成用のクエリを作成するAPI)
    res1 = requests.post(VICEVOX_API_URL + '/audio_query',
                        params={'text': text, 'speaker': speakerID})
    # synthesis (音声合成するAPI)
    res2 = requests.post(VICEVOX_API_URL + '/synthesis',
                        params={'speaker': speakerID},
                        data=json.dumps(res1.json()))
    return res2

def save_audio(conversation, audio_file_path):
    for i, line in enumerate(conversation):
        try:
            if line:
                speaker, text = next(iter(line.items()))
                if speaker == "Speaker 1":
                    speakerID = SPEACKER1_CHARACTOR_ID
                elif speaker == "Speaker 2":
                    speakerID = SPEACKER2_CHARACTOR_ID
                else:
                    continue #想定外のspeakerはスキップ

                res = get_audio(text, speakerID)
                with open(f"{audio_file_path}/{i:03}.wav", mode='wb') as f:
                    f.write(res.content)
            else:
                print(f"Error processing line {i+1}: Empty dictionary")
        except (KeyError, ValueError, StopIteration) as e:
            print(f"Error processing line {i+1}: {e}")
            continue #エラー発生時は次の行へ


def combine_wav_files(output_file, input_folder):
  # フォルダ内のWAVファイルを順番に取得（例：001.wav, 002.wav ）
  wav_files = sorted(glob.glob(os.path.join(input_folder, "*.wav")))
  
  # 出力ファイルの準備
  if wav_files:
    with wave.open(wav_files[0], 'rb') as first_wav:
        params = first_wav.getparams()
        with wave.open(output_file, 'wb') as output_wav:
            output_wav.setparams(params)
            for wav_file in wav_files:
                with wave.open(wav_file, 'rb') as wf:
                    output_wav.writeframes(wf.readframes(wf.getnframes()))
  else:
    print("No WAV files found in the input folder.")


VICEVOX_API_URL = "http://localhost:50021"
SPEACKER1_CHARACTOR_ID = 46
SPEACKER2_CHARACTOR_ID = 8

if __name__ == "__main__":
  # Loading
  with open('podcast_data.json', 'r') as f:
      loaded_data = json.load(f)

      #loaded_data = ast.literal_eval(loaded_data) #不要な行を削除
      print(loaded_data)

  with tempfile.TemporaryDirectory() as temp_dir:
    # print(temp_dir)
    save_audio(loaded_data, temp_dir)
    combine_wav_files(f"{temp_dir}/podcast.wav", temp_dir)
