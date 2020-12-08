#!/usr/bin/env python3
import face_recognition
import os
import cv2

import door

def image_filter(file):
    extension = os.path.splitext(file)[1]
    accepted_extensions = [ #  https://docs.opencv.org/master/d4/da8/group__imgcodecs.html
        ".bmp", ".dib",
        ".jpeg", ".jpg", ".jpe",
        ".jp2",
        ".png",
        ".webp",
        ".pbm", ".pgm", ".ppm", ".pxm", ".pnm",
        ".pfm",
        ".sr", ".ras",
        ".tiff", ".tif",
        ".exr",
        ".hdr", ".pic"
    ]

    if extension in accepted_extensions:
        return True
    return False

def load_family_faces():
    face_encodings = []
    face_names = []

    print("Loading family members")
    for directory, _unused, files in os.walk("family"):
        for file in filter(image_filter, files):
            print(f"    {os.path.splitext(file)[0]}")
            path = os.path.join(directory, file)
            image = face_recognition.load_image_file(path)
            face_encodings.append(face_recognition.face_encodings(image)[0])
            face_names.append(os.path.splitext(file)[0])
    return face_encodings, face_names

def recognize_faces(frame, known_face_encodings, known_face_names):
    rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)
    return face_locations, face_names

openLock = cv2.imread("assets/lock-open.png", cv2.IMREAD_UNCHANGED)
closedLock = cv2.imread("assets/lock-closed.png", cv2.IMREAD_UNCHANGED)
def draw_lock(frame, x_offset, y_offset):
    lock = openLock if door.isOpened() else closedLock
    y1, y2 = y_offset, y_offset + lock.shape[0]
    x1, x2 = x_offset, x_offset + lock.shape[1]
    alpha_s = lock[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        frame[y1:y2, x1:x2, c] = (alpha_s * lock[:, :, c] +
                              alpha_l * frame[y1:y2, x1:x2, c])

def draw_state(frame):
    lockMarginLeft = 8
    textMarginBottom = 32
    if door.isOpened():
        text = f"Welcome {door.unlocker()}"
        color = (192, 223, 133)
    else:
        text = "The door is locked"
        color = (255, 255, 255)

    font = cv2.FONT_HERSHEY_DUPLEX
    text_width, text_height = cv2.getTextSize(text, font, 2, 1)[0]
    textX = int((frame.shape[1] - text_width - lockMarginLeft - openLock.shape[1]) / 2)
    textY = int(frame.shape[0] - textMarginBottom)
    cv2.putText(frame, text, (textX, textY ), font, 2, color, 1)
    lockX = int(textX + text_width + lockMarginLeft)
    lockY = int(textY - text_height / 2 - openLock.shape[0] / 2)
    draw_lock(frame, lockX, lockY)

def draw_result(frame, face_locations, face_names):
    font = cv2.FONT_HERSHEY_DUPLEX

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        rectangleColor = (255, 255, 255)
        textColor = (0, 0, 0)
        if name != "Unknown":
            door.open(name)
            rectangleColor = (192, 223, 133)
            textColor = (255, 255, 255)
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), rectangleColor, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, textColor, 1)
    draw_state(frame)

def main():
    known_face_encodings, known_face_names = load_family_faces()
    cap = cv2.VideoCapture(0)
    i = -1
    face_locations = None
    face_names = None

    while True:
        _ret, frame = cap.read()
        i += 1
        if not i % 3: # Process one out of three frames
            face_locations, face_names = recognize_faces(frame, known_face_encodings, known_face_names)
        draw_result(frame, face_locations, face_names)
        cv2.imshow('SmartDoor', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

main()