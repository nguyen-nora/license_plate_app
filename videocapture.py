import time
import threading
import cv2
import PIL.Image
from VN_language import *

# Đọc từng frame từ camera
class VideoCapture:

    def __init__(self, video_source, width=None, height=None):
        """TODO: add docstring"""

        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = 0

        # Cài đặt trạng thái hoạt động
        self.running = False

        # Đọc frame và lấy các thông số chiều rộng, chiều cao, fps
        self.vid = cv2.VideoCapture(video_source)
        
        if not self.vid.isOpened():
            print(cannot_connect_camera)
            self.vid.release()
            time.sleep(1)
            self.vid = cv2.VideoCapture(video_source)
            time.sleep(10)
            raise ValueError(error_read_frame, video_source)

        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))              # convert float to int

        # Khởi tạo giá trị mặc định cho frame
        self.ret = False
        self.frame = None

        self.convert_color = cv2.COLOR_BGR2RGB
        self.convert_pillow = True

        # Khởi tạo thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True
        self.thread.start()
        # print(threading.active_count())
        # print(threading.enumerate())

    # Thực hiện luồng stream
    def process(self):
        """TODO: add docstring"""
        while self.running:
            ret, frame = self.vid.read()
            self.origin_frame= frame
            
            if ret:
                # Hàm imshow phải dùng trong luồng chính, chạy trong thread sẽ gây ra các lỗi ko mong muốn
                # process image
                #frame = cv2.resize(frame, (self.width, self.height))

                if self.convert_pillow:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = PIL.Image.fromarray(frame)
            else:
                # print(toast_end_stream, self.video_source)
                self.running = False
                break

            # assign new frame
            self.ret = ret
            self.frame = frame

    def get_frame(self):
        return self.ret, self.frame
    
    def get_origin_frame(self):
        return self.ret, self.origin_frame

    # Giải phóng tài nguyên khi kết thúc ghi hình, hàm hủy sẽ được gọi trước khi đóng cửa sổ
    def __del__(self):
        # print(toast_end, self.video_source)
        # stop thread
        if self.running:
            self.running = False
            self.thread.join()
        # relase stream
        if self.vid.isOpened():
            self.vid.release()
            
            