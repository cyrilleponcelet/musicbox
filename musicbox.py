from gpiozero import Button
from subprocess import check_call
import vlc
import glob
import re
import time



class Player:

    # match directories and their associated files to play
    directories= {"Odyssee": ('/home/pi/Music/Odyssee',"./odyssee.m4a"),
                      "Olma": ('/home/pi/Music/Olma',"./olma.m4a"),
                      "LeSoldatRose":('/home/pi/Music/LeSoldatRose',"./SoldatRose.m4a")
                      }

    def __init__(self, first_dir="Odyssee"):
        # static stuff
        self.media_player = None
        self.current_dir = first_dir


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

    def _next_dir(self):
        keys = self.directories.keys
        current_idx = keys.index(self.current_dir)
        current_idx = current_idx+1
        if current_idx >= len(keys):
            current_idx = 0
        self.current_dir = keys[current_idx]
        self._pause()
        self.create_playlist(self.current_dir)

    def _next(self):
        self.media_player.next()

    def _pause(self):
        self.media_player.pause()

    def _backward(self):
        self.media_player.previous()



    def parse_directory(self,dir_name: str):
        """ Parse a directory and return file content"""
        input_dir = self.directory_names[dir_name.lower()][0]
        print(f"Parsing {input_dir}")
        self.play_single_file(self.directory_names[dir_name.lower()][1])

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


    def create_playlist(self,dir_name: str):
        """ parse a directory and create playlist"""
        file_list = self.parse_directory(dir_name)
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
        self.create_playlist(self.current_dir)
        button_gauche = Button(4)
        button_droit = Button(3, hold_time=1)
        button_milieu = Button(2, hold_time=1)


        button_gauche.when_pressed = self._backward
        button_droit.when_pressed = self._next
        button_droit.when_held = self._next_dir

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
