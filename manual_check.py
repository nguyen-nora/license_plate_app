import tkinter
from VN_language import *
import PIL.Image, PIL.ImageTk
import datetime
from utils import Validation_int, Validation_str
from utils import msg_question, save_image_background, save_image_license

class Manual_check():
    
    def __init__(self, cam1, cam2, isIN, database):
        
        self.window = tkinter.Toplevel()
        self.window.title("Kiểm tra thủ công")
        self.window.geometry("1000x700-100-100")
        
        driver = PIL.Image.open("image\img_src\driver.png")
        driver = driver.resize((400, 300), PIL.Image.Resampling.LANCZOS)
        self.driver_ex=PIL.ImageTk.PhotoImage(driver)
        
        license = PIL.Image.open("image\img_src\license_plate.png")
        license = license.resize((400, 300), PIL.Image.Resampling.LANCZOS)
        self.license_ex=PIL.ImageTk.PhotoImage(license)
        
        self.cam1 = cam1
        self.cam2 = cam2
        self.isIN = isIN
        self.my_DB = database
        
        self.window.columnconfigure(0,weight=1)
        self.window.columnconfigure(1,weight=1)
        self.window.rowconfigure(0,weight=1)
        
        # Tạo frame chứa thông tin cần điền
        self.left_frame= tkinter.Frame(self.window, bg=terumo_color, border=5)
        self.left_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        
        self.left_frame.columnconfigure(0,weight=1)
        self.left_frame.columnconfigure(1,weight=1)
        self.left_frame.rowconfigure(0,weight=1)
        self.left_frame.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),weight=5)
        
        # Tạo frame chứa hình ảnh
        self.right_frame= tkinter.Frame(self.window, bg="red", border=5)
        self.right_frame.grid(row=0, column=1, sticky=tkinter.NSEW)
        
        self.right_frame.columnconfigure(0,weight=1)
        self.right_frame.rowconfigure(0,weight=1)
        self.right_frame.rowconfigure((1,2),weight=3)
        self.right_frame.rowconfigure(3,weight=1)
        
        # Label chứa thời gian vào
        left_label = tkinter.Label(self.left_frame, padx=2, pady=5, font = "bold", text="Nhập thông tin ")  
        left_label.grid(row=0, column=0, columnspan= 2, sticky="nsew" )
        self.entry_license = self.make_entry_gui(1, 0, "Nhập biển số: ", "Ví dụ: 38-F7390.01")
        self.entry_license.bind("<FocusIn>", lambda args: self.entry_license.delete('0', 'end'))
        
        self.entry_id = self.make_entry_gui(2, 0, "Nhập mã nhân viên:","Ví dụ: 238299 hoặc căn cước công dân")
        self.entry_id['validatecommand'] = (self.entry_id.register(Validation_int),'%P','%d')
        self.entry_id.bind("<FocusIn>", lambda args: self.entry_id.delete('0', 'end'))
        
        self.entry_name = self.make_entry_gui(3, 0, "Nhập họ tên: ", "Ví dụ: Nguyễn Đức Quân")
        self.entry_name['validatecommand'] = (self.entry_name.register(Validation_str),'%P','%d')
        self.entry_name.bind("<FocusIn>", lambda args: self.entry_name.delete('0', 'end'))
        
        self.Time_label = self.make_label_gui(4, 0, "Thời gian: ")
        self.ID_label = self.make_label_gui(5, 0, "ID thẻ: ")
        self.make_button_gui(10, 0, "Bấm nút để lấy hình ảnh", self.get_image_manual_check, 2)
        self.make_button_gui(15, 0, "Đồng ý", self.create_info)
        self.make_button_gui(15,1, "Hủy", self.cancel_create_info)
        
        right_label = tkinter.Label(self.right_frame, background="#3cb371", padx=2, pady=5, font = "bold", fg = "white", text="hình ảnh")  
        right_label.grid(row=0, column=0, sticky=tkinter.NSEW )
        self.driver_image, self.driver_image_on_canvas = self.make_canvas_gui(1,0, "Ảnh chụp toàn cảnh", self.driver_ex)
        self.license_plate_image, self.license_plate_image_on_canvas = self.make_canvas_gui(2,0, "Ảnh chụp biển số", self.license_ex)
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    # Tạo Gui
    def make_entry_gui(self, row, column, text1, text2):
        # Label chứa thời gian vào
        label = tkinter.Label(self.left_frame, background="#784212", padx=2, pady=5, font = "bold", fg = "white", text=text1)  
        label.grid(row=row, column=column, sticky=tkinter.NSEW )
        
        entry = tkinter.Entry(self.left_frame, bd=5, font=("Arial",15), fg="white", bg="#784212", justify="left", width=30)
        entry.insert(0,text2)
        entry.grid(row=row, column=column+1, sticky=tkinter.NSEW )
        return entry
    
    def make_label_gui(self,row, column, text):
        # Label chứa thời gian vào
        label = tkinter.Label(self.left_frame, background="#784212", padx=2, pady=5, font = "bold", fg = "white", text=text)  
        label.grid(row=row, column=column, sticky=tkinter.NSEW )
        # Label chứa thời gian vào
        label = tkinter.Label(self.left_frame, background="#784212", padx=2, pady=5, font = "bold", fg = "white", text=text)  
        label.grid(row=row, column=column+1, sticky=tkinter.NSEW )
        return label
        
    
    def make_button_gui(self, row, column, text, function, columnspan = 1):
        button = tkinter.Button(self.left_frame, text=text, cursor="hand2", command=function)
        button.grid(row=row, column=column, columnspan=columnspan)
    
    def make_canvas_gui(self, row, column, text, image):
        frame=tkinter.Frame(self.right_frame, bg="#3cb371", border=5)
        frame.grid(row=row, column=column, sticky=tkinter.NSEW)   

        label = tkinter.Label(frame, text=text)  # Hiển thị tên của frame đang phát camera, ví dụ "IP_Cam1"
        label.pack(side= tkinter.TOP,fill=tkinter.BOTH, expand=True)

        canvas_another_window = tkinter.Canvas(frame, width=400, height=300, background="#784212")
        canvas_another_window.pack(fill=tkinter.BOTH, expand=True)
        image_on_canvas = canvas_another_window.create_image(0, 0, anchor='nw', image= image)
        return canvas_another_window, image_on_canvas 
    
    def create_info(self):
        
        license_plate = self.entry_license.get()
        employ_id = self.entry_id.get()
        employ_id =int(employ_id)
        name = self.entry_name.get()
        id_card = self.id_card
        today = self.now
        
        respond = msg_question()
        if respond:
            if self.isIN :
                img_path_license = save_image_license(frame=self.img1, success= True)
                img_path_background = save_image_background(frame= self.img2, success= True)
                self.my_DB.info_insert(id_card, today, license_plate, 'IN', 'OK', 0, 0, img_path_background, img_path_license, None, None, None, None)
            else:
                img_path_license = save_image_license(frame= self.img2, success= True)
                img_path_background = save_image_background(frame= self.img1, success= True)
                self.my_DB.info_insert(id_card, today, license_plate, 'IN', 'OK', 0, 0, img_path_background, img_path_license, None, None, None, None)
            self.on_close()
    def cancel_create_info(self):
        self.window.destroy()
    
    #
    def get_image_manual_check(self):
        
        self.now = datetime.datetime.now()
        self.today = str(self.now.strftime("%Y-%m-%d %H:%M:%S"))
        self.id_card = 145739
        
        canvas_width = self.license_plate_image.winfo_width()
        canvas_height = self.license_plate_image.winfo_height()
        ret1, frame1, self.img1 = self.cam1.get_frame_from_cam()
        ret2, frame2, self.img2 = self.cam2.get_frame_from_cam()
        
        resized_image1 = frame1.resize((canvas_width, canvas_height), PIL.Image.Resampling.LANCZOS)
        self.photo1 = PIL.ImageTk.PhotoImage(resized_image1)
        resized_image2 = frame2.resize((canvas_width, canvas_height), PIL.Image.Resampling.LANCZOS)
        self.photo2 = PIL.ImageTk.PhotoImage(resized_image2)
        
        self.Time_label.config( text=self.today)
        self.ID_label.config( text= self.id_card)
        
        if self.isIN :
            self.driver_image.itemconfig(self.driver_image_on_canvas, image=self.photo1)
            self.license_plate_image.itemconfig(self.license_plate_image_on_canvas, image=self.photo2)
        else:
            self.driver_image.itemconfig(self.driver_image_on_canvas, image=self.photo2)
            self.license_plate_image.itemconfig(self.license_plate_image_on_canvas, image=self.photo1)
              
        
    def on_close(self):   # PEP8: `lower_case_names` for functions/methods/variables
        self.running = False
        #self.stream.stop()   # don't stop stream
        self.window.destroy()
        