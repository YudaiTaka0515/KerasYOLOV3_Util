from Detect import *
from ThinOutDataset import *
from CalcIOU import *


ANNOTATION_PATH = "new_annotations.txt"
TRAIN_DIR = r"I:\3.Data\FaceDataset\KerasV3_1214_v2\train"


CLASSES = {"face": 0, "mouth": 1, "nose": 2}
COLOR = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255)}
# box : [top, left, bottom, right]


def evaluate_detection(annotation_path, yolo):
    f = open(ANNOTATION_PATH, 'r')
    lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i].split(' ')
        img_name = line[0]
        img_path = os.path.join(TRAIN_DIR, img_name)

        img = cv2.imread(img_path)

        detection_result, nose_box, mouth_box, face_box = yolo.detect(Image.fromarray(img))

        detection_result = np.array(detection_result)
        mouth_iou_list = []
        nose_iou_list = []
        face_iou_list = []
        for j in range(1, len(line)):
            left, top, right, bottom, class_id = [int(temp) for temp in line[j].split(',')]
            pred_box = [top, left, bottom, right]
            if class_id == CLASSES["face"]:
                face_iou = calculate_iou(face_box, pred_box)
                face_iou_list.append(face_iou)
            elif class_id == CLASSES["nose"]:
                nose_iou = calculate_iou(nose_box, pred_box)
                nose_iou_list.append(nose_iou)
            elif class_id == CLASSES["mouth"]:
                mouth_iou = calculate_iou(mouth_box, pred_box)
                mouth_iou_list.append(mouth_iou)

        print("face  : ", face_iou_list[-1])
        print("nose  : ", nose_iou_list[-1])
        print("mouth : ", mouth_iou_list[-1])

        pil_image = Image.fromarray(cv2.imread(img_path))
        draw = ImageDraw.Draw(pil_image)
        for j in range(1, len(line)):
            left, top, right, bottom, class_id = [int(temp) for temp in line[j].split(',')]
            for k in range(THICKNESS):
                draw.rectangle([left + k, top + k, right - k, bottom - k], outline=COLOR[class_id])
        del draw

        cv2.imshow("ground truth", np.array(pil_image))
        cv2.imshow("prediction", detection_result)
        cv2.waitKey(0)


if __name__ == "__main__":
    FLAGS = {'image': False, 'input': './path2your_video', 'output': ''}
    evaluate_detection(ANNOTATION_PATH, YOLO(**FLAGS))

