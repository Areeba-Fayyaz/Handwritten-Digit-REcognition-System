import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tkinter import *
import tkinter.font as tkFont
from win32gui import FindWindow,GetWindowRect
import PIL
import cv2
from tkinter import filedialog,ttk
import numpy as np
from PIL import ImageGrab,ImageTk
from PIL import Image, ImageDraw#
from keras.models import load_model


model = load_model("mnist.h5")
image_folder = "img/"
lastx, lasty = None, None
image_number = 0
#filename='img/handwritten1.jpg'



def clear_widget():
    global cv, image1, draw, text
    image1 = PIL.Image.new("RGB", (800, 600), (255, 255, 255))
    text.delete(1.0, END)
    draw = ImageDraw.Draw(image1)
    cv.delete('all')


def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width=8, fill='black', capstyle=ROUND, smooth=TRUE, splinesteps=12)
    draw.line([lastx, lasty, x, y], fill="black", width=10)#
    lastx, lasty = x, y


def activate_event(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y


def Recognize_Digit():
    text_num = []
    global image_number
    filename = f'img_{image_number}.png'
    widget = cv

###############
    win=FindWindow(None,"Digit Recognition System")
    rect=GetWindowRect(win)
    list_rect=list(rect)
    list_frame=[-9,-38,9,190]
    final_rect=tuple((map(lambda x,y:x-y,list_rect,list_frame)))
    img=ImageGrab.grab(bbox=final_rect)
    img.save(filename)
    
###############
    # get image and save
    #image1.save(filename)
    image = cv2.imread(filename)
    
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
        digit = th[y:y + h, x:x + w]
        resized_digit = cv2.resize(digit, (18, 18))
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        print(padded_digit.shape)
        digit = padded_digit.reshape(1, 28, 28, 1)
        digit = digit / 255.0

        pred = model.predict([digit])[0]
        final_pred = np.argmax(pred)
        text_num.append([x, final_pred])


        data = str(final_pred) + ' ' + str(int(max(pred) * 100)) + '%'

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (0, 0, 0)
        thickness = 1
        cv2.putText(image, data, (x, y - 5), font, fontScale, color, thickness)

    text_num = sorted(text_num, key=lambda t: t[0])
    text_num = [i[1] for i in text_num]
    final_text = "".join(map(str, text_num))
    text.insert(END, final_text)
    cv2.imshow('Predictions', image)
    cv2.waitKey(0)
def upload_image():
    global cv,filename
    filename=filedialog.askopenfilename(initialdir="/Program Files/Python39/Handwritten-Multiple-Digits-Recognizer-main",title="Select a file",filetype=(("jpeg","*.jpg"),('PNG Files','*.png'),("All Files","*.*")))
    #l1=Label(root,text="")
    #l1.grid(row=0, column=0, pady=3, padx=1)
    #l1.configure(text=filename)
   
    #img = ImageTk.PhotoImage(Image.open(filename))
    img = ImageTk.PhotoImage(file=filename)
    
    cv.create_image(200, 80, image=img, anchor=NW)
    #my_im=Label(image=img).grid(row=0, column=1, pady=10, padx=1)
    #img=img.configure(width = 40, activebackground = "#33B5E5", relief = FLAT)
    
    cv.create_window(240, 250, anchor=NW, window=img)
    



root = Tk()
root.resizable(0, 0)
root.title("Digit Recognition System")

#img=PhotoImage(file='img/handwritten.png')
#Label(root,image=img).grid(row=0,column=0)

cv = Canvas(root, width=800, height=600, bg='white')
cv.grid(row=0, column=0, pady=2, sticky=NSEW, columnspan=2)
##img = ImageTk.PhotoImage(Image.open(filename))
##cv.create_image(200, 80, image=img, anchor=NW)
cv.bind('<Button-1>', activate_event)

image1 = PIL.Image.new("RGB", (800, 600), (255, 255, 255))
draw = ImageDraw.Draw(image1)

btn_upload= Button(text='Select image',width=15, height=3, command=lambda:upload_image(), font=tkFont.Font(family="Lucida Grande", size=10))
btn_upload.grid(row=3, column=0, pady=10, padx=1)
#btn_upload.configure(width = 40, activebackground = "#33B5E5", relief = FLAT)
#btn_upload= cv.create_window(240, 250, anchor=NW, window=btn_upload)



btn_save=Button(text='Recognize Digits',width=15, height=3, command=Recognize_Digit, font=tkFont.Font(family="Lucida Grande", size=10))
btn_save.grid(row=3, column=1, pady=10, padx=1)


l=Label(root,text="Extracted number: ",font=tkFont.Font(family="Lucida Grande", size=11))
l.grid(row=1, column=0, pady=3, padx=1)
text = Text(root, height=2, width=25, font=tkFont.Font(family="Lucida Grande", size=13))
text.grid(row=2, column=0, pady=1, padx=1)

button_clear = Button(text='Clear Output',width=15, height=3, command=clear_widget, font=tkFont.Font(family="Lucida Grande", size=10))
button_clear.grid(row=2, column=1, pady=5, padx=1)


#img=PhotoImage(file='img/handwritten.png')
#Label(root,image=img).grid(row=0,column=0)


root.mainloop()

