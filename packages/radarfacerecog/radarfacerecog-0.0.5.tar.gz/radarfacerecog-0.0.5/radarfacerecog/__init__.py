import cv2
import os
import face_recognition
import numpy as np
import pandas as pd


class Radarfacerecog:

    def __init__(self):
        self.path = '/usr/local/lib/python3.8/site-packages/radarfacerecog/data/'
        self.images = []
        self.classnames = []
        self.datalist = os.listdir(self.path)

        for cl in self.datalist:
            curimg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curimg)
            self.classnames.append(os.path.splitext(cl)[0])

    def find_encodigns(self):
        encodeList = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        
        return encodeList

    def predict(self, image):
        df = pd.read_csv('/usr/local/lib/python3.8/site-packages/radarfacerecog/politicos.csv')
        apelidos = df['Apelido'].astype(str).tolist()
        encodeListKnow = self.find_encodigns()
        # For local running remove comment
        #unknowface = cv2.imread(image)

        #imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        #imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        predict = face_recognition.face_locations(image)
        encode_predict = face_recognition.face_encodings(image, predict)

        for encodeFace, faceLoc in zip(encode_predict, predict):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            facedis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(facedis)

            if matches[matchIndex]:
                self.name = self.classnames[matchIndex]
                return True
            elif self.name in apelidos:
                return True
            else:
                return False
