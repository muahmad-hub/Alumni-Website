from .utils import vectorize, save_model, load_model
from sklearn import svm
import pandas as pd
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score     

SKILLS_DATA_PATH = "ai/data/Skill.csv"
MODEL_PATH = "ai/models/svm_model.pkl"
ENCODER_PATH = "ai/models/encoded_labels.pkl"

def train_and_save_model():
    df = pd.read_csv(SKILLS_DATA_PATH)

    encoded_labels_dic = {}
    count = 0
    for label in df["Category"]:
        if label in encoded_labels_dic:
            continue
        else:
            encoded_labels_dic[label] = count
            count += 1

    skill_vector = []
    encoded_labels = []
    for i, skill in enumerate(df["Skill"]):
        with torch.no_grad():
            vector = vectorize(skill)
            skill_vector.append(vector)
        label = encoded_labels_dic[df["Category"][i]]
        encoded_labels.append(label)

    skill_vector = np.vstack(skill_vector)

    # clf = svm.SVC(kernel='linear', probability=True)
    # clf.fit(skill_vector, encoded_labels)


    # Code for testing accuracy of AI
    X_train, X_test, y_train, y_test = train_test_split(
    skill_vector, encoded_labels, test_size=0.2, random_state=42
    )

    clf = svm.SVC(kernel='linear', probability=True)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {acc:.2%}")

    save_model(clf, MODEL_PATH)
    save_model(encoded_labels_dic, ENCODER_PATH)

def predict_category(text):
    model = load_model(MODEL_PATH)
    encoded_labels_dic = load_model(ENCODER_PATH)

    with torch.no_grad():
        tokens = vectorize(text)

    probabilities = model.predict_proba(tokens)[0]

    # Alternative manual implementation of argmax
    # highest = 0
    # encoded_label = None
    # for i, prob in enumerate(probabilities):
    #     if prob > highest:
    #         highest = prob
    #         encoded_label = i

    # Using Numpy for production due to effeciency

    encoded_label = int(np.argmax(probabilities))

    label = None

    for key, value in encoded_labels_dic.items():
        if value == encoded_label:
            label = key
            break

    probability = float(probabilities[encoded_label])

    return label, probability

train_and_save_model()
# want_more = True
# x = input("Enter a skill: ")
# while want_more:
#     label, probability = predict_category(x)
#     print(f"{probability} that it is {label}")

#     x = input("Want more: ")
#     if x == "n":
#         want_more = False

