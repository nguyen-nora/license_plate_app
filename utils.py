import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime
import os
import cv2
from VN_language import *


def load_image(self):
    self.image = Image.open(self.image_path)
    self.photo = ImageTk.PhotoImage(self.image)

    self.canvas.delete("all")
    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
def resize_image(self, event):
    # Lấy chiều rộng và chiều cao mới của cửa sổ
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()

    # Resize hình ảnh
        
    resized_image = self.image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    self.photo = ImageTk.PhotoImage(resized_image)

    # Cập nhật hình ảnh trong canvas
    self.canvas.delete("all")
    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

def msg_future_feature():
    messagebox.showinfo('Thông báo',sys_future_feature)
    # messagebox.showerror('error', 'Something went wrong!')
    # messagebox.showwarning('warning', 'accept T&C')
    # messagebox.askokcancel('Ok Cancel', 'Are You sure?')
    # messagebox.askyesno('Yes|No', 'Do you want to proceed?')
    # messagebox.askretrycancel('retry', 'Failed! want to try again?')

def msg_question():
    # messagebox.showinfo('Thông báo',toast_future_feature)
    # messagebox.showerror('error', 'Something went wrong!')
    # messagebox.showwarning('warning', 'accept T&C')
    # messagebox.askquestion('Ask Question', 'Do you want to continue?') # Trả về Yes hoặc No
    # messagebox.askokcancel('Ok Cancel', 'Are You sure?') Trả về True False
    respond = messagebox.askyesno('Lưu ý', sys_mess_done) # trả về True nếu chọn Yes, False nếu chọn No
    # messagebox.askretrycancel('retry', 'Failed! want to try again?') # Trả về Truwe hoặc False 
    
    return respond

# Tạo Gui để nhập thông tin vào
def make_entry_gui(frame, row, column, text1, text2, background="#784212", bg="#784212"):
    # Label chứa thời gian vào
    label = tk.Label(frame, background=None, padx=2, pady=5, font = "bold", fg = "black", text=text1)  
    label.grid(row=row, column=column, sticky=tk.NSEW )
    
    entry = tk.Entry(frame, validate="key", bd=5, font=("Arial",15), fg="black", bg=None, justify="left", width=30)
    entry.insert(0,text2)
    entry.grid(row=row, column=column+1, sticky=tk.NSEW )
    return entry

# Chỉ cho phép nhập ký tự số, ko cho phép ký tự chữ
def Validation_int(inStr,acttyp): #inStr là p: Chuỗi đang có, acttyp là d: hành động vừa xảy ra
    if acttyp == '1': #insert, 0 là delete
        if not inStr.isdigit():
            return False
    return True

# Chỉ cho phép nhập ký tự, ko cho phép số
def Validation_str(inStr,acttyp): #inStr là p: Chuỗi đang có, acttyp là d: hành động vừa xảy ra
    if acttyp == '1': #insert, 0 là delete
        if any(char.isdigit() for char in inStr):
            return False
    return True
    
# Chụp ảnh frame hiện tại, ĐÃ TEST XONG (tkCamera)
def snapshot(filename=None, frame = None, text =''):
    
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))
    image_path = "image/screen_image/"+date_today
    os.makedirs(image_path, exist_ok=True)
    
    if not filename:
        filename = datetime.datetime.now().strftime("-screen-%d-%m-%Y-%H-%M-%S")
        filename = text + filename +'.png'
        #cv2.imwrite(os.path.join(image_path , filename), self.origin_frame)
        
    cv2.imwrite(os.path.join(image_path , filename), frame)
    # print(toast_snapshort_cv2, filename)

# Lưu ảnh biển số, toàn cảnh, ĐÃ TEST XONG (tkCamera, tkButton)
def save_image_license_plate(license_plate_VN, license_plate_crop, save_dir_license_plate):

    today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) #chua ngay thang nam cung voi gio phut giay
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))

    save_dir_license_plate = "license_plate"
    save_dir_ok = "./image/image_result/"+ date_today + "/" + save_dir_license_plate
    save_dir_fail = "./image/image_fail/"+ date_today + "/" + save_dir_license_plate
    
    if license_plate_VN:
        os.makedirs(save_dir_ok, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_ok , save_dir_license_plate +today+'.png'), license_plate_crop)
        img_path = save_dir_ok +"/"+save_dir_license_plate +today+'.png'
        return img_path
        
    else:
        os.makedirs(save_dir_fail, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_fail , save_dir_license_plate +today+'.png'), license_plate_crop)
        img_path = save_dir_fail +save_dir_license_plate +today+'.png'
        return img_path


def save_image_license(frame, success):
    
    today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) #chua ngay thang nam cung voi gio phut giay
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))
    
    save_dir_license = "license"
    save_dir_license_ok = "image/image_result/"+date_today + "/" + save_dir_license
    save_dir_license_fail = "image/image_fail/"+date_today + "/" + save_dir_license
    
    if(success):
        os.makedirs(save_dir_license_ok, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_license_ok , save_dir_license +today+'.png'), frame)
        img_path = save_dir_license_ok + "/"+save_dir_license +today+'.png'
        print(img_path)
        return img_path
        
    else:
        os.makedirs(save_dir_license_fail, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_license_fail , save_dir_license +today+'.png'), frame)
        img_path = save_dir_license_fail + "/"+save_dir_license +today+'.png'
        print(img_path)
        return img_path   
    
def save_image_background(frame, success):
    
    today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) #chua ngay thang nam cung voi gio phut giay
    date_today = str(datetime.datetime.now().strftime("%d-%m-%y"))
    
    save_dir_background = "background"
    save_dir_background_ok = "image/image_result/"+date_today + "/" + save_dir_background
    save_dir_background_fail = "image/image_fail/"+date_today + "/" + save_dir_background
        
    if(success):
        os.makedirs(save_dir_background_ok, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_background_ok , save_dir_background +today+'.png'), frame)
        img_path = save_dir_background_ok + "/"+save_dir_background +today+'.png'
        return img_path
        
    else:
        os.makedirs(save_dir_background_fail, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir_background_fail , save_dir_background +today+'.png'), frame)
        img_path = save_dir_background_fail +"/"+save_dir_background +today+'.png'
        return img_path

# Tạo label, kế bên label có chứa label có thể chỉnh sửa, ĐÃ TEST XONG (tkGui)
def set_label_in_row (frame, row, column, text, text_out):
    label = tk.Label(frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text=text)  
    label.grid(row=row, column=column, sticky=tk.NSEW )
    
    info_label = tk.Label(frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text=text_out)  
    info_label.grid(row=row, column=column+1, sticky=tk.NSEW )
    return info_label

# Tạo canvas chứa text, và tự động căn chỉnh text ở bên trong, ĐÃ TEST XONG (tkGui)
def set_canvas_text(frame, row, column, text):
    
    text_license_plate_canvas_IN = tk.Canvas(frame, background="#784212")
    text_license_plate_canvas_IN.grid(row=row, column=column, sticky=tk.NSEW )
    text_on_canvas_IN = text_license_plate_canvas_IN.create_text(10, 80, anchor="nw", text=text, fill="black", font="Helvetica 30 bold")
    text_license_plate_canvas_IN.bind("<Configure>", lambda event:resize_text_in_canvas(event,canvas_store_text= text_license_plate_canvas_IN,
                                                                                                text_id= text_on_canvas_IN, fontsize= 30))
    return text_license_plate_canvas_IN, text_on_canvas_IN

def set_canvas_image (frame, row, column, image):
        # canvans chứa hình ảnh biển số
        image_license_plate_canvas_IN = tk.Canvas(frame, background="#78281F")
        image_license_plate_canvas_IN.grid(row=row, column=column, sticky=tk.NSEW )
        image_on_canvas_IN = image_license_plate_canvas_IN.create_image(0, 0, anchor='nw', image= image)
        return image_license_plate_canvas_IN, image_on_canvas_IN

# Tự động điều chỉnh kích thước cỡ chữ ở trong canvas, ĐÃ TEST XONG (tkGui)
def resize_text_in_canvas(event, canvas_store_text, text_id, fontsize):
    font = "Helvetica %i bold"
    fontsize = fontsize
    x0 = canvas_store_text.bbox(text_id)[0] # x-coordinate of the left side of the text
    canvas_store_text.itemconfigure(text_id, width=canvas_store_text.winfo_width() - x0, font=font % fontsize)
    # shrink to fit
    height = canvas_store_text.winfo_height() # canvas height
    y1 = canvas_store_text.bbox(text_id)[3] # y-coordinate of the bottom of the text
    while y1 > height and fontsize > 1:
        fontsize -= 1
        canvas_store_text.itemconfigure(text_id, font=font % fontsize)
        y1 = canvas_store_text.bbox(text_id)[3]
    