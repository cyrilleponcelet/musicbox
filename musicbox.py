from gpiozero import Button
from subprocess import check_call
import vlc
import glob
import re
import time

class Player:

    def __init__(self, input_dir='/home/pi/Music/LeSoldatRose'):
        # static stuff
        self.media_player = None
        self.input_dir = input_dir


    def main_loop(self):
        from signal import pause
        pause()
        pass

    def shutdown(self):
        print("Shutdown")
        self.play_single_file("./termine.mp3")
        time.sleep(1)
        print("Really Shutdown")
        check_call(['sudo', 'poweroff'])


    def _next(self):
        self.media_player.next()

    def _pause(self):
        self.media_player.pause()

    def _backward(self):
        self.media_player.previous()



    def parse_directory(self,input_dir: str):
        """ Parse a directory and return file content"""
        print(f"Parsing {input_dir}")
        files = glob.glob(f"{input_dir}/*mp3")
        file_list = sorted(files, key=lambda x: float(re.findall("(\d+)", x)[0]))
        return file_list


    def play_single_file(self,input_file:str):
        player = vlc.Instance()
        media_list = player.media_list_new()
        pn = player.media_new(input_file)
        media_list.add_media(pn)
        self.media_player.set_media_list(media_list)
        self.media_player.play_item_at_index(0)


    def create_playlist(self,input_dir: str):
        """ parse a directory and create playlist"""
        file_list = self.parse_directory(input_dir)
        player = vlc.Instance()
        media_list = player.media_list_new()
        for f in file_list:
            print(f"Adding {f} to playlist")
            pn = player.media_new(f)
            media_list.add_media(pn)
        self.media_player.set_media_list(media_list)
        self.media_player.play_item_at_index(0)




    def run(self):
        # player = vlc.MediaPlayer('termine.mp3')
        print("create media player")
        self.media_player = vlc.MediaListPlayer()
        print("create playlist")
        self.create_playlist(self.input_dir)
        button_gauche = Button(4)
        button_droit = Button(3)
        button_milieu = Button(2, hold_time=3)


        button_gauche.when_pressed = self._backward
        button_droit.when_pressed = self._next

        button_milieu.when_pressed =self._pause
        button_milieu.when_held = self.shutdown

        #read first song
        self.media_player.play_item_at_index(0)

        #pause and wait
        self.main_loop()


if __name__ == "__main__":
    # execute only if run as a script
    player = Player()
    player.run()
