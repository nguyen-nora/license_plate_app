from paddleocr import PaddleOCR
from ultralytics import YOLO
import string
from PIL import Image
from VN_language import error_no_license_plate, error_read_license_plate, error_format_license_plate,error_format_license_plate_9\
                        ,error_format_license_plate_11, dict_int_to_char,dict_char_to_int, dict_two
from utils import save_image_license_plate
import os


# It took a long time for this run
license_plate_detect= YOLO("best.pt")
# ocr = PaddleOCR(use_angle_cls=True, lang='en', det=False, ret= False, show_log=False, save_crop_res=False, crop_res_save_dir='./output') # need to run only once to download and load model into memory
ROOT = os.path.dirname(__file__)

rec_model_dir=os.path.join(ROOT, "model", "rec"),
det_model_dir=os.path.join(ROOT, "model", "det"),
cls_model_dir=os.path.join(ROOT, "model", "cls")

ocrEngine = PaddleOCR(
            use_angle_cls=False,
            lang='en',
            show_log=False,
            use_gpu=False,
            rec_model_dir=os.path.join(ROOT, "model", "rec"), # use in here
            det_model_dir=os.path.join(ROOT, "model", "det"), # use in here
            cls_model_dir=os.path.join(ROOT, "model", "cls") # use in here
        )

def license_complies_format(license_plate):

    license_plate_size= len(license_plate)
    # dinh dang bien so VN cu la 9 so, moi la 11 so (bao gom dau gach ngang va dau cham o bien moi)
    # example: 38-F7 3901

    if (license_plate_size != 9) and (license_plate_size != 11) and (license_plate_size != 12):
        # print(error_format_license_plate, license_plate)
        return False, license_plate
    
    if license_plate_size == 9:
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-']) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[7] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[8] in dict_int_to_char.keys()):
            
            license_plate_= license_plate_format(license_plate,license_plate_size)
            return True, license_plate_
        else:
            # print(error_format_license_plate_9, license_plate)
            return False, license_plate
    
    if license_plate_size == 11: 
        # example: 38-F7 390.11
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-']) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[7] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['.']) and \
        (license_plate[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[9] in dict_int_to_char.keys()) and \
        (license_plate[10] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[10] in dict_int_to_char.keys()):
            
            license_plate_=license_plate_format(license_plate,license_plate_size)
            return True, license_plate_

        # example: 38-FA 390.11
        if (license_plate[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[0] in dict_int_to_char.keys()) and \
        (license_plate[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[1] in dict_int_to_char.keys()) and \
        (license_plate[2] in ['-']) and \
        (license_plate[3] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[4] in string.ascii_uppercase or license_plate[3] in dict_char_to_int.keys()) and \
        (license_plate[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[4] in dict_int_to_char.keys()) and \
        (license_plate[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[5] in dict_int_to_char.keys()) and \
        (license_plate[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[6] in dict_int_to_char.keys()) and \
        (license_plate[8] in ['.']) and \
        (license_plate[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[9] in dict_int_to_char.keys()) and \
        (license_plate[10] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or license_plate[10] in dict_int_to_char.keys()):
            
            license_plate_=license_plate_format(license_plate,license_plate_size)
            return True, license_plate_
        
    else:
        # print(error_format_license_plate_11, license_plate)
        return False, license_plate


def license_plate_format(license_plate, license_plate_size):
    license_plate_ = ''

    #38-F7 3901
    mapping_9 = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char
               , 7: dict_int_to_char, 8: dict_int_to_char}

    #38-F7 390.01
    mapping_11 = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char
               , 7: dict_int_to_char, 8: dict_two, 9: dict_int_to_char, 10: dict_int_to_char}
    
    #38-FA 390.01
    mapping_11_new = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_two, 3: dict_char_to_int, 4: dict_char_to_int, 5: dict_int_to_char, 6: dict_int_to_char
                , 7: dict_int_to_char, 8: dict_two, 9: dict_int_to_char, 10: dict_int_to_char}
    
    mapping=[0,0,0,0,0,0,0,0,0,mapping_9,0,mapping_11,mapping_11_new]

    for j in range(license_plate_size):
        if license_plate[j] in mapping[license_plate_size][j].keys():
            license_plate_ += mapping[license_plate_size][j][license_plate[j]]
        else:
            license_plate_ += license_plate[j]
    return license_plate_


def get_license_plate(license_plate_crop):

    is_license_plate= False
    result_license_plate= ocrEngine.ocr(license_plate_crop, cls=True)[0]
    
    license_plate_crop_cvt = Image.fromarray(license_plate_crop)
    
    if result_license_plate:
        license_plate = [line[1][0] for line in result_license_plate]

        license_plate = [i.upper() for i in license_plate]
        license_plate =''.join(license_plate) # bỏ các khoảng trắng
        is_license_plate, license_plate=license_complies_format(license_plate)
    else:
        license_plate='000000000'

    return is_license_plate, license_plate_crop_cvt, license_plate

def predict(image, save=False):
    
    is_license_plate= False   #default
    license_plate = error_no_license_plate   #default
    license_plate_crop_cvt= Image.open("image\img_src\error.png")   #default
    img_path = None    #default
    
    # phát hiện khu vực có biển số
    results = license_plate_detect(image)[0]
    if results:
        # Trích xuất vị trí bounding box
        boxes = results.boxes.xyxy.tolist()
        
        for i, box in enumerate(boxes):
            # lấy tọa độ (x1,y1) trên cùng bên trái và (x2,y2) cuối cùng bên phải
            x1, y1, x2, y2 = box
            # Cắt khu vực chứa biển số để đưa vào paddleocr
            license_plate_crop = image[int(y1):int(y2), int(x1):int(x2)]
            is_license_plate, license_plate_crop_cvt, license_plate = get_license_plate(license_plate_crop)
            #lưu và hiển thị ảnh lên màn hình
            if save:
                img_path = save_image_license_plate(is_license_plate,license_plate_crop, license_plate)
    return license_plate, license_plate_crop_cvt, is_license_plate, img_path


if __name__== "__main__":
    #path= "results/16-01-24/15-B1567.89.jpg"
    path= "results/16-01-24/AIUIANAN6996.jpg"
    a,b,c=get_license_plate(path)
   