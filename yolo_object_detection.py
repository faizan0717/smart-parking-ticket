import cv2
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
from datetime import datetime

class OCRApp:
    car_map = {}
    def __init__(self, master):
        self.master = master
        self.master.title("License Plate OCR")
        
        self.file_path = None
        
        self.label = tk.Label(master, text="Select an image:")
        self.label.pack()
        
        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_button.pack()
        
        self.ocr_button = tk.Button(master, text="Perform OCR", command=self.perform_ocr, state=tk.DISABLED)
        self.ocr_button.pack()
        
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()
        
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        
    def select_image(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.ocr_button.config(state=tk.NORMAL)
            self.display_image()
    
    def display_image(self):
        image = cv2.imread(self.file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.canvas.image = image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
    
    def perform_ocr(self):
        harcascade = "model/haarcascade_russian_plate_number.xml"
        plate_cascade = cv2.CascadeClassifier(harcascade)
        img = cv2.imread(self.file_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
        
        min_area = 500
        count = 0
        
        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                img_roi = img[y: y+h, x:x+w]
                
                cv2.imwrite("temp_plate.jpg", img_roi)
                
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                plate_image = cv2.imread("temp_plate.jpg")
                gray_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray_plate)

                
                if text not in self.car_map:
                    self.car_map[text] = datetime.now()
                    self.result_label.config(text=f"Car {text} parked now at {str(datetime.now())}")
                else:
                    parked_time = self.car_map[text]
                    elapsed_time = datetime.now() - parked_time
                    self.result_label.config(text=f"Car {text} parked {elapsed_time} ago")
                    del self.car_map[text]
                count += 1
        
        cv2.imshow("Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

def main():
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
