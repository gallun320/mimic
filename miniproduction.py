import sys
import os
import dlib
import glob
from skimage import io
import cv2
import shutil

predictor_path = "/Users/kazan12396/dlib/examples/build/shape_predictor_68_face_landmarks.dat"
faces_folder_path = "./faces"
bamaFile = open("./points/neuro_in.txt", "w")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


def landmarksFunc():
  indexFile = 0
  for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
      img = io.imread(f)
      dets = detector(img, 1)
      for k, d in enumerate(dets):
        shape = predictor(img, d)
        for el in shape.parts():
          print el
          bamaFile.write(str(el.x) + " " + str(el.y) + " ")   
      indexFile = indexFile + 1
      print indexFile
      #dlib.hit_enter_to_continue()
  for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    os.remove(f)