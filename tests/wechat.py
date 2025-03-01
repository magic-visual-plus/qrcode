import cv2
import os
import shutil

def decode_qr_wechat(image_path):
    # 加载预训练的模型文件
    try:
        model_path = os.path.dirname(os.path.abspath(__file__))
        # 处理模型文件路径
        detect_prototxt_path = os.path.join(model_path, 'detect.prototxt')
        detect_caffemodel_path = os.path.join(model_path, 'detect.caffemodel')
        sr_prototxt_path = os.path.join(model_path, 'sr.prototxt')
        sr_caffemodel_path = os.path.join(model_path, 'sr.caffemodel')
        detector = cv2.wechat_qrcode_WeChatQRCode(detect_prototxt_path, detect_caffemodel_path, sr_prototxt_path, sr_caffemodel_path)
        img = cv2.imread(image_path)
        
        res, points = detector.detectAndDecode(img)
        if res:
            for r in res:
                print(f"图片 {image_path} 解码结果: {r}")
            return True
        else:
            print(f"图片 {image_path} 未识别到二维码")
            # 复制文件到目标文件夹
            shutil.copy(image_path, 'tests/data/failed')
            return False
    except Exception as e:
        print(f"处理图片 {image_path} 时出现错误: {e}")
        return False

def process_folder(folder_path):
    success_count = 0
    fail_count = 0
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            if decode_qr_wechat(image_path):
                success_count += 1
            else:
                fail_count += 1

    # 输出统计结果
    print(f"\n统计结果：")
    print(f"识别成功的图片数量: {success_count}")
    print(f"识别失败的图片数量: {fail_count}")

# 替换为实际的文件夹路径
folder_path = 'tests/data'
process_folder(folder_path)