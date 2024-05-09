import sys
log_file_path = "log\log.txt"
sys.stdout = open(log_file_path, "a")
sys.stderr = open(log_file_path, "a")

from tkCamera import tkCamera
from VN_language import *
import tkinter
import PIL.Image, PIL.ImageTk
from tkGUI import make_gui_infor
from tkButton import make_gui_btn

class App:
    def __init__(self, window, title, sources):

        self.window = window
        self.window.geometry("1200x900-100-100")
        self.window.title(title)
        self.stream_widgets = []

        width = 400
        height = 300
        self.simple_image = PIL.Image.open("image\img_src\img203.png")
        self.simple_image=PIL.ImageTk.PhotoImage(self.simple_image)
        
        # Cấu hình window theo dạng lưới (3x3)
        self.window.columnconfigure((0,1),weight=3, uniform="a")
        self.window.columnconfigure(2,weight=1, uniform="a")
        self.window.rowconfigure((0,1),weight=4, uniform="a")
        self.window.rowconfigure(2,weight=1, uniform="a")
        
           
        Cam1 = tkCamera(self.window, 0, 0, width, height, sources, text= "Cam toàn cảnh", source= 'demo\demo.mp4')
        self.stream_widgets.append(Cam1)
        
        Cam2 = tkCamera(self.window, 0, 1, width, height, sources, text= "Cam biển số", source= sources[0][1])
        self.stream_widgets.append(Cam2)
        
        IN_frame = make_gui_infor(self.window, row = 1, column = 0, text = "Thông tin lúc vào", image = self.simple_image, IN= True)   
        OUT_frame = make_gui_infor(self.window, row = 1, column = 1, text = "Thông tin lúc ra", image = self.simple_image, IN= False)  
        button = make_gui_btn(self.window, row=2, column=0, columnspan=3, cam1= Cam1, cam2= Cam2, frame1= IN_frame, frame2= OUT_frame)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self, event=None):
        # print("[App] stoping threads")
        #self.my_DB.cleanup_before_exit()
        for widget in self.stream_widgets:
            widget.running = False

        # print("[App] exit")
        self.window.destroy()

class Start(object):
    
    def __init__(self):
        global cam1, cam2, sources
        cam1 = ""
        cam2 = ""
        sources =[]
        self.window = tkinter.Tk()
        self.window.geometry("400x300-700-500")
        self.window.title("SmartVN")
        
        L0 = tkinter.Label(self.window, text="Nhập địa chỉ Camera, chỉ chấp nhận rtsp")
        L0.pack()
        
        L1 = tkinter.Label(self.window, text="Cam toàn cảnh")
        L1.pack()
        
        self.E1 = tkinter.Entry(self.window, width=40, bd =5)
        self.E1.insert(0, IP_cam1)
        self.E1.pack()
        
        L2 = tkinter.Label(self.window, text="Cam biển số ")
        L2.pack()
        
        self.E2 = tkinter.Entry(self.window, width=40, bd =5)
        self.E2.insert(0, IP_cam2)
        self.E2.pack()
        
        B = tkinter.Button(self.window, text ="Bắt đầu", background='tomato', cursor="hand2", command = self.callback)
        B.pack()
        
        self.L3 = tkinter.Label(self.window, text="Hãy điền đầy đủ địa chỉ 2 camera")
        self.window.mainloop()
        
    def callback(self):
        global cam1, cam2, sources
        cam1 =self.E1.get()
        cam2 =self.E2.get()
        
        if cam1 == "" or cam2 == "":
            self.L3.pack()
            return
        if cam1.isdigit():
            cam1 = int(cam1)
        if cam2.isdigit():
            cam2 = int(cam2)
        sources.append(("Cam toàn cảnh", cam1))
        sources.append(("Cam biển số", cam2))
        self.window.destroy()
        App(tkinter.Tk(), "SmartVN", sources)

if __name__ == "__main__":
    
    Start()
    
    
    