from .utils import vectorize, save_model, load_model
from sklearn import svm
import pandas as pd
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score     

SKILLS_DATA_PATH = "ai/data/Skill.csv"
SKILL_MODEL_PATH = "ai/models/skill_svm_model.pkl"
SKILL_ENCODER_PATH = "ai/models/skill_encoded_labels.pkl"

GOAL_DATA_PATH = "ai/data/Goal.csv"
GOAL_MODEL_PATH = "ai/models/goal_svm_model.pkl"
GOAL_ENCODER_PATH = "ai/models/goal_encoded_labels.pkl"

# Give parameter True to load GOALS and False to load SKILLS
def train_and_save_model(is_goal):
    if is_goal:
        df = pd.read_csv(GOAL_DATA_PATH)
        COL1 = "Goal"
        COL2 = "Category"
        model_path = GOAL_MODEL_PATH
        encoder_path = GOAL_ENCODER_PATH
    else:
        df = pd.read_csv(SKILLS_DATA_PATH)
        COL1 = "Skill"
        COL2 = "Category"
        model_path = SKILL_MODEL_PATH
        encoder_path = SKILL_ENCODER_PATH

    encoded_labels_dic = {}
    count = 0
    for label in df[COL2]:
        if label in encoded_labels_dic:
            continue
        else:
            encoded_labels_dic[label] = count
            count += 1

    vector_list = []
    encoded_labels = []
    for i, value in enumerate(df[COL1]):
        with torch.no_grad():
            vector = vectorize(value)
            vector_list.append(vector)
        label = encoded_labels_dic[df[COL2][i]]
        encoded_labels.append(label)

    vector_list = np.vstack(vector_list)

    # clf = svm.SVC(kernel='linear', probability=True)
    # clf.fit(vector_list, encoded_labels)


    # Code for testing accuracy of AI
    X_train, X_test, y_train, y_test = train_test_split(
    vector_list, encoded_labels, test_size=0.2, random_state=42
    )

    clf = svm.SVC(kernel='linear', probability=True)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {acc:.2%}")

    save_model(clf, model_path)
    save_model(encoded_labels_dic, encoder_path)

def predict_category_skill(text):
    model = load_model(SKILL_MODEL_PATH)
    encoded_labels_dic = load_model(SKILL_ENCODER_PATH)

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

def predict_category_goal(text):
    model = load_model(GOAL_MODEL_PATH)
    encoded_labels_dic = load_model(GOAL_ENCODER_PATH)

    with torch.no_grad():
        tokens = vectorize(text)

    probabilities = model.predict_proba(tokens)[0]

    encoded_label = int(np.argmax(probabilities))

    label = None

    for key, value in encoded_labels_dic.items():
        if value == encoded_label:
            label = key
            break

    probability = float(probabilities[encoded_label])

    return label, probability

train_and_save_model(True)
# want_more = True
# x = input("Enter: ")
# while want_more:
#     label, probability = predict_category_goal(x)
#     print(f"{probability} that it is {label}")

#     x = input("Want more: ")
#     if x == "n":
#         want_more = False

