import sys
import os
import dlib
import glob
from skimage import io
import cv2

predictor_path = "/Users/kazan12396/dlib/examples/build/shape_predictor_68_face_landmarks.dat"
faces_folder_path = ""
bamaFile = open("points.txt", "w")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def crop(img):
  face_c = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  faces = face_c.detectMultiScale(img, 1.3, 2)
  return img[faces[0][1]: faces[0][1] + faces[0][3], faces[0][0]: faces[0][0] + faces[0][2]]

k = 0
for f in glob.glob(os.path.join(faces_folder_path, "oleg.jpg")):
    img = crop(io.imread(f))
    dets = detector(img, 1)
    for k, d in enumerate(dets):
      shape = predictor(img, d)
      for el in shape.parts():
        print el
        bamaFile.write(str(el.x) + " " + str(el.y) + "\n")
        k += 1
      
    dlib.hit_enter_to_continue()
print(k)
cv2.destroyAllWindows()