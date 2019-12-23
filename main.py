import requests
import os
from bs4 import BeautifulSoup as bs
import time

url = "https://storiesig.com/stories/"
dir = "Enter your dir path with file targets.txt"


class StoriesParser:
    def __init__(self, target):
        self.target = target
        self.target_dir = dir.format(target)
        self.image_stories = []
        self.video_stories = []
        self.operation_success = False
        self.find_error = False

    def get_stories(self):
        try:
            connect = requests.get(url + self.target)
            soup = bs(connect.content, "html.parser")
            for image_story in soup.find_all("img"):
                self.image_stories.append(image_story['src'])
            for video_story in soup.find_all("video"):
                self.video_stories.append(video_story['src'])
        except:
            print("Error in get_stories method: " + self.target)
            self.find_error = True

    def save_stories(self):
        try:
            if (len(self.image_stories) == 0) and (len(self.video_stories) == 0):
                time.sleep(10)
                return
            number_of_stories = len([f for f in os.listdir(self.target_dir)])
            for image_story in self.image_stories:
                time.sleep(0.5)
                connect = requests.get(image_story)
                image = connect.content
                if self.duplicate_checker(image):
                    number_of_stories += 1
                    self.operation_success = True
                    with open(self.target_dir + "\\{0}.jpg".format(number_of_stories), "wb") as file:
                        file.write(image)
            for video_story in self.video_stories:
                time.sleep(0.5)
                connect = requests.get(video_story, stream=True)
                video = connect.content
                if self.duplicate_checker(video):
                    number_of_stories += 1
                    self.operation_success = True
                    with open(self.target_dir + "\\{0}.mp4".format(number_of_stories), "wb") as file:
                        for chunk in connect.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
        except:
            print("Error in save_stories method: " + self.target)
            self.find_error = True

    def duplicate_checker(self, image):
        try:
            objects = [f for f in os.listdir(self.target_dir)]
            for object in objects:
                with open(self.target_dir + "\\{0}".format(object), "rb") as binary_file:
                    if image == binary_file.read():
                        return False
            return True
        except:
            print("Error in duplicate_checker method: " + self.target)
            self.find_error = True

    def print_report(self):
        if self.find_error:
            return
        if self.operation_success:
            print("Target: " + self.target + " was successful processed with +++")
        else:
            print("Target: " + self.target + " was successful processed with ---")

    def run(self):
        self.get_stories()
        self.save_stories()
        self.print_report()


class Main:
    def __init__(self):
        self.list_for_targets = []

    def get_targets_list(self):
        with open(dir.format("targets.txt")) as file:
            for target in file:
                self.list_for_targets.append(target)

    def run(self):
        print("Targets processing started.")
        self.get_targets_list()
        for target in self.list_for_targets:
            StoriesParser(target.rstrip()).run()
            time.sleep(10)
        print("Targets processing completed")


Main().run()
