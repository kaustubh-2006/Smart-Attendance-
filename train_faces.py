import cv2
import os
import numpy as np
import pickle

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}

label_id = 0

# 🔥 SORT folders to keep label ↔ StudentID mapping correct
student_folders = sorted(os.listdir("faces"))

for student_id in student_folders:
    folder_path = os.path.join("faces", student_id)
    if not os.path.isdir(folder_path):
        continue

    print("Training for:", student_id)

    # Map numeric label → StudentID
    label_map[label_id] = student_id

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        face_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if face_img is None:
            continue

        faces.append(face_img)
        labels.append(label_id)

    label_id += 1

# Train model
recognizer.train(faces, np.array(labels))

# Save trained model
recognizer.save("face_model.yml")

# Save label map
with open("label_map.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("✅ Face model trained with CORRECT label mapping")
print("Label Map:", label_map)
