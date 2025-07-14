import random
from pydub import AudioSegment
from pydub.playback import play
from jamo import h2j, j2hcj

char_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', ' ']

char_sounds = {}
char_sounds_high = {}

for idx, item in enumerate(char_list):
    str_idx = str(idx + 1).zfill(2)
    char_sounds[item] = AudioSegment.from_mp3(f'./sources/{str_idx}.padata')
    char_sounds_high[item] = AudioSegment.from_mp3(f'./sources/high/{str_idx}.padata')

while True:
    source = input('원본 문자열 입력: ')

    if source == "종료":
        break

    result_sound = None
    result_sound_high = None
    print('생성중...')
    for ch in source:
        jamo_ch = j2hcj(h2j(ch))
        if jamo_ch[0] not in char_list:
            print(f'지원되지 않는 문자를 건너뛰었습니다: {jamo_ch}')
        else:
            char_sound = char_sounds[jamo_ch[0]]
            char_sound_high = char_sounds_high[jamo_ch[0]]

            octaves = 2 * random.uniform(0.96, 1.15)
            new_sample_rate = int(char_sound.frame_rate * (2.0 ** octaves))

            pitch_char_sound = char_sound._spawn(char_sound.raw_data, overrides={'frame_rate': new_sample_rate})
            result_sound = pitch_char_sound if result_sound is None else result_sound + pitch_char_sound

            pitch_char_sound_high = char_sound_high._spawn(char_sound_high.raw_data,
                                                           overrides={'frame_rate': new_sample_rate})
            result_sound_high = pitch_char_sound_high if result_sound_high is None else result_sound_high + pitch_char_sound_high

    # Add silence to the beginning and end to prevent cutting off
    silence = AudioSegment.silent(duration=200) # 200ms of silence

    print("재생중: " + source + "(일반)")
    if result_sound:
        result_sound_padded = silence + result_sound + silence
        play(result_sound_padded)
        output_filename_normal = f"output_normal_{source}.wav"
        result_sound_padded.export(output_filename_normal, format="wav")
        print(f"일반 음성 저장됨: {output_filename_normal}")

    print("재생중: " + source + "(고음)")
    if result_sound_high:
        result_sound_high_padded = silence + result_sound_high + silence
        play(result_sound_high_padded)
        output_filename_high = f"output_high_{source}.wav"
        result_sound_high_padded.export(output_filename_high, format="wav")
        print(f"고음 음성 저장됨: {output_filename_high}")

print('종료되었습니다.')
