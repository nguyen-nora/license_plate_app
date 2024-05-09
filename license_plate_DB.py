
import time
import pyodbc
from contextlib import contextmanager
import sys
import traceback
import pyodbc
from VN_language import *

server = 'DESKTOP-HANN\SQLEXPRESS'  # change your server, database, username, password database and your driver ODBC
database = 'License_Plate_DB'
username = 'hieu'
password = 'hieunguyen123'
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;Encrypt=no;'
class my_sql_server_DB():
    
    def __init__(self,connection_string, maxAttempts, waitBetweenAttemptsSeconds):
        
        self.connection_string = connection_string
        self.maxAttempts = maxAttempts
        self.waitBetweenAttemptsSeconds = waitBetweenAttemptsSeconds
        self.connect_to_DB()
    
    def connect_to_DB (self):
        for attemptNumber in range(self.maxAttempts):
            self.connection = None
            try:
                self.connection = pyodbc.connect(self.connection_string)
                self.cursor = self.connection.cursor()
            except Exception as e:
                #pass # nhớ edit lại, ghi log
                print(traceback.format_exc())
            finally:
                if self.connection:
                    print(connected_DB)
                    return True
                else:
                    
                    print(error_connect_DB + str(attemptNumber))
                time.sleep(self.waitBetweenAttemptsSeconds)
        print(not_connect_DB)
        return False

    def cleanup_before_exit(self):
        # Đảm bảo tất cả các kết nối đã được đóng trước khi chấm dứt
        self.connection.close()

    @contextmanager
    def open_db_connection(self, commit=False):
        # connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
        try:
            yield self.cursor # tương tự return nhưng nó sẽ lưu trữ các trạng thái của biến cục bộ
            # Thường đi kèm với hàm with, trả về cursor và tạm dừng ở đây để thực hiện các lệnh trong with trước
            # Sau khi kết thúc các lệnh trong with sẽ tiếp tục thực hiện các dòng mã bên dưới
            # Nếu không có lỗi thì sẽ commit (xác nhận các giao dịch thêm, sửa, xóa là hợp lệ và lưu vào CSDL)
            # Hoặc tự động rollback nếu không cài tham số commit = True
            if commit:
                self.cursor.execute("COMMIT")
            else:
                self.cursor.execute("ROLLBACK")
                # print(" câu lệnh không commit")
        except pyodbc.DatabaseError as err:
            
            # Nếu có ngoại lệ, lỗi, ... xảy ra trong khối lệnh with ngay lập tức rollback (quay trở lại) trước khi lệnh with chạy
            error= err.args[0]
            print("Lỗi: ", err)
            sys.stderr.write(str(error))
            self.cursor.execute("ROLLBACK") 
            print("đã rollback ở ngoại lệ")
            raise err

        finally:
            # Cuối cùng luôn đóng kết nối với CSDL
            self.cursor.close()
        
        
    # Thêm các thông tin vào CSDL, nếu đã có thông tin vào, nhân viên quẹt thẻ thêm lần nữa thì sẽ ghi đè dữu liệu cũ     
    def info_insert_IN_onetime(self,id_card, time_in, license_plate, status='IN', result='OK', lane=1, time_out=0, in_background= None, in_license = None, in_license_plate = None):
        # Dấu mở ngoặc của exists hay update bắt buộc phải nằm 1 hàng riêng biệt
        info_insert_IN_onetime_quert = """
        IF EXISTS (
            SELECT ID_Card FROM License_Plate
            WHERE ID_Card = ? AND Status = 'IN' AND Result = 'OK'
        )
        BEGIN
            UPDATE License_Plate
            SET Time_IN = ?, License_Plate_Number = ?, Result = ?, Lane = ?, IN_Background = ?, IN_License = ?, IN_License_Plate = ?
            WHERE Time_IN = (
                SELECT TOP (1) Time_IN
                FROM License_Plate
                WHERE ID_Card = ? AND Status = 'IN' AND Result = 'OK'
            )
        END
        ELSE
        BEGIN
            INSERT INTO License_Plate 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        END
    """
        #insert_in_string = "insert into License_Plate values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        with self.open_db_connection(True) as cursor:
            cursor.execute(info_insert_IN_onetime_quert, id_card, time_in, license_plate, result, lane, in_background, in_license,
                           in_license_plate, id_card, id_card,time_in, license_plate, status, result, lane, time_out, in_background, in_license,
                           in_license_plate, None, None, None)
            #cursor.commit()

    # Thêm thông tin vào csdl, cho phép thêm dữ liệu trùng nhau, chỉ khác nhau về thời gian
    def info_insert (self,id_card, time_in, license_plate, status='IN', result='OK', lane=1, time_out=0, in_background= None,
                     in_license = None, in_license_plate = None, out_background= None, out_license = None, out_license_plate = None):
        info_insert_query = "insert into License_Plate values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        with self.open_db_connection(True) as cursor:
            cursor.execute(info_insert_query, id_card, time_in, license_plate, status, result, lane, time_out, in_background,
                            in_license, in_license_plate, out_background, out_license, out_license_plate)

    # Lấy dữ liệu ra và so sánh
    def select_and_compare (self,id_card, license_plate):
        select_and_compare_query = "select top (1) License_Plate_Number from License_Plate where ID_Card = ? and status = 'IN' and Result = 'OK' order by Time_IN desc"
        with self.open_db_connection() as cursor:
            cursor.execute(select_and_compare_query,id_card)
            data = cursor.fetchone() # lấy 1 hàng dữ liệu, gọi thêm 1 lần nữa là lấy hàng tiếp theo, fetchall là lấy hết các hàng dữ liệu
            
            if data == None:
                mess = "Chưa có thông tin lúc vào"
                # print("Chưa có thông tin lúc vào")
                return False, mess
            if data[0] == license_plate :
                mess = "Dữ liệu khớp"
                return True, mess
            else:
                mess = "Dữ liệu không khớp"
                return False, mess
    
    
    # Cập nhật dữ liệu khi đã đi ra thành công
    def update_DB_OUT(self,id_card, time_out, out_background, out_license, out_license_plate):
        update_DB_OUT_query = "UPDATE License_Plate \
                        SET Status='IN/DONE', Time_OUT = ?, OUT_Background = ?, OUT_License = ?, OUT_License_Plate = ? \
                        WHERE Time_IN =  (SELECT TOP (1) Time_IN \
							FROM License_Plate \
							WHERE ID_Card=? \
							ORDER BY Time_IN DESC);"
        with self.open_db_connection(commit= True) as cursor:
            cursor.execute(update_DB_OUT_query, time_out, out_background, out_license, out_license_plate, id_card)
     
    def get_info_IN (self, id_card):
        get_info_IN_query = "select top (1) ID_Card, Time_IN, License_Plate_Number, IN_License_Plate from License_plate where ID_Card = ? and status = 'IN/DONE' order by Time_IN desc" 
        with self.open_db_connection() as cursor:
            cursor.execute(get_info_IN_query, id_card)
            data = cursor.fetchone() # lấy 1 hàng dữ liệu, gọi thêm 1 lần nữa là lấy hàng tiếp theo, fetchall là lấy hết các hàng dữ liệu
            id_card = data[0]
            time_in = data[1]
            license_plate = data[2]
            IN_License_Plate = data[3]
            # print(data)
        return id_card, time_in, license_plate, IN_License_Plate
        
    
    # Kiểm tra xem người dùng quẹt thẻ vào nhiều lần thì xóa dữ liệu cũ hoặc chặn 
    def check_In_twice ():
        check_In_twice = "UPDATE License_Plate\
                            SET ID_Card= 'Kumari'\
                            WHERE EXISTS (SELECT *\
                                            FROM License_Plate\
                                            WHERE Status='IN')"
                                            
    # Lấy thông tin để hiển thị
    def select_120_row(self):
        select_120_row_query = "select top (120) ID_Card, Time_IN, License_Plate_Number, Status, Result, Lane, Time_OUT from License_plate \
                                        ORDER BY \
                                        CASE \
                                        WHEN Time_IN >= Time_OUT THEN Time_IN\
                                        ELSE Time_OUT\
                                        END DESC;" 
        with self.open_db_connection() as cursor:
            cursor.execute(select_120_row_query)
            data = cursor.fetchall() # lấy 1 hàng dữ liệu, gọi thêm 1 lần nữa là lấy hàng tiếp theo, fetchall là lấy hết các hàng dữ liệu
        return data
    
    def search_db(self, id_card, license_plate, result):
        search_120_row_query = "select top (120) ID_Card, Time_IN, License_Plate_Number, Status, Result, Lane, Time_OUT from License_plate \
                                WHERE (ID_Card = ?)\
                                    OR (ID_Card = ? AND License_Plate_Number = ?)\
                                        OR (ID_Card = ? AND License_Plate_Number = ? AND Result = ?)\
                                            OR (License_Plate_Number = ?)\
                                                OR (Result = ?)\
                                                    OR (License_Plate_Number = ? AND Result = ?)\
                                                        OR (ID_Card = ? AND Result = ?)\
                                ORDER BY \
                                CASE \
                                WHEN Time_IN >= Time_OUT THEN Time_IN\
                                ELSE Time_OUT\
                                END DESC;"
        with self.open_db_connection() as cursor:
            cursor.execute(search_120_row_query, id_card, id_card, license_plate, id_card, license_plate, result, license_plate, result,
                           license_plate, result, id_card, result)
            data = cursor.fetchall() # lấy 1 hàng dữ liệu, gọi thêm 1 lần nữa là lấy hàng tiếp theo, fetchall là lấy hết các hàng dữ liệu
        return data
    
    
if __name__ == "__main__":    

    
    id_card=167354
    
    now = datetime.datetime.now()
    time_in_str = now.strftime('%Y-%m-%d %H:%M:%S')
    license_plate = "63-B9999.99" #30-T7624.15
    isIN = "IN"
    success = "Hợp lệ"
    # print(time_in_str)
    # info_insert(id_card, now, license_plate, isIN, success)
    my_DB = my_sql_server_DB(connection_string, 3, 5)
    #print(my_DB.select_and_compare(111111, "30-A1567.89"))
    #my_DB.info_insert(id_card=167564, time_in= now, license_plate="30-A1567.89", status="IN",result= "OK")
    #my_DB.get_info_IN(146463)
    my_DB
    
    
    my_DB.cleanup_before_exit()
    