import os
from pocketsphinx import LiveSpeech
import pyautogui


os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY']='/run/user/1000/gdm/Xauthority'

if __name__ == "__main__":
    speech = LiveSpeech(
        lm = False,
        kws = 'key.list',
        verbose = 'True',
        no_search = False,
        full_utt = False,
        buffer_size = 1048,
        sampling_rate = 16000,
    )
    for phrase in speech:
        keyword = str(phrase)
        # print(keyword)
        if 'up' in keyword:
            # print("fuck")
            print(keyword)
            pyautogui.press('up')
            # pyautogui.alert('up')
        elif 'right' in keyword:
            print(keyword)
            pyautogui.press('right')
            # pyautogui.alert('right')
        elif 'left' in keyword:
            print(keyword)
            pyautogui.press('left')
            # pyautogui.alert('left')
        elif 'down' in keyword:
            print(keyword)
            pyautogui.press('down')
            # pyautogui.alert('down')
