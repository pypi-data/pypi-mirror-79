import os
import random

import torch

from xml.etree import ElementTree as et
import json

# 0 未标记  无difficult
# 1 标记但被遮挡  difficult=1
# 2 标记且可见   difficult=0

diffToFlag = {
    '1': 1.000,
    '0': 2.000
}

list = []
isValidation = 1.000

category = ['L_eye', 'R_eye', 'L_ear', 'R_ear',
            'Nose', 'Throut', 'Withers', 'Tail',
            'L_F_elbow', 'R_F_elbow', 'L_F_knee',
            'R_F_knee', 'L_F_paw', 'R_F_paw',
            'L_B_elbow', 'R_B_elbow', 'L_B_knee',
            'R_B_knee', 'L_B_paw', 'R_B_paw']
def xmlToList(path='1.xml'):
    root = et.parse(path)
    tree = root.getroot()
    scale = round(random.uniform(0.5, 2.5), 3)
    filename = tree.find('filename').text
    size = tree.find('size')
    width, height = size.find('width').text, size.find('height').text
    center_width = round(random.uniform(3.0/8.0*float(width), 5.0/8.0*float(width)), 3)
    center_height = round(random.uniform(3.0/8.0*float(height), 5.0/8.0*float(height)), 3)
    center = [center_width, center_height]
    objects = tree.iter('object')
    joint_self = [[] for _ in range(20)]
    # print(joint_self)
    for object in objects:
        name = object.find('name').text
        index = category.index(name)
        flag = diffToFlag[object.find('difficult').text]
        bndbox = object.find('bndbox')

        x = bndbox.find('xmin').text
        y = bndbox.find('ymin').text
        joint_self[index].extend([float(x), float(y), flag])
    for i in joint_self:
        if len(i) == 0:
            i.extend([1.0, 1.0, 0.0])

    out = {
        "isValidation": isValidation,
        "img_paths": filename,
        "center":center,
        "joint_self": joint_self,
        "scale":scale
    }
    list.append(out)
def getFromXmlDir(dir_path):
    file_list = os.listdir(dir_path)
    sum, l = 1, len(file_list)
    for file_path in file_list:
        if file_path.split('.')[-1] == 'xml':
            xml_path = os.path.join(dir_path, file_path)
            xmlToList(xml_path)
            if sum % 5 == 0:
                print("{}/{}".format(sum, l))
            sum = int(sum)+1
    json_path = os.path.join(dir_path, 'data.json')
    with open(json_path, 'w') as json_file:
        json.dump(list, json_file)
    if check(json_path):
        print("已完成"+dir_path)
def check(json_path):
    with open(json_path) as anno_file:
        anno = json.load(anno_file)
    b = len(anno)
    for i in range(b):
        try:
            c = anno[i]
            img_paths = c['img_paths']
            # print("img_paths",img_paths)
            a = torch.Tensor(c['joint_self'])
        except ValueError:
            print("{}对应标签包含重复点，请检查".format(img_paths))
            return False
    return True


