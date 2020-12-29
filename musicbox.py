from gpiozero import Button
from subprocess import check_call
import vlc
import glob
import re

# static stuff
media_player = None
input_dir = '/home/pi/Music/LeSoldatRose'


def main_loop():
    from signal import pause
    pause()
    pass


def shutdown():
    play_single_file("./termine.mp3")
    check_call(['sudo', 'poweroff'])


def _next():
    media_player.next()

def _pause():
    media_player.pause()

def _backward():
    media_player.previous()



def parse_directory(input_dir: str):
    """ Parse a directory and return file content"""
    print(f"Parsing {input_dir}")
    files = glob.glob(f"{input_dir}/*mp3")
    file_list = sorted(files, key=lambda x: float(re.findall("(\d+)", x)[0]))

def play_single_file(input_file:str):
    player = vlc.Instance()
    media_list = player.media_list_new()


    pn = player.media_new(input_file)


    media_list.add_media(pn)
    media_player.set_media_list(media_list)


def create_playlist(input_dir: str):
    """ parse a directory and create playlist"""
    file_list = parse_directory(input_dir)
    player = vlc.Instance()
    media_list = player.media_list_new()
    for f in file_list:
        print(f"Adding {f} to playlist")
        pn = player.media_new(f)
        media_list.add_media(pn)
    media_player.set_media_list(media_list)
    media_player.play_item_at_index(0)




def main():
    # player = vlc.MediaPlayer('termine.mp3')
    print("create media player")
    media_player = vlc.MediaListPlayer()
    print("create playlist")
    create_playlist(input_dir)
    button_gauche = Button(4)
    button_droit = Button(3)
    button_milieu = Button(2, hold_time=3)


    button_gauche.when_pressed = _backward
    button_droit.when_pressed = _next

    button_milieu.when_pressed = _pause
    button_milieu.when_held = shutdown


    media_player.play_item_at_index(0)


    main_loop()


if __name__ == "__main__":
    # execute only if run as a script
    main()
