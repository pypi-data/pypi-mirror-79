"""
在执行该文件之前，必须先创建embedding.npz数据文件,测试数据，请运行create_save_embedding.py 文件
"""
import sys
import os
sys.path.append("..")
from utils import fmkf
face=fmkf()
#人脸嵌入压缩数据文件
save_embedding_path='./embedding_test.npz'
#需要分类或者识别的图片
face_image_path=os.getcwd()+'/5-celebrity-faces-dataset/data/val/elton_john/httpafilesbiographycomimageuploadcfillcssrgbdprgfacehqwMTEODAOTcxNjcMjczMjkzjpg.jpg'
#识别图片
face.recognition(face_image_path,save_embedding_path)


