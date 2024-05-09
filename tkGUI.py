import tkinter
from utils import set_label_in_row, set_canvas_text, set_canvas_image
from VN_language import *

class make_gui_infor():
    
    def __init__(self, window, row, column, text = "New Frame", image = None, IN= True):
        
        # frame chứa thông tin lúc vào
        IN_frame= self.make_frame(window,row, column, text)
        
        if IN:
            self.Time_label_IN = set_label_in_row(frame= IN_frame, row=1, column=0, text= sys_time, text_out=" ")
            self.ID_label_IN = set_label_in_row(frame= IN_frame, row=2, column=0, text= sys_id_card, text_out=" ")
            self.Employ_code_IN = set_label_in_row(frame= IN_frame, row=3, column=0, text= sys_employ_id, text_out=" ")
            self.Employ_Name_IN = set_label_in_row(frame= IN_frame, row=4, column=0, text= sys_name, text_out=" ")
        
            self.text_license_plate_canvas_IN, self.text_on_canvas_IN = set_canvas_text(frame=IN_frame, row= 5, column=0, text=sys_license_plate)
            self.image_license_plate_canvas_IN, self.image_on_canvas_IN = set_canvas_image(frame=IN_frame, row= 5, column= 1, image= image)
        else:
            self.Time_label_OUT = set_label_in_row(frame= IN_frame, row=1, column=0, text= sys_time, text_out=" ")
            self.ID_label_OUT = set_label_in_row(frame= IN_frame, row=2, column=0, text= sys_id_card, text_out=" ")
            self.Employ_code_OUT = set_label_in_row(frame= IN_frame, row=3, column=0, text= sys_employ_id, text_out=" ")
            self.Employ_Name_OUT = set_label_in_row(frame= IN_frame, row=4, column=0, text= sys_name, text_out=" ")
        
            self.text_license_plate_canvas_OUT, self.text_on_canvas_OUT = set_canvas_text(frame=IN_frame, row= 5, column=0, text=sys_license_plate)
            self.image_license_plate_canvas_OUT, self.image_on_canvas_OUT = set_canvas_image(frame= IN_frame, row= 5, column= 1, image= image)

    # Tạo frame theo dạng lưới và đặt tên cho frame, nằm ở hàng đầu tiên của frame (phía trên cùng)
    def make_frame (self, window, row, column, text):
        IN_frame=tkinter.Frame(window, width=200, height=400, bg=terumo_color, border=5)
        IN_frame.grid(row=row, column=column, sticky=tkinter.NSEW)

        # Cấu hình frame theo dạng lưới (6x2)
        IN_frame.columnconfigure((0,1),weight=1, uniform="a")
        IN_frame.rowconfigure(0,weight=1, uniform="a")
        IN_frame.rowconfigure((1,4),weight=1, uniform="a")
        IN_frame.rowconfigure(5,weight=5, uniform="a")
        
        infor_label_IN = tkinter.Label(IN_frame, text=text)  
        infor_label_IN.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW )
        return IN_frame
          
