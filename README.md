# Smart Door
Prototype of a door protected with facial recognition using opencv.\
Project made for an Introduction to Artificial Intelligence course.
## Features
- Scan the webcam for known faces in the family folder
- Displays the state of the door
- Keeps the door open for 3 seconds when seeing a known face

## Get started
### Setup
Install [face_recognition](https://github.com/ageitgey/face_recognition#installation)

```
git clone https://github.com/michaelbnd/smart_door
cd smart_door
pip3 install -r requirements.txt
```
### Usage
Customize the face pictures in the family folder
```
./smart_door.py
```

## Limitations
Using a simple webcam comes with limitations :
- This will not work in the dark
- A picture of an allowed person can be shown to the camera to open the door
- False positive are common