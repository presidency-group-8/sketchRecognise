import os
import time
import cv2 as cv
import dlib
import numpy as np

def preprocessing():
    # dataset_path = r".\CASIA_FACE_DATASET"
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
    end = time.time()
    print("\n\n-----------------------------------\n")
    print("          READINGS OF TEST             ")
    print("\n-----------------------------------\n\n")
    print(f"TEST CASES           --->   {total_images} IMAGES")
    print(f"TIME TAKEN           --->   {end-start} SECONDS")
    print(f"HOG DETECTED         --->   {hog_detected}")
    print(f"HOG NOT DETECTED     --->   {hog_not_detected}")


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
    for image in images:
        count += 1
        print(f"WORKING ON IMAGE - {count}")
        img = dataset_path + "\\" + image
        img = cv.imread(img, 0)
        # Detect Faces
        cascade_faces = cascade_face_model.detectMultiScale(img, 1.1, 4)
        if len(cascade_faces):
            cascade_detected += 1
            for (x,y,h,w) in cascade_faces:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.imshow(image, img)
                cv.waitKey(0)

        else:
            cascade_not_detected += 1
    end = time.time()
    print("\n\n-----------------------------------\n")
    print("          READINGS OF TEST             ")
    print("\n-----------------------------------\n\n")
    print(f"TEST CASES           --->   {total_images} IMAGES")
    print(f"TIME TAKEN           --->   {end-start} SECONDS")
    print(f"CASCADE DETECTED     --->   {cascade_detected}")
    print(f"CASCADE NOT DETECTED --->   {cascade_not_detected}")
    # print(f"LIST OF SKETCHES NOT DETECTED BY CASCADE")
    # for face in error:
    #     print(face)


def unit_test(img_name):
    # Load models
    cascade_face_model = load_models("cascade")
    hog_face_model = load_models("hog")
    # Read images twice
    img1 = cv.imread(f"{img_name}")
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
    cv.imshow("TEST", img)
    cv.waitKey(0)


def hash_face_compare(image1, image2):



if __name__ == "__main__":
    print("\n---------------")
    # Path specifies the location of image dataset
    # path = r".\CASIA_FACE_DATASET"
    # path = r".\CUHK_SKETCH_DATASET"
    path = r".\C_NATURAL_IMAGES_DATASET"

    # CASiA has over 493021 face images of 10570 individuals.
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

    # To check performance of Cascade model
    # cascade_test(path)

    # To check performance of HOG model
    # hog_test(path)

    # To check the performance of both models on a single image
    # path_of_image = "./C_NATURAL_IMAGES_DATASET/flower_0752.jpg"
    # unit_test(path_of_image)
    # print("\n-------- EXIT -----------\n")
