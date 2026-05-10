import os
import cv2
import tkinter as tk
import easyocr
import matplotlib.pyplot as plt


CASCADE_PATH = "haarcascade_russian_plate_number.xml"
SAVE_DIR = "captures"
PLATE_FILE = os.path.join(SAVE_DIR, "plate.jpg")

os.makedirs(SAVE_DIR, exist_ok=True)


def screen():
    haarcascade = cv2.CascadeClassifier(CASCADE_PATH)
    if haarcascade.empty():
        print("Could not load cascade file:", CASCADE_PATH)
        return

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    min_area = 500
    plate_img = None

    while True:
        success, img = cap.read()
        if not success:
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = haarcascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            if w * h > min_area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Number plate", (x, y - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                plate_img = img[y:y + h, x:x + w]
                cv2.imshow("Plate", plate_img)

        cv2.imshow("Result", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and plate_img is not None:
            cv2.imwrite(PLATE_FILE, plate_img)
            cv2.rectangle(img, (0, 200), (640, 300), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, "Saved!", (15, 265),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow("Final", img)
            cv2.waitKey(500)
            break
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def citit():
    if not os.path.exists(PLATE_FILE):
        print("No plate captured yet. Use the Capture button first.")
        return

    img = cv2.imread(PLATE_FILE)
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(img)

    for bbox, text, score in results:
        print(text, round(score, 2))
        p1 = tuple(map(int, bbox[0]))
        p2 = tuple(map(int, bbox[2]))
        cv2.rectangle(img, p1, p2, (0, 255, 0), 1)
        cv2.putText(img, text, p1, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


tab = tk.Tk()
tab.geometry("500x500")
tab.resizable(width=False, height=False)
tab.configure(background='black')

btn_capture = tk.Button(tab, text='Capture', command=screen, bg='blue', fg='red')
btn_capture.pack(padx=100, pady=20, side=tk.LEFT)

btn_read = tk.Button(tab, text='Read', command=citit, bg='blue', fg='red')
btn_read.pack(padx=100, pady=20, side=tk.RIGHT)

tab.mainloop()
