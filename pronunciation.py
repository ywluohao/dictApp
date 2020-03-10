import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
import os
from datetime import datetime


def verify_number():
    while True:
        try:
            v = int(input().strip())
        except:
            print("This is not an integer, please enter again: ")
            continue
        else:
            return v
            break


# ask for input:
print("Please enter the directory of the txt file: ")
txt_file_name = input().strip()
while not os.path.isfile(txt_file_name):
    print("This is not a valid file name, please enter again: ")
    txt_file_name = input().strip()

print("How do you want to proceed?")
print("Write 1 if by multiple of the length of word")
print("Write 2 if by a fixed length")
choice = input().strip()
while not choice in ['1', '2']:
    print("Please enter 1 or 2 only: ")
    choice = input().strip()
if choice == '1':
    print("Enter the multiple: ")
    mul = verify_number()
elif choice == '1':
    print("Enter the fixed length: ")
    sec = verify_number()

print("Please enter the directory, where the file will be saved: ")
save_dir = input().strip()
while not os.path.isdir(save_dir):
    print("This is not a valid file name, please enter again: ")
    save_dir = input().strip()

# main program
cur_time = datetime.now().strftime("%m_%d_%H_%M_%S")
os.mkdir(save_dir + '/NewWord_' + cur_time)
os.chdir(save_dir + '/NewWord_' + cur_time)

with open(txt_file_name, 'r') as t:
    txt = t.readlines()

word_list = [t[:-1] for t in txt if t[-1] == '\n']

concat_mp3 = AudioSegment.empty()
wrong_list = []

for i, word in enumerate(word_list, start=1):
    web = 'https://www.dictionary.com/browse/' + word
    page = requests.get(web)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup2 = soup.find(class_="audio-wrapper css-48y3p0 e1rg2mtf7")
    if not soup2:
        wrong_list.append(word)
        continue
    url = list(list(soup2.children)[1].children)[1].attrs['src']
    file_name = str(i) + '_' + word + '.mp3'

    r = requests.get(url)
    with open(file_name, 'wb') as fn:
        fn.write(r.content)

    mp3 = AudioSegment.from_mp3(file_name)

    silence = mul * mp3.duration_seconds if choice == '1' else sec

    concat_mp3 += mp3
    concat_mp3 += AudioSegment.silent(duration=1000 * silence)

concat_mp3.export("_concat.mp3", format="mp3")

if not wrong_list:
    final = 'Success!'
else:
    final = str(len(wrong_list)) + ' words are not found: '
    final += ', '.join(wrong_list)
print(final)
