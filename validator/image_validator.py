from intellichess.recognition.recognition import ChessRecognizer
import os
import cv2
import shutil

recogniser = ChessRecognizer()
folder_path = 'images for validation'
destination_path = 'validated images'
nonvalid_files = []
for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)
        img = cv2.imread(file_path)
        board, corners = recogniser.predict(img)
        print(filename)
        print(corners.tolist())
        shutil.move(file_path, destination_path)
        #print(board)
    except Exception as e:
        nonvalid_files.append(file_path)
        print(e)
