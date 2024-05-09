
from tkinter import ttk
import tkinter as tk
from VN_language import *
from utils import make_entry_gui, Validation_int, Validation_str

class show_DB():
    def __init__(self, mydb):
        
        self.window = tk.Toplevel()
        self.window.title("Cơ sở dữ liệu")
        self.window.geometry("1500x800")
        style = ttk.Style()
        style.theme_use("default")
        #style.map("Treeview")
        
        # Cấu hình window theo dạng lưới (3x3)
        self.window.columnconfigure((0),weight=1, uniform="a")
        self.window.rowconfigure((0),weight=1, uniform="a")
        self.window.rowconfigure(1,weight=5, uniform="a")
        
        self.database_frame = tk.Frame(self.window)
        self.search_frame = tk.Frame(self.window)
        self.database_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=20, pady=10)
        self.search_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=20, pady=10)

        self.tv_DB = self.crete_TV()
        self.search_gui = self.search_DB()
        search_btn = tk.Button(self.search_gui, text=sys_search, cursor="hand2", command= self.search_CSDL)
        search_btn.grid(row=0, column=4, padx=5, pady= 5)
        refresh_btn = tk.Button(self.search_gui, text=sys_refresh, cursor="hand2", command= lambda: self.refresh(1))
        refresh_btn.grid(row=1, column=4, padx=5, pady= 5)
        
        self.entry_id_search = make_entry_gui(self.search_gui, 0, 0, sys_id_card, "VD: 123456")
        self.entry_id_search['validatecommand'] = (self.entry_id_search.register(Validation_int),'%P','%d')
        self.entry_id_search.bind("<FocusIn>", lambda args: self.entry_id_search.delete('0', 'end'))
        
        self.entry_license_search = make_entry_gui(self.search_gui, 1, 0, sys_license_plate, "VD: 38-F7390.01")
        self.entry_license_search.bind("<FocusIn>", lambda args: self.entry_license_search.delete('0', 'end'))
        
        self.entry_result = make_entry_gui(self.search_gui, 0, 2, sys_result, "VD: OK hoặc REFUSE")
        self.entry_result.bind("<FocusIn>", lambda args: self.entry_result.delete('0', 'end'))
        self.entry_result['validatecommand'] = (self.entry_result.register(Validation_str),'%P','%d')
        
        self.entry_id_employ_search = make_entry_gui(self.search_gui, 1, 2, sys_employ_id, "chưa khả dụng ")
        self.entry_id_employ_search.bind("<FocusIn>", lambda args: self.entry_id_employ_search.delete('0', 'end'))
        self.entry_id_employ_search['validatecommand'] = (self.entry_id_employ_search.register(Validation_int),'%P','%d')
        # DB
        self.myDB = mydb
        self.data = self.myDB.select_120_row()
        self.refresh(data=self.data)

    # Tạo mục tìm kiếm
    def search_DB(self):
        wrapper2 =  tk.LabelFrame(self.search_frame, text="Tìm kiếm")
        wrapper2.pack()
        wrapper2.columnconfigure((0,2,4),weight=1, uniform="a")
        wrapper2.columnconfigure((1,3),weight=3, uniform="a")
        wrapper2.rowconfigure(0,weight=1, uniform="a")
        
        return wrapper2
    
    # Từ khóa tìm kiếm
    def search_list(self, window, row, column, text1, text2):
        # Label chứa thời gian vào
        label = tk.Label(self.left_frame, background="#784212", padx=2, pady=5, font = "bold", fg = "white", text=text1)  
        label.grid(row=row, column=column, sticky=tk.NSEW )
        
        entry = tk.Entry(self.left_frame, bd=5, font=("Arial",15), fg="white", bg="#784212", justify="left", width=30)
        entry.insert(0,text2)
        entry.grid(row=row, column=column+1, sticky=tk.NSEW )
        return entry
        
    # Tạo TreeView
    def crete_TV(self):
        self.wrapper1 =  tk.LabelFrame(self.database_frame, text="Cơ sở dữ liệu")
        self.wrapper1.pack()
        trv = ttk.Treeview(self.wrapper1, columns=(1,2,3,4,5,6,7), show="headings", height="30")
        trv.pack(side="left")
        #naming headings
        trv.heading(1, text="Mã thẻ")
        trv.heading(2, text="Thời gian vào")
        trv.heading(3, text="Biển số xe")
        trv.heading(4, text="Trạng thái")
        trv.heading(5, text="Kết quả")
        trv.heading(6, text="Làn")
        trv.heading(7, text="Thời gian ra")
        
        scrollbar = tk.Scrollbar(self.wrapper1, orient=tk.VERTICAL)
        scrollbar.pack(side="right", fill="y")
        trv.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=trv.yview)
        return trv
        
    # Khi click vào 1 hàng nào đó thì nó sẽ có trạng thái đang focus, và dữ liệu của hàng được lưu vào biến temp    
    def select_row(self, tv_db):
        selected = tv_db.focus()
        temp = tv_db.item(selected, 'values')
        # thay đổi giá trị và lưu vào 1 biến 
        sal_up = float(temp[2]) + float(temp[2]) * 0.05
        # Gán lại thông tin của biến vào giá trị theo thứ tự
        tv_db.item(selected, values=(temp[0], temp[1], sal_up))
        
    # Cập nhật CSDL
    def refresh (self, data):
        # Xóa toàn bộ các hàng trong treeview
        self.tv_DB.delete(*self.tv_DB.get_children())
        if (data == 1):
            data = self.myDB.select_120_row()
        for i in range(119): 
            self.tv_DB.insert(parent='', index="end", iid=i, text='', values=(data[i][0], data[i][1],data[i][2],data[i][3], data[i][4], data[i][5], data[i][6]))

    # Tìm kiếm CSDL
    def search_CSDL (self):
        id_card = self.entry_id_search.get()  
        id_card = int(id_card)       
        license_plate = self.entry_license_search.get()
        result = self.entry_result.get()
        employ_id = self.entry_id_employ_search.get()
        data = self.myDB.search_db(id_card, license_plate, result)
        self.refresh(data=data)
if __name__ == "__main__":
    window = tk.Tk()
    show_DB(window)
    window.mainloop()