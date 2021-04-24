import face_recognition
import cv2 as cv
import os

from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
classifier = load_model("Emotion_Detection.h5")
class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']


def read_img(path):
    img = cv.imread(path)
    (h, w) = img.shape[:2]
    width = 500
    ratio = width / float(w)
    height = int(h * ratio)
    img = cv.resize(img, (width, height))
    return img


def encodings_of_image_database(known_images_db):
    known_encoding = []
    names = os.listdir(known_images_db)
    for file in names:
        print(file)
        img = read_img(f"{known_images_db}/{file}")
        encode = face_recognition.face_encodings(img)[0]
        print("Working...\n")
        known_encoding.append(encode)
    return known_encoding


def encodings_of_sketch(sketch):
    img = read_img(f"{sketch}")
    cv.imshow("Uploaded Sketch", img)
    sketch_encode = face_recognition.face_encodings(img)[0]
    return sketch_encode


def image_matching(known_encoding, sketch_encode, known_images_db):
    image_list = os.listdir(known_images_db)
    res = face_recognition.compare_faces(known_encoding, sketch_encode)
    print(image_list)
    count = 0
    for i in range(len(res)):
        if res[i]:
            count += 1
            print(f"Matched image is {image_list[i]}")
            img = read_img(f"{known_images_db}/+{image_list[i]}")
            cv.imshow(f"Matched Image {count}", img)
    if count == 0:
        print("No match found in the database")
    cv.waitKey(0)


def live_recognise(sketch, cam_code):
    sketch = read_img(f"imageCollection/{sketch}.jpeg")
    sketch_encode = face_recognition.face_encodings(sketch)
    print("\n\nREADY\n")
    cam = cv.VideoCapture(cam_code)
    while True:
        success, image = cam.read()
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        # face_68_points = face_recognition.face_landmarks(img)
        # for key in face_68_points:
        #     print(list(key.values()))

        face_loc = face_recognition.face_locations(img)
        encode = []
        try:
            encode = face_recognition.face_encodings(img, face_loc)
        except Exception:
            print("Error")

        for code, loc in zip(encode, face_loc):
            matches = face_recognition.compare_faces(sketch_encode, code)
            # print(matches)
            # faceDistance = face_recognition.face_distance(sketch_encode, code)
            # print(faceDistance)  # Lowest distance is best match
            # match = np.argmin(faceDistance)
            # name = names[match]
            # print(name)

            if matches[0]:
                y1, x2, y2, x1 = loc
                cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv.putText(image, "Match", (x1+10, y1-10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv.imshow("LIVE", image)

        if cv.waitKey(10) == ord('q'):
            break


def video_recognise(vid, sketch):
    sketch = read_img(f"imageCollection/{sketch}.jpeg")
    sketch_encode = face_recognition.face_encodings(sketch)
    print("\n\nREADY\n")
    cam = cv.VideoCapture(vid)
    while True:
        success, image = cam.read()
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        face_loc = face_recognition.face_locations(img)
        encode = []
        try:
            encode = face_recognition.face_encodings(img, face_loc)
        except Exception:
            print("Error")

        for code, loc in zip(encode, face_loc):
            matches = face_recognition.compare_faces(sketch_encode, code)

            if matches[0]:
                y1, x2, y2, x1 = loc
                cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv.putText(image, "Caught", (x1+10, y1-10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv.imwrite("location\vid.jpeg", image)
        cv.imshow("LIVE", image)

        if cv.waitKey(10) == ord('q'):
            break


def emotion_recognizer(image, x, y, w, h):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    face = image[y:y+h, x:x+w]
    face = cv.resize(face, (48, 48), interpolation=cv.INTER_AREA)

    if np.sum([face]):
        face = face.astype('float') / 255.0
        face = img_to_array(face)
        face = np.expand_dims(face, axis=0)

    prediction = classifier.predict(face)[0]
    result = class_labels[prediction.argmax()]
    print("Result")



# Call functions