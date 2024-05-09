import PIL.ImageTk
import tkinter
from videocapture import VideoCapture
from VN_language import *
from tkinter import *
import threading

            
# Class tạo giao diện cho mỗi camera
class tkCamera(tkinter.Frame):

    def __init__(self, window, row, col, width=None, height=None, sources=None, text="", source=0):

        super().__init__(window)

        self.source = source # source hiện tại đang phát trực tiếp
        self.other_sources = sources # Tất cả các source đã khai báo
        
        # Vị trí đặt camera theo hàng và cột
        self.vid = VideoCapture(self.source, width, height)
        # print(toast_connected, self.source)
        self.canvas = self.make_gui_camera(text, window, row, col, width, height)   

        self.delay = int(100/self.vid.fps)
        self.running = True
        self.update_frame()
          
    def make_gui_camera(self, text, window, row, column, width, height):
        
        # frame chứa camera 
        frame_toan_canh=Frame(window, width=200, height=400, bg="#3cb371", border=5)
        frame_toan_canh.grid(row=row, column=column, sticky=NSEW)   
        
        # Label hiển thị tên camera, ví dụ "Cam toan canh"
        label = tkinter.Label(frame_toan_canh, text=text)  
        label.pack(side= TOP,fill=BOTH)

        # Canvas chứa hình ảnh lấy từ camera
        canvas = tkinter.Canvas(frame_toan_canh, width=width, height=height)
        canvas.pack(fill=BOTH, expand=True)
        return canvas

    def origin_frame(self):
        _,frame = self.vid.get_origin_frame()
        return frame

    def update_frame(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        # Lấy chiều cao, chiều rộng của frame chứa camera
        self.canvas.update()
        width = self.canvas.winfo_width()
        height= self.canvas.winfo_height()
        # print(width,height )
        if ret:
            resized_image= frame.resize((width,height), PIL.Image.Resampling.LANCZOS)
            self.photo = PIL.ImageTk.PhotoImage(image=resized_image)
            id_image = self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        if self.running:
            self.after(self.delay, self.update_frame)
    
    def get_frame_from_cam(self):
        ret1, frame = self.vid.get_frame()
        ret2, origin_frame = self.vid.get_origin_frame()
        return ret1, frame, origin_frame
            
    def open_new_window(self, is_quick_view):
        
        self.new_window = threading.Thread(target= another_window, args=(self.vid,is_quick_view))
        self.new_window.start()
        return self.new_window
        
class another_window():

    def __init__(self, source, is_quick_view):
        
        self.vid = source
        self.is_quick_view = is_quick_view
        
        self.window = tkinter.Toplevel()
        self.window.title("Chế độ xem nhanh")
        self.window.geometry("1200x800-0-100")
        
        self.window.columnconfigure((0,2),weight=1, uniform="a")
        self.window.columnconfigure(1,weight=4, uniform="a")
        self.window.rowconfigure(0,weight=1, uniform="a")
        
        self.stop = False
        self.make_gui_camera("camera")
        self.make_label()
        self.make_label_result(0,2)
        self.running = True
        self.delay = int(100/self.vid.fps)

        self.update_frame_another_window()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame_another_window(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        width = self.frame_quick_view.winfo_width()
        height= self.frame_quick_view.winfo_height()
        # print(width,height )
        if ret:
            self.image = frame
            resized_image= self.image.resize((width,height), PIL.Image.Resampling.LANCZOS)
            self.photo = PIL.ImageTk.PhotoImage(image=resized_image)
            
            # Creat image của canvas luôn chiếm nhiều bộ nhớ vì nó không thay thế cái cũ, nó luôn tạo ra cái mới
            # Vì vậy tạo 1 biến chứa id cảu các image khi tạo, và biens này sẽ được thay thế bằng id mới
            # Không gây ra vấn đè về bộ nhớ
            id_image = self.canvas_another_window.create_image(0, 0, image=self.photo, anchor='nw')

        if self.running:
            self.window.after(self.delay, self.update_frame_another_window)

    def make_label_result(self, row, column):
        
        right_frame= tkinter.Frame(self.window, bg=gray_color, border=5)
        right_frame.grid(row=row, column=column, sticky=tkinter.NSEW)
        # Frame chứa thông tin làn
        infor_lane= tkinter.Frame(right_frame, width=200, height=100, bg ="#784212")
        infor_lane.pack(fill=tkinter.BOTH,pady=(0,5), expand=True)
        
        # hiển thị tên làn
        self.info_lane1 = tkinter.Label(infor_lane, text="Thông tin quang cao")
        self.info_lane1.pack(side="top", fill=tkinter.BOTH)
        
        # Frame chứa kết quả so sánh
        result_frame= tkinter.Frame(right_frame, bg ="#154360")
        result_frame.pack(fill=tkinter.BOTH, pady=(0,5))
        
        # hiển thị tên 
        self.result_label = tkinter.Label(result_frame, text="Kết quả")  # Hiển thị tên của frame đang phát camera, ví dụ "IP_Cam1"
        self.result_label.pack(side="bottom", fill=tkinter.BOTH)
        

        self.result_canvas= tkinter.Canvas(result_frame, background="#784212")
        self.text_result_canvas = self.result_canvas.create_text(30, 100, anchor="nw", text=sys_pass, fill="black", font="Helvetica 20 bold")
        self.result_canvas.pack(fill=tkinter.BOTH)

    def make_gui_camera(self, text):
        
        # frame chứa camera toàn cảnh
        self.frame_quick_view=Frame(self.window, width=200, height=400, bg="#3cb371", border=5)
        self.frame_quick_view.grid(row=0, column=1, sticky=NSEW)   

        # Self trong câu lệnh dưới là chỉ bản thân frame gọi nó, widget ở bên file main, đặt breakpoint và xem biến self
        self.label = tkinter.Label(self.frame_quick_view, text=text)  # Hiển thị tên của frame đang phát camera, ví dụ "IP_Cam1"
        self.label.pack(side= TOP,fill=BOTH)

        self.canvas_another_window = tkinter.Canvas(self.frame_quick_view, width=self.vid.width, height=self.vid.height, background="red")
        self.canvas_another_window.pack(fill=BOTH, expand=True)
    
    def make_label(self, row = 0, column= 0):
        left_frame= tkinter.Frame(self.window, bg=gray_color, border=5)
        left_frame.grid(row=row, column=column, sticky=tkinter.NSEW)
        
        # hiển thị tên làn
        self.info_lane1 = tkinter.Label(left_frame, text="Thông tin vao: ")
        self.info_lane1.pack(side="top", fill=tkinter.BOTH, padx=(0,5))
        
        self.license_plate_label_IN = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="Bien so")  
        self.license_plate_label_IN.pack(fill=tkinter.BOTH, padx=5)
        
        self.name_label_IN = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="ho ten")  
        self.name_label_IN.pack(fill=tkinter.BOTH, padx=5)
        
        self.time_label_IN = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="Time")  
        self.time_label_IN.pack(fill=tkinter.BOTH, padx=5)
        
        # hiển thị tên làn
        self.info_lane1 = tkinter.Label(left_frame, text="Thông tin ra: ")
        self.info_lane1.pack( fill=tkinter.BOTH, padx=(0,5))
        
        self.license_plate_label_OUT = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="Bien so")  
        self.license_plate_label_OUT.pack(fill=tkinter.BOTH, padx=5)
        
        self.name_label_OUT = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="ho ten")  
        self.name_label_OUT.pack(fill=tkinter.BOTH, padx=5)
        
        self.time_label_OUT = tkinter.Label(left_frame, background="#0E6655", padx=2, pady=5, font = "bold", fg = "white", text="Time")  
        self.time_label_OUT.pack(fill=tkinter.BOTH, padx=5)
    
    def IN_success (self,today,name,license_plate ):
        # Canvas chứa kết quả so sánh
        self.result_canvas.configure(bg=terumo_color)
        self.result_canvas.itemconfig(self.text_result_canvas, text="Hợp lệ") 
        
        # Label chứa thời gian vào, id lúc vào, mã nhân viên, họ tên nhân viên
        self.time_label_IN.config( text=today)
        self.name_label_IN.config( text= name)
        self.license_plate_label_IN.config(text = license_plate)
    def on_close(self):   # PEP8: `lower_case_names` for functions/methods/variables
        self.running = False
        self.is_quick_view = False
        #self.stream.stop()   # don't stop stream
        self.window.destroy()
        
        
