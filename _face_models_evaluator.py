import time
import cv2 as cv
import dlib
import os
import imagehash
from PIL import Image
import face_recognition as fr
import numpy as np
import pandas as pd


def read_img(img_path):
    img = cv.imread(img_path)
    (h, w) = img.shape[:2]
    width = 500
    ratio = width / float(w)
    height = int(h * ratio)
    img = cv.resize(img, (width, height))
    return img


def preprocessing():
    dataset_path = ""  # r".\CASIA_FACE_DATASET"
    dirs = os.listdir(dataset_path)
    print(len(dirs))
    print("\n\n----------------\n\n")
    destination = r".\CASIA_FACE_DATASET"

    # CASIA face selection
    count = 0
    for sub in dirs:
        image = dataset_path + "\\" + sub + "\\001.jpg"
        count += 1
        os.system(f'copy "{image}" "{destination}\\face_{count}.jpg"')
    print("\n\n-------------\n\nDONE\n\n-------------\n\n")
    count = 10570
    for sub in dirs:
        image = dataset_path + "\\" + sub + "\\002.jpg"
        count += 1
        os.system(f'copy "{image}" "{destination}\\face_{count}.jpg"')
    print("\n\n-------------\n\nDONE\n\n-------------\n\n")
    # Renaming CASIA faces
    count = 0
    for image in os.listdir(destination):
        count += 1
        os.rename(f"{destination}\\{image}", f"{destination}\\face_{count}.jpg")
    print(count)

    # Non face image selection
    dataset_path = r"C:\Users\aryap\Downloads\natural_images"
    destination = r"C:\Users\aryap\Documents\Python Scripts\sketchRecognise\C_NATURALIMAGES_DATASET"
    natural_img_sub = os.listdir(dataset_path)
    for sub in natural_img_sub:
        images = os.listdir(dataset_path + "\\" + sub)
        for image in images:
            print(f"WORKING ON {image}")
            os.system(f'copy "{dataset_path}\\{sub}\\{image}" "{destination}\\{image}.jpg')


def load_models(model):
    if model == "hog":
        # Load HOG Model
        hog_face_model = dlib.get_frontal_face_detector()
        print("HOG loaded successfully")
        return hog_face_model

    if model == "cascade":
        # Load Cascade Model
        cascade_face_model_path = r"haarcascade_frontalface_default.xml"
        cascade_face_model = cv.CascadeClassifier(cascade_face_model_path)
        print("Cascade loaded successfully")
        return cascade_face_model

    if model == "expression":
        pass
        # expression_model = load_model("Emotion_Detection.h5")
        # return expression_model


def hog_test(dataset_path):
    # Load HOG model
    hog_face_model = load_models("hog")
    # Initialize values
    hog_detected = 0
    hog_not_detected = 0
    # Load images
    images = os.listdir(dataset_path)
    total_images = len(images)
    print("STARTING TEST\n")
    count = 0
    # error = []
    start = time.time()
    for image in images:
        count += 1
        print(f"WORKING ON IMAGE - {count}")
        img = dataset_path + "\\" + image
        img = cv.imread(img, 0)
        # Detect faces
        hog_faces = hog_face_model(img, 1)
        if hog_faces:
            hog_detected += 1
        else:
            hog_not_detected += 1
            # error.append(image)
    end = time.time()

    print("\n\n-----------------------------------\n")
    print("READINGS OF TEST".center(35))
    print("\n-----------------------------------\n\n")
    print("TEST CASES".ljust(21), f"--->   {total_images} IMAGES")
    print("TIME TAKEN".ljust(21), f"--->   {end - start} SECONDS")
    print("HOG DETECTED".ljust(21), f"--->   {hog_detected}")
    print("HOG NOT DETECTED".ljust(21), f"--->   {hog_not_detected}")
    # print(f"LIST OF SKETCHES NOT DETECTED BY HOG")
    # count = 0
    # for face in error:
    #     print(face)


def cascade_test(dataset_path):
    # Load Cascade model
    cascade_face_model = load_models("cascade")
    # Initialize values
    cascade_detected = 0
    cascade_not_detected = 0
    # Load images
    images = os.listdir(dataset_path)
    total_images = len(images)
    print("STARTING TEST\n")
    count = 0
    start = time.time()
    # error = []
    for image in images:
        count += 1
        print(f"WORKING ON IMAGE - {count}")
        img = dataset_path + "\\" + image
        img = cv.imread(img, 0)
        # Detect Faces
        cascade_faces = cascade_face_model.detectMultiScale(img, 1.1, 4)
        if len(cascade_faces):
            cascade_detected += 1
        else:
            cascade_not_detected += 1
            # error.append(image)
    end = time.time()
    print("\n\n-----------------------------------\n")
    print("READINGS OF TEST".center(35))
    print("\n-----------------------------------\n\n")
    print("TEST CASES".ljust(21), f"--->   {total_images} IMAGES")
    print("TIME TAKEN".ljust(21), f"--->   {end-start} SECONDS")
    print("CASCADE DETECTED".ljust(21), f"--->   {cascade_detected}")
    print("CASCADE NOT DETECTED".ljust(21), f"--->   {cascade_not_detected}")
    # print(f"LIST OF SKETCHES NOT DETECTED BY CASCADE")
    # for face in error:
    #     print(face)


def unit_test(img_name):
    # Load models
    cascade_face_model = load_models("cascade")
    hog_face_model = load_models("hog")
    # Read images twice
    img1 = read_img(f"{img_name}")
    img2 = np.copy(img1)
    # Test Cascade Model
    faces = cascade_face_model.detectMultiScale(img1, 1.1, 4)
    if len(faces):
        print("\nCascade model detected face\n")
        for (x, y, h, w) in faces:
            cv.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 2)
    else:
        print("\nCascade model did not detect any face\n")

    # Test HOG Model
    faces = hog_face_model(img2, 1)
    if faces:
        print("HOG model detected face")
        for face in faces:
            cv.rectangle(img2, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)
    else:
        print("HOG model did not detect any face")

    cv.putText(img1, "CASCADE", (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.putText(img2, "HOG", (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    img = np.hstack((img1, img2))
    cv.imshow("Test", img)
    cv.waitKey(0)


def hash_face_compare_test(sketch_path, image_db):
    sketches = os.listdir(sketch_path)
    sketch_hash = {}
    for sketch in sketches:
        hash_value = imagehash.average_hash(Image.open(f"{sketch_path}\\{sketch}"))
        sketch_hash[sketch] = hash_value

    images = os.listdir(image_db)
    image_hash = {}
    for image in images:
        hash_value = imagehash.average_hash(Image.open(f"{image_db}\\{image}"))
        image_hash[image] = hash_value

    cutoff = 30
    result = {}
    for sketch in sketches:
        matches = []
        for image in images:
            hash1 = sketch_hash[sketch]
            hash2 = image_hash[image]
            if hash1 - hash2 < cutoff:
                matches.append(image)
        result[sketch] = matches

    for key, value in result.items():
        print(f"{key} ---> {value}\n\n")


def encodings_face_compare_test(sketch_path, image_db):
    start = time.time()
    error = []
    sketches = os.listdir(sketch_path)
    sketch_encoding = {}
    for sketch in sketches:
        img = read_img(f"{sketch_path}\\{sketch}")
        try:
            encodings = fr.face_encodings(img)[0]
            sketch_encoding[sketch] = encodings
        except Exception:
            error.append(sketch)
    print("SKETCH ENCODINGS DONE")
    end = time.time()
    sketch_time = end - start

    start = time.time()
    images = os.listdir(image_db)
    image_encodings = []
    for image in images:
        img = read_img(f"{image_db}\\{image}")
        try:
            encodings = fr.face_encodings(img)[0]
            image_encodings.append(encodings)
        except Exception:
            error.append(image)
    print("IMAGE DB ENCODINGS DONE")
    end = time.time()
    image_time = end - start

    start = time.time()
    result = {}
    for sketch in sketches:
        matches = []
        match_result = fr.compare_faces(image_encodings, sketch_encoding[sketch])
        for i, res in enumerate(match_result):
            if res:
                matches.append(images[i])
        result[sketch] = matches
        print(f"DONE {sketch}")
    end = time.time()
    compare_time = end - start

    count = 0
    for key, value in result.items():
        count += 1
        print(f"{count}) {key} ---> {value}")

    print("TOTAL SKETCHES".ljust(31), f"---> {len(sketches)}")
    print("TOTAL IMAGES".ljust(31), f"---> {len(images)}")
    print("TOTAL CASES".ljust(31), f"---> {len(sketches) * len(images)}")
    print("TIME TAKEN FOR SKETCH ENCODE".ljust(31), f"---> {sketch_time} Seconds")
    print("TIME TAKEN FOR IMAGE DB ENCODE".ljust(31), f" {image_time} Seconds")
    print("TIME TAKEN FOR COMPARING".ljust(31), f"---> {compare_time} Seconds")
    print("TOTAL IME TAKEN".ljust(31), f"---> {sketch_time + image_time + compare_time} Seconds")
    print(f"Error occured in the following images\n {error}")


def emotion_classifier_test(emotions_image_set, emotions_data_set):
    from keras.models import load_model
    from keras.preprocessing.image import img_to_array

    face_detector_model = dlib.get_frontal_face_detector()
    classifier = load_model("Emotion_Detection.h5")
    class_labels = ['angry', 'happy', 'neutral', 'sad', 'surprised']

    images = os.listdir(emotions_image_set)
    print(f"Images in DB ---> {len(images)}\n")
    time.sleep(3)

    df = pd.read_csv(emotions_data_set)
    image_name = list(map(str, list(df["Name"])))
    image_emotion = list(df["Exp"])
    image_emotion_pair = {i: j for i, j in zip(image_name, image_emotion)}
    print("DONE CREATING PAIRS\n")
    print(f"Images in Excel ---> {len(image_emotion_pair)}\n")
    time.sleep(3)

    count = 0
    accuracy = 0
    error = 0
    error_list = []
    for img in images:
        count += 1
        print(f"{count}    --->    {img}")
        try:
            image = read_img(f"{emotions_image_set}\\{img}")
            detected_faces = face_detector_model(image, 1)
            if not detected_faces:
                error_list.append(img)
                continue
            for face in detected_faces:
                top, left = face.top(), face.left()
                bottom, right = face.bottom(), face.right()
                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                face = image[top:bottom, left:right]
                face = cv.resize(face, (48, 48), interpolation=cv.INTER_AREA)
                if np.sum([face]):
                    face = face.astype('float') / 255.0
                    face = img_to_array(face)
                    face = np.expand_dims(face, axis=0)
                prediction = classifier.predict(face)[0]
                result = class_labels[prediction.argmax()]
                if result == image_emotion_pair[img]:
                    accuracy += 1
                else:
                    error += 1
        except Exception:
            error_list.append(img)
            error += 1
    total_images = accuracy + error

    print("\n\n-----------------------------------\n")
    print("          READINGS OF TEST             ")
    print("\n-----------------------------------\n\n")
    print(f"TEST CASES     --->   {total_images} IMAGES")
    print(f"ACCURACY       --->   {accuracy} ({accuracy / total_images} %)")
    print(f"ERROR          --->   {error} ({error / total_images} %)")


if __name__ == "__main__":
    print("\n---------------")
    # Path specifies the location of image dataset
    # path = r".\CASIA_FACE_DATASET"
    # path = r".\NON_FACE_DATASET"
    # path = r".\CUHK_SKETCH_DATASET"
    # sketchPath = r".\sketch_samples"
    # imageDb = r".\image_database"
    # emotionImageSet = r".\emotion_dataset\emotion_imageset"
    # emotionDataSet = r".\emotion_dataset\emotion_dataset.csv"

    # CASIA has over 493021 face images of 10570 individuals.
    # Hence, we extract 2 images of every individual i.e. 10570*2 -> 21140 images
    # preprocessing()

    # To find time taken to load models
    # start = time.time()
    # load_models("cascade")
    # end = time.time()
    # print(f"TIME TAKEN TO LOAD CASCADE MODEL  --->   {(end-start)} seconds")
    # print("\n---------------\n")
    # start = time.time()
    # load_models("hog")
    # end = time.time()
    # print(f"TIME TAKEN TO LOAD HOG MODEL  --->   {(end-start)} seconds")

    # To evaluate the performance of Cascade model
    # cascade_test(path)

    # To evaluate the performance of HOG model
    # hog_test(path)

    # To evaluate the performance of both models on a single image
    # path_of_image = "./C_NATURAL_IMAGES_DATASET/flower_0752.jpg"
    # unit_test(path_of_image)

    # To evaluate the Sketch Recognition performance of Hash algorithm
    # hash_face_compare_test(sketchPath, imageDb)

    # To evaluate the Sketch Recognition performance of Encodings algorithm
    # encodings_face_compare_test(sketchPath, imageDb)

    # To evaluate the performance of Emotion Recognition model
    # emotion_classifier_test(emotionImageSet, emotionDataSet)

    # print("\n-------- EXIT -----------\n")
