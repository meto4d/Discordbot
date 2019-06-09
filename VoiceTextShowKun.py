#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
import base64 # Base64

apikey = "YOUR KEY"

class VTWA:
    apiurl = "https://api.voicetext.jp/v1/tts"
    list_fmat = ["mp3", "wav", "ogg"]
    list_speaker = ["show", "haruka", "hikari", "takeru", "santa", "bear"]
    list_emotion = ["", "happiness", "anger", "sadness"]

    def __init__(self, key):
        self.key = key
        self.text = ""
        self.fmat = VTWA.list_fmat[0]
        self.speaker = VTWA.list_speaker[0]
        self.emotion = VTWA.list_emotion[0]
        self.emotionLv = 2
        self.pitchLv = 2
        self.speedLv = 2
        self.volumeLv = 2

    def __SetText(self, text):
        if len(text) > 200:
            raise ValueError("Over 200 letters! Please less than 200 letters.")
        else:
            self.text = urllib.parse.quote(text, encoding='utf-8')

    def __SetFmat(self, fmat="wav"):
        if fmat in VTWA.list_fmat:
            self.fmat = fmat
        else:
            raise ValueError("Not include Spealer List")

    def __SetSpeaker(self, speaker="show"):
        if speaker in VTWA.list_speaker:
            self.speaker = speaker
        else:
            raise ValueError("Not include Speaker List")

    def __SetEmotion(self, emotion=""):
        if emotion in VTWA.list_emotion:
            self.emotion = emotion
        else:
            raise ValueError("Not include Emotion List")

    def __SetEmotionLv(self, level=2):
        if level > 0 and level < 5:
            self.emotionLv = level
        else:
            raise ValueError("out of range Emotion level")
        
    def __SetPitchLv(self, level=100):
        if level > 49 and level < 201:
            self.pitchLv = level
        else:
            raise ValueError("out of range pitch level")

    def __SetSpeedLv(self, level=100):
        if level > 49 and level < 201:
            self.speedLv = level
        else:
            raise ValueError("out of range speed level")

    def __SetVolumeLv(self, level=100):
        if level > 49 and level < 201:
            self.volumeLv = level
        else:
            raise ValueError("out of range volume level")
        
    def __params(self, tx, pm, first=False):
        text = ("?" if first else "&") + tx + "=" + str(pm)
        if tx != "text":
            if pm == 2 or pm == 100 or pm == "":
                text = ""
        return text
    
    def __CreateParams(self):
        prm = self.__params("text", self.text, first=True)
        prm += self.__params("format", self.fmat)
        prm += self.__params("speaker", self.speaker)
        if self.speaker != "show":
            prm += self.__params("emotion", self.emotion)
            prm += self.__params("emotion_level", self.emotionLv)
        prm += self.__params("pitch", self.pitchLv)
        prm += self.__params("speed", self.speedLv)
        prm += self.__params("volume", self.volumeLv)

        return prm

    def SetVTWA(self, text, fmat="wav", speaker="show", emotion="", emotion_level=2, pitch_level=100, speed_level=100, volume_level=100):
        try:
            self.__SetText(text)
            self.__SetFmat(fmat)
            self.__SetSpeaker(speaker)
            self.__SetEmotion(emotion)
            self.__SetEmotionLv(emotion_level)
            self.__SetPitchLv(pitch_level)
            self.__SetSpeedLv(speed_level)
            self.__SetVolumeLv(volume_level)
        except ValueError as e:
            print(e)

    def getfile(self, name, dirname="./"):
        url = VTWA.apiurl + self.__CreateParams()
        try:
            res = BasicReq(self.key, "", url)
            self.__saveEnc(res, name, dirname)
        except ValueError as e:
            print(e)

    def __saveEnc(self, res, name, dirname="./"):
        if dirname[-1:] != "/":
            dirname += "/"
        fname = dirname + name + "." + self.fmat
        with open(fname, mode="wb") as f:
            f.write(res)


###################################
# Basic認証
# ref: https://www.yoheim.net/blog.php?q=20181003
def BasicReq(user, pas, url):
    bas = base64.b64encode((user +':'+ pas).encode('utf-8'))
    headers = {"Authorization": "Basic " + bas.decode('utf-8')}
    try:
        req = urllib.request.Request(url, headers=headers, method="POST")
        return urllib.request.urlopen(req).read()
    except urllib.request.HTTPError as e:
        raise ValueError("HTTP Error "+e.code+ " :"+e.read())


if __name__ == "__main__":
    vtwa = VTWA(apikey)
    vtwa.SetVTWA("テスト", fmat="mp3")
    vtwa.getfile("test")
