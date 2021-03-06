import cv2 as cv
import dlib as dl
import face_recognition
import os
import pickle

from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np

face_detector_model = dl.get_frontal_face_detector()
classifier = load_model("Emotion_Detection.h5")
class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprised']


def read_img(path):
    img = cv.imread(path)
    (h, w) = img.shape[:2]
    width = 500
    ratio = width / float(w)
    height = int(h * ratio)
    img = cv.resize(img, (width, height))
    return img


def encodings_of_image_database(known_images_db):
    try:
        encodings_file = open("encodings_pickle.txt", "rb")
    except Exception:
        return "error"
    try:
        known_encodings_file, flag = pickle.load(encodings_file), 1
    except Exception:
        known_encodings_file, flag = {}, 0
    encodings_file.close()

    known_encodings = []
    images = os.listdir(known_images_db)
    for file in images:
        print("Working.....")
        print(file + "\n")
        img = read_img(known_images_db + file)
        try:
            temp_res = known_encodings_file.get(file, "error")
            if flag and len(temp_res) == 128:
                encode = known_encodings_file[file]
            else:
                encode = face_recognition.face_encodings(img)[0]
                known_encodings_file[file] = encode
            known_encodings.append(encode)
        except Exception:
            os.remove(f"{known_images_db}{file}")
            print(f"{known_images_db}{file} does not have a face.")

    encodings_file = open("encodings_pickle.txt", "wb")
    pickle.dump(known_encodings_file, encodings_file)
    encodings_file.close()
    return known_encodings


def encodings_of_sketch(sketch):
    img = read_img(f"{sketch}")
    try:
        sketch_encode = face_recognition.face_encodings(img)[0]
    except Exception:
        return "error"
    else:
        return sketch_encode


def image_matching(known_encoding, sketch_encode, known_images_db):
    image_list = os.listdir(known_images_db)
    res = face_recognition.compare_faces(known_encoding, sketch_encode)
    count = 0
    for i in range(len(res)):
        if res[i]:
            count += 1
            img = read_img(known_images_db + image_list[i])
            cv.imshow(f"Matched Image {count} - {image_list[i]}", img)
    if count == 0:
        return "no_match"
    cv.waitKey(0)


def image_sketch_recognizer(sketch):
    database = "image_database/"
    sketch_encode = encodings_of_sketch(sketch)
    if sketch_encode == "error":
        return "no_match"
    known_encodings = encodings_of_image_database(database)
    if known_encodings == "error":
        return "no_pickle"
    return image_matching(known_encodings, sketch_encode, database)


def video_sketch_recognizer(sketch, vid, location):
    sketch = read_img(sketch)
    sketch_encode = face_recognition.face_encodings(sketch)
    if not sketch_encode:
        cv.destroyAllWindows()
        return "no_match"

    frame_count = 0
    cam = cv.VideoCapture(vid)
    while True:
        success, image = cam.read()
        if not success:
            cv.destroyAllWindows()
            return frame_count
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        face_loc = face_recognition.face_locations(img)
        encode = []
        try:
            encode = face_recognition.face_encodings(img, face_loc)
        except Exception:
            print("No Faces")

        for code, loc in zip(encode, face_loc):
            matches = face_recognition.compare_faces(sketch_encode, code)
            if matches[0]:
                y1, x2, y2, x1 = loc
                cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv.putText(image, "Match", (x1+10, y1-10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                frame_count += 1
                cv.imwrite(f"{location}/Match-{frame_count}.jpeg", image)

        cv.imshow("Performing Recognition - Press 'q' to stop", image)

        if cv.waitKey(10) == ord('q'):
            cv.destroyAllWindows()
            break


def live_sketch_recognizer(sketch, cam_code):
    sketch = read_img(sketch)
    sketch_encode = face_recognition.face_encodings(sketch)

    cam = cv.VideoCapture(cam_code)
    while True:
        success, image = cam.read()
        if sketch_encode:
            img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(img)
            encode = []
            try:
                encode = face_recognition.face_encodings(img, face_loc)
            except Exception:
                print("No faces")

            for code, loc in zip(encode, face_loc):
                matches = face_recognition.compare_faces(sketch_encode, code)
                if matches[0]:
                    y1, x2, y2, x1 = loc
                    cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv.putText(image, "Match", (x1+10, y1-10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv.imshow("LIVE RECOGNITION - Press 'q' to exit", image)
        if cv.waitKey(10) == ord('q'):
            cv.destroyAllWindows()
            break


def emotion_recognizer(image, left, top, right, bottom):
    try:
        dimensions = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
        for dim in dimensions:
            if dimensions[dim] < 0:
                dimensions[dim] = 5
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        face = image[dimensions['top']:dimensions['bottom'], dimensions['left']:dimensions['right']]
        face = cv.resize(face, (48, 48), interpolation=cv.INTER_AREA)
        if np.sum([face]):
            face = face.astype('float') / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis=0)
        prediction = classifier.predict(face)[0]
        result = class_labels[prediction.argmax()]
        print(result)
    except Exception:
        return "error"
    else:
        return result


def image_emotion_recognizer(image):
    if not image:
        return
    image = read_img(image)
    detected_faces = face_detector_model(image, 1)
    for face in detected_faces:
        top = face.top()
        left = face.left()
        bottom = face.bottom()
        right = face.right()
        result = emotion_recognizer(image, left, top, right, bottom)
        if result != "error":
            cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
            cv.putText(image, result, (left + 5, top - 5), cv.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        else:
            cv.putText(image, "ERROR", (25, 25), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            print(result)
    cv.imshow("EMOTION RECOGNITION", image)
    cv.waitKey(0)


def live_emotion_recognizer():
    cam = cv.VideoCapture(0)
    while True:
        success, frame = cam.read()
        detected_faces = face_detector_model(frame, 1)
        for face in detected_faces:
            top = face.top()
            left = face.left()
            bottom = face.bottom()
            right = face.right()
            result = emotion_recognizer(frame, left, top, right, bottom)
            if result != "error":
                cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv.putText(frame, result, (left + 5, top - 5), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv.putText(frame, "ERROR", (25, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print(result)
        cv.imshow("LIVE EMOTION RECOGNITION - Press 'q' to exit", frame)
        if cv.waitKey(10) == ord('q'):
            cv.destroyAllWindows()
            break
