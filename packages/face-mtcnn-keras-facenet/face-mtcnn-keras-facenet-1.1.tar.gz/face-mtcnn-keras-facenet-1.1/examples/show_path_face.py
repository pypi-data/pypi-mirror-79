import sys
import os
sys.path.append("..")
from utils import fmkf
face=fmkf()
#待显示的人脸图片集合路径
show_face_path=os.getcwd()+'/5-celebrity-faces-dataset/data/val/elton_john/'
#显示图片中提取到的人脸，并通过matplotlib展示
face.showImageFace(show_face_path)
