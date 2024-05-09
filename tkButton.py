import tkinter
from VN_language import *
from tkinter import messagebox
import datetime
import PIL.Image, PIL.ImageTk
from license_plate_DB import my_sql_server_DB
from load_logo import ImageLabel
from manual_check import Manual_check
from show_database import show_DB
from utils import snapshot, save_image_license, save_image_background, msg_future_feature, resize_text_in_canvas
from license_plate import predict
import sys


server = 'DESKTOP-HANN\SQLEXPRESS'  # change your server, database, username, password database and your driver ODBC
database = 'License_Plate_DB'
username = 'hieu'
password = 'hieunguyen123'
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;Encrypt=no;'

class make_gui_btn():
    
    def __init__(self, window, row, column, columnspan, cam1, cam2, frame1, frame2):
        
        self.window = window
        self.Cam1 = cam1
        self.Cam2 = cam2
        
        self.IN_frame = frame1
        self.OUT_frame = frame2
        self.IS_quick_view = False
        self.my_DB = my_sql_server_DB(connection_string, 3, 5)
        
        self.make_GUI_bottom_btn(row= row, column= column, columnspan= columnspan)
        self.make_GUI_right_btn(row= 0, column= 2, columnspan= 1, rowspan = 2)

    def make_GUI_bottom_btn(self, row, column, columnspan):
         
        self.frame_button_bottom = self.make_frame_in_row(self.window, row= row, column= column, columnspan= columnspan, rowspan = 1)
        
        self.btn_Find = self.create_btn(self.frame_button_bottom, finDB, self.open_Database)
        self.btn_Redo = self.create_btn(self.frame_button_bottom, text=redo, function=self.get_license)
        self.btn_manual = self.create_btn(self.frame_button_bottom, text="sau nay", function=msg_future_feature)
        logo = ImageLabel(self.frame_button_bottom)
        logo.pack(anchor='center', side='left', fill='both')
        logo.load("image/img_src/VN.gif")
        self.btn_snapshot = self.create_btn(self.frame_button_bottom, text=btn_snapshort, function=self.snapshot_new)
        self.btn_Source = self.create_btn(self.frame_button_bottom, text=source, function=msg_future_feature)
        self.btn_manual = self.create_btn(self.frame_button_bottom, text=manual_check, function=self.manual_check)
                
    def make_frame_in_row (self, window, row = 2, column= 0, columnspan = 3, rowspan = 1):
        # Tạo frame chứa các nút bấm
        frame= tkinter.Frame(window, bg=gray_color, border=5)
        frame.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=tkinter.NSEW)
        return frame
             
    def make_GUI_right_btn(self, row, column, columnspan, rowspan):
        
        self.right_button_frame = self.make_frame_in_row(self.window, row= row, column= column, columnspan= columnspan, rowspan= rowspan)
        # Frame chứa thông tin làn
        infor_lane= tkinter.Frame(self.right_button_frame, width=200, height=100, bg ="#784212")
        infor_lane.pack(fill=tkinter.BOTH,pady=(0,5), expand=True)
        
        # hiển thị tên làn
        self.info_lane1 = tkinter.Label(infor_lane, text=sys_lane1)
        self.info_lane1.pack(side="top", fill=tkinter.BOTH)
        
        # Bấm nút để thay đổi chế độ vào ra của làn
        self.isIN = True
        self.btn_swap_text = tkinter.StringVar()
        self.btn_swap = tkinter.Button(infor_lane, bg=tomato_color, activebackground=tomato_color , cursor="hand2",
                                       textvariable=self.btn_swap_text, command= lambda: self.swap_mode_lane(cam1=self.Cam1, cam2= self.Cam2))
        self.btn_swap_text.set(swap_lane_IN)
        self.btn_swap.pack( padx=10, pady= 10)
        
        # Hiển thị thông tin các phương tiện đang có
        self.info_vehicle = tkinter.Label(infor_lane, text=sys_vehicle, pady=5)
        self.info_vehicle.pack(fill=tkinter.BOTH)
        
        self.vehicle_frame= tkinter.Frame(infor_lane, background="#784212", pady=5)
        self.vehicle_frame.pack(fill="both")
        self.vehicle_frame.grid_columnconfigure((0,1), weight=1,uniform=1)
        self.vehicle_frame.grid_rowconfigure(0, weight=1, uniform=1)
        
        # Bấm nút để mở cửa sổ chế độ xem
        self.btn_quick_view = tkinter.Button(infor_lane, text=open_new_window, cursor="hand2", command= self.quick_view )
        self.btn_quick_view.pack( padx=10, pady= 10)
        
        # Xe máy
        self.number_moto = 0
        self.motobike= tkinter.Label(self.vehicle_frame, text=sys_motorbike)
        self.motobike.grid(row=0, column=0,sticky="nsew")
        self.moto_count_var = tkinter.StringVar()
        self.moto_count= tkinter.Label(self.vehicle_frame, textvariable=self.moto_count_var, background="#C1CDCD")
        self.moto_count.grid(row=0, column=1,sticky="nsew")
        self.moto_count_var.set(self.number_moto)
        
        # Xe đạp
        self.number_cycle = 0
        self.cycle= tkinter.Label(self.vehicle_frame, text=sys_bike)
        self.cycle.grid(row=1, column=0,sticky="nsew")
        self.cycle_count_var = tkinter.StringVar()
        self.cycle_count= tkinter.Label(self.vehicle_frame, textvariable=self.cycle_count_var,background="#98F5FF")
        self.cycle_count.grid(row=1, column=1,sticky="nsew")
        self.cycle_count_var.set(self.number_cycle)
        
        # Bấm nút để ...
        self.btn_new = tkinter.Button(infor_lane, text=sys_new, cursor="hand2", command=msg_future_feature)
        self.btn_new.pack( padx=10, pady= 10)
        
        # Bấm nút để 
        self.btn_new = tkinter.Button(infor_lane, text=sys_new, cursor="hand2",  command=msg_future_feature)
        self.btn_new.pack( padx=10, pady= 10)
        
        # Frame chứa kết quả so sánh
        result_frame= tkinter.Frame(self.right_button_frame, bg ="#154360")
        result_frame.pack(fill=tkinter.BOTH, pady=(0,5))
        
        # hiển thị tên 
        self.result_label = tkinter.Label(result_frame, text=sys_result)  # Hiển thị tên của frame đang phát camera, ví dụ "IP_Cam1"
        self.result_label.pack(side="bottom", fill=tkinter.BOTH)
        

        self.result_canvas= tkinter.Canvas(result_frame, background="#784212")
        self.text_result_canvas = self.result_canvas.create_text(30, 100, anchor="nw", text=sys_pass, fill="black", font="Helvetica 20 bold")
        self.result_canvas.pack(fill=tkinter.BOTH)
        self.result_canvas.bind("<Configure>", lambda event:resize_text_in_canvas(event,canvas_store_text= self.result_canvas,text_id= self.text_result_canvas, fontsize=20))
    
    # Tạo 1 nút bấm và gán nó cho hàm           
    def create_btn (self, frame, text, function):
        # Bấm nút để mở CSDL và tìm kiếm
        self.btn = tkinter.Button(frame, text=text, cursor="hand2", command=function)
        self.btn.pack(anchor='center', side='left', expand=True , padx=5, pady= 5)   
        
    # Bấm nút để thay đổi chế độ ra vào
    def swap_mode_lane(self, cam1, cam2):

        if self.isIN :
            respond1 = self.msg_ask(toast_swap_in_to_out)
            if respond1:
                cam1.canvas, cam2.canvas = cam2.canvas, cam1.canvas  
                self.btn_swap_text.set(swap_lane_OUT)
                self.btn_swap.config(bg=powder_blue_color, activebackground=powder_blue_color)
                self.isIN = False
        else:
            respond2 = self.msg_ask(toast_swap_out_to_in)
            if respond2:
                cam2.canvas, cam1.canvas = cam1.canvas, cam2.canvas 
                # Cam2, Cam1 = Cam1, Cam2
                self.btn_swap.config(bg=tomato_color, activebackground=tomato_color)
                self.btn_swap_text.set(swap_lane_IN)
                self.isIN = True
                
    def msg_ask (self, mess):
        self.respond = messagebox.askokcancel('Lưu Ý',"Bạn có chắc chắn {}".format(mess)) # Nhận về True hoặc fail
        return self.respond
    
    # Bấm nút để chụp ảnh từ tất cả camera
    def snapshot_new (self):
        back_frame= self.Cam1.origin_frame()
        license_frame = self.Cam2.origin_frame()
        if self.isIN:
            snapshot(filename= None, frame= back_frame, text="background_cam")
            snapshot(filename= None, frame= license_frame, text="license_plate_cam")
        else:
            snapshot(filename= None, frame= license_frame, text="background_cam")
            snapshot(filename= None, frame= back_frame, text="license_plate_cam")
    
    # Khi quẹt thẻ vào thành công        
    def setup_IN_success (self):
        
        # Canvas chứa kết quả so sánh
        self.result_canvas.configure(bg=terumo_color)
        self.result_canvas.itemconfig(self.text_result_canvas, text=sys_success) 
        self.number_moto +=1
        self.moto_count_var.set(self.number_moto)  
        
        # Hiển thị lên chế độ xem nhanh
        if self.IS_quick_view:
            self.quick_view.IN_success(self.now, self.id_card, self.license_plate)
        
        # Label chứa thời gian vào, id lúc vào, mã nhân viên, họ tên nhân viên
        self.IN_frame.Time_label_IN.config( text=self.today)
        self.IN_frame.ID_label_IN.config( text= self.id_card)
        
        # Canvas chứa text và hình ảnh biển số
        width = self.IN_frame.image_license_plate_canvas_IN.winfo_width() # lấy chiều cao chiều rộng của canvas
        height= self.IN_frame.image_license_plate_canvas_IN.winfo_height() 
        
        resized_image= self.license_plate_crop.resize((width,height), PIL.Image.Resampling.LANCZOS) # resize hình ảnh biển số phù hợp với 
        self.photo_IN = PIL.ImageTk.PhotoImage(image=resized_image)                                 # kích thước của canvas
        
        self.IN_frame.image_license_plate_canvas_IN.itemconfig(self.IN_frame.image_on_canvas_IN, image=self.photo_IN)
        self.IN_frame.text_license_plate_canvas_IN.itemconfig(self.IN_frame.text_on_canvas_IN, text=self.license_plate)
        
        # Ghi dữ liệu vào CSDL
        in_background= save_image_background(success=True, frame= self.Cam1.origin_frame())
        in_license = save_image_license(success= True, frame=self.Cam2.origin_frame())
        self.my_DB.info_insert_IN_onetime(self.id_card, self.now, self.license_plate, status="IN",result= "OK", lane=1, time_out= 0,
                                          in_background= in_background, in_license = in_license, in_license_plate = self.license_plate_path)
    
    # Lấy thông tin lúc vào để đưa lên màn hình     
    def get_info_IN_success(self):
        
        # Lấy data từ CSDL về lần vào gần nhất
        id_card, time_in, license_plate, license_plate_path = self.my_DB.get_info_IN(self.id_card)
        # Label chứa thời gian vào, id lúc vào, mã nhân viên, họ tên nhân viên
        self.IN_frame.Time_label_IN.config( text=time_in)
        self.IN_frame.ID_label_IN.config( text= id_card)
        # Canvas chứa text và hình ảnh biển số
        width = self.IN_frame.image_license_plate_canvas_IN.winfo_width() # lấy chiều cao chiều rộng của canvas
        height= self.IN_frame.image_license_plate_canvas_IN.winfo_height() 
        
        resized_image = PIL.Image.open(license_plate_path)
        resized_image= resized_image.resize((width,height), PIL.Image.Resampling.LANCZOS) # resize hình ảnh biển số phù hợp với 
        self.photo_IN = PIL.ImageTk.PhotoImage(image=resized_image)                                 # kích thước của canvas
        
        self.IN_frame.image_license_plate_canvas_IN.itemconfig(self.IN_frame.image_on_canvas_IN, image=self.photo_IN)
        self.IN_frame.text_license_plate_canvas_IN.itemconfig(self.IN_frame.text_on_canvas_IN, text=license_plate)
    
    # Khi quẹt thẻ vào thất bại
    def setup_IN_fail (self):
        
        # Canvas chứa kết quả so sánh
        self.result_canvas.configure(bg=red_color)
        self.result_canvas.itemconfig(self.text_result_canvas, text=toast_do_again)
        
        # Label chứa thời gian vào, id lúc vào, mã nhân viên, họ tên nhân viên
        self.IN_frame.Time_label_IN.config( text=self.today)
        self.IN_frame.ID_label_IN.config( text= self.id_card)
        
        # Canvas chứa text và hình ảnh biển số lỗi
        width = self.IN_frame.image_license_plate_canvas_IN.winfo_width() # lấy chiều cao chiều rộng của canvas
        height= self.IN_frame.image_license_plate_canvas_IN.winfo_height() 
        
        resized_image= self.license_plate_crop.resize((width,height), PIL.Image.Resampling.LANCZOS) # resize hình ảnh biển số phù hợp với 
        self.photo_IN = PIL.ImageTk.PhotoImage(image=resized_image)                                 # kích thước của canvas
        
        self.IN_frame.image_license_plate_canvas_IN.itemconfig(self.IN_frame.image_on_canvas_IN, image=self.photo_IN)  # ảnh hiển thị lỗi
        self.IN_frame.text_license_plate_canvas_IN.itemconfig(self.IN_frame.text_on_canvas_IN, text=self.license_plate) # text : Không đọc được biển số
        
        # Ghi dữ liệu vào CSDL
        in_background= save_image_background(success=False, frame= self.Cam1.origin_frame())
        #print("in_background", in_background)
        in_license = save_image_license(success= False, frame=self.Cam2.origin_frame())
        self.my_DB.info_insert(self.id_card, self.now, self.license_plate, status='IN', result='REFUSE',lane=1, time_out=0,
                               in_background=in_background, in_license= in_license, in_license_plate=self.license_plate_path) 
    
    # Khi quẹt hẻ ra thành công
    def setup_OUT_success(self):
        
        # Label chứa thời gian, id card, mã nhân viên, họ tên lúc ra
        self.OUT_frame.Time_label_OUT.config( text=self.today)
        self.OUT_frame.ID_label_OUT.config( text= self.id_card)
        
        # Canvas chứa text và hình ảnh biển số
        width = self.OUT_frame.image_license_plate_canvas_OUT.winfo_width() # lấy chiều cao chiều rộng của canvas
        height= self.OUT_frame.image_license_plate_canvas_OUT.winfo_height() 
        
        resized_image= self.license_plate_crop.resize((width,height), PIL.Image.Resampling.LANCZOS) # resize hình ảnh biển số phù hợp với 
        self.photo_OUT = PIL.ImageTk.PhotoImage(image=resized_image)                                 # kích thước của canvas
        
        self.OUT_frame.image_license_plate_canvas_OUT.itemconfig(self.OUT_frame.image_on_canvas_OUT, image=self.photo_OUT)
        
        self.OUT_frame.text_license_plate_canvas_OUT.itemconfig(self.OUT_frame.text_on_canvas_OUT, text=self.license_plate)
        
        # Lấy dữ liệu lúc vào và so sánh (đi vào, thời gian gần đây nhất, tình trạng là IN, chưa IN/DONE, và hợp lệ )
        reults_compare, mess = self.my_DB.select_and_compare(self.id_card, self.license_plate) # True hoặc false
        
        if reults_compare:
            out_background= save_image_background(success=True, frame= self.Cam2.origin_frame())
            out_license = save_image_license(success= True, frame=self.Cam1.origin_frame())
            # Cập nhật trạng thái của dữ liệu từ IN thành IN/DONE, lấy dữ liệu lúc so sánh và cập nhật status
            self.my_DB.update_DB_OUT(time_out=self.now, id_card=self.id_card, out_background=out_background, out_license=out_license, out_license_plate=self.license_plate_path)
            
            # Hiển thị lên canvas kết quả
            self.result_canvas.configure(bg=terumo_color)
            self.result_canvas.itemconfig(self.text_result_canvas, text=mess) 
            self.number_moto -=1 
            self.moto_count_var.set(self.number_moto)
            
            # Hiển thị thông tin lúc đi vào trên frame "thông tin lúc vào"
            self.get_info_IN_success()
        else:
            # Ghi dữ liệu lỗi vào CSDL
            out_background= save_image_background(success=False, frame= self.Cam2.origin_frame())
            out_license = save_image_license(success= False, frame=self.Cam1.origin_frame())
            self.my_DB.info_insert(self.id_card, time_in=0, license_plate=self.license_plate, status='OUT', result='REFUSE', lane=1,
                                   time_out=self.now, out_background=out_background, out_license=out_license, out_license_plate=self.license_plate_path)
            
            self.result_canvas.configure(bg=red_color)
            self.result_canvas.itemconfig(self.text_result_canvas, text=mess)
    
    # Khi quẹt thẻ ra thất bại
    def setup_OUT_fail(self):
        # Canvas chứa kết quả so sánh
        self.result_canvas.configure(bg=red_color)
        self.result_canvas.itemconfig(self.text_result_canvas, text="Quẹt thẻ lại") 
        
        # Label chứa thời gian vào, id lúc vào, mã nhân viên, họ tên nhân viên
        self.OUT_frame.Time_label_OUT.config( text=self.today)
        self.OUT_frame.ID_label_OUT.config( text= self.id_card)
        
        # Canvas chứa text và hình ảnh biển số lỗi
        width = self.OUT_frame.image_license_plate_canvas_OUT.winfo_width()
        height= self.OUT_frame.image_license_plate_canvas_OUT.winfo_height() 
        
        resized_image= self.license_plate_crop.resize((width,height), PIL.Image.Resampling.LANCZOS)
        self.photo_OUT = PIL.ImageTk.PhotoImage(image=resized_image)
        
        self.OUT_frame.image_license_plate_canvas_OUT.itemconfig(self.OUT_frame.image_on_canvas_OUT, image=self.photo_OUT)
        self.OUT_frame.text_license_plate_canvas_OUT.itemconfig(self.OUT_frame.text_on_canvas_OUT, text=self.license_plate_path)
        
        # Ghi dữ liệu vào CSDL
        out_background= save_image_background(success=False, frame= self.Cam2.origin_frame())
        out_license = save_image_license(success= False, frame=self.Cam1.origin_frame())
        
        self.my_DB.info_insert(self.id_card, time_in=0, license_plate= self.license_plate, status='OUT', result='REFUSE', lane=1,
                               time_out=self.now, out_background=out_background, out_license=out_license, out_license_plate=self.license_plate_path) 
    
    # Button khi nhấn nút quẹt thẻ  
    def get_license(self):
        self.now = datetime.datetime.now()
        self.today = str(self.now.strftime("%Y-%m-%d %H:%M:%S"))
        self.id_card = 123456
        
        # Nếu là đi vào
        if self.isIN:
            
            image_get_license = self.Cam2.origin_frame()
            self.license_plate, self.license_plate_crop, self.success, self.license_plate_path = predict(image= image_get_license, save= True)

            if (self.success):
                self.setup_IN_success()
            else:
                self.setup_IN_fail()
        # Nếu là đi ra     
        else:
            image_get_license = self.Cam1.origin_frame()
            self.license_plate, self.license_plate_crop, self.success, self.license_plate_path = predict(image= image_get_license, save= True)
            if (self.success):
                self.setup_OUT_success()
            else:
                self.setup_OUT_fail()  
                
    # Mở chế độ xem nhanh
    def quick_view(self):
        self.IS_quick_view = True
        self.quick_view = self.Cam2.open_new_window(self.IS_quick_view)     
     
    # Kiểm tra thủ công
    def manual_check(self):
        manual_check_window =  Manual_check(self.Cam1, self.Cam2, self.isIN, self.my_DB)         
        
    # mở cửa sổ CSDL
    def open_Database(self):
        showDB =  show_DB(self.my_DB) 
                
