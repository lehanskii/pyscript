import requests
import os
from bs4 import BeautifulSoup as bs
import time

url = "https://storiesig.com/stories/"

def pars_target(target):
    target_dir = 'D:\\Новая папка\\Data\\pars\\{0}'.format(target)
    for_check = "---"
    try:
        connect = requests.get(url + target, headers={"accept": "*/*",
                                                      "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"})
        soup = bs(connect.content, "html.parser")
        images = soup.find_all("img")
        videos = soup.find_all("video")
        if len(images) == 0:
            time.sleep(20)
            return
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for_count = len([f for f in os.listdir(target_dir)])
        for image in images:
            time.sleep(0.2)
            with requests.get(image['src']) as connect:
                binaryimage = connect.content
            if (check_list(target_dir, binaryimage)):
                for_count += 1
                for_check = "+++"
                with open(target_dir + "\\{0}.jpg".format(for_count), "wb") as file:
                    file.write(binaryimage)
        #    for video in videos:
        #        time.sleep(0.2)
        #        with requests.get(video['src']) as connect:
        #            binaryvideo = connect.content
        #        if (check_list(target_dir, binaryvideo)):
        #            for_count += 1
        #            for_check = "+++"
        #            with open(target_dir + "\\{0}.mp4".format(for_count), "wb") as file:
        #                for chunk in binaryvideo:
        #                    file.write(chunk)

        print_report(target, True, for_check)
    except:
        print_report(target, False)

    time.sleep(20)


def check_list(targets_path, binaryobject):
    objects = [f for f in listdir(targets_path)]
    for object in objects:
        with open(targets_path + "\\{0}".format(object), "rb") as binaryfile:
            if binaryfile.read() == binaryobject:
                return False
    return True


def targets_list(targets_path):
    list_of_target = []
    with open(targets_path) as file:
        for target in file:
            list_of_target.append(target)
    return list_of_target

def print_report(target, well, *for_check):
    if well:
        print("Target: " + target + " was successful processed with " + for_check[0])
    else:
        print("Error: " + target)


targets_list_path = "D:\\Новая папка\\Data\\pars\\persons.txt"
print("Targets processing started.")
for target in targets_list(targets_list_path):
    pars_target(target.rstrip())

print("Targets processing completed")
a = input()
