from langchain.llms import OpenAI
from pdf2image import convert_from_path
import numpy as np
import cv2
import os
import pytesseract 
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\poppler-23.01.0\Library\bin'
apiKey = "..."
os.environ["OPENAI_API_KEY"] = apiKey
llm = OpenAI(temperature=0.3)


def preprocess_image(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    processed_image = cv2.adaptiveThreshold(
        resized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        61,
        11
    )
    return processed_image


def answer(ques):
    prompt = ques + " tell in 150 words"
    return llm.predict(prompt)


def summary(path):
    pages = convert_from_path(path, poppler_path=poppler_path)
    text = ""
    for i in range(len(pages)):
        text += pytesseract.image_to_string(preprocess_image(pages[i]), lang='eng')
        text += '\n'
    prompt = f'Give the summary of "{text}" in 150 words'
    return llm.predict(prompt)


def Summary(path, ques):
    summ = summary(path)
    time.sleep(2)
    prompt = fr'If the summary of a topic is given as "{summ}" then tell {ques}'
    return llm.predict(prompt)

if __name__ == '__main__':
    print(Summary("test.pdf", "What is communication"))
