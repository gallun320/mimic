import sys
import os
import dlib
import glob
from skimage import io

predictor_path = "/Users/kazan12396/dlib/examples/build/shape_predictor_68_face_landmarks.dat"
faces_folder_path = "./faces"
#bamaFile = open("points.txt", "w")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

k = 0

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    
    named = str(k) + '.txt'
    open(named, 'a').close()
    bamaFile = open(named, 'w')
    img = io.imread(f)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
      shape = predictor(img, d)
      
      for el in shape.parts():
        print el
        bamaFile.write(str(el.x) + " " + str(el.y) + " ")
    bamaFile.close()    
    k = k + 1  
    dlib.hit_enter_to_continue()