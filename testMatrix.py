import sys
import os
import dlib
import glob
from skimage import io
import PIL
from PIL import Image

predictor_path = "/Users/kazan12396/dlib/examples/build/shape_predictor_68_face_landmarks.dat"
faces_folder_path = ""
bamaFile = open("points.txt", "w")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


for f in glob.glob(os.path.join(faces_folder_path, "donald_trump.jpg")):
    img = io.imread(f)
    
    dets = detector(img, 1)
    for k, d in enumerate(dets):
      shape = predictor(img, d)
      
      for el in shape.parts():
        print el
        bamaFile.write(str(el.x) + " " + str(el.y) + "\n")
      
    dlib.hit_enter_to_continue()