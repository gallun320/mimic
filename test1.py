import cv2

pic = cv2.imread('oleg.jpg', 0)
face_c = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

faces = face_c.detectMultiScale(pic)

print faces[0]

def crop(img):
  face_c = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  faces = face_c.detectMultiScale(img, 1.3, 2)
  return img[faces[0][1]: faces[0][1] + faces[0][3], faces[0][0]: faces[0][0] + faces[0][2]]

for (x, y, w, h) in faces:
  cv2.rectangle(pic, (x, y), (x + w, y + h), (0, 255, 0), 6)

cv2.imshow('frame', pic)
cv2.imshow('crop', crop(pic))
cv2.waitKey(0)
cv2.destroyAllWindows()