import sys
sys.path.append("..")
from utils import fmkf
from numpy import  load
from numpy import savez_compressed
face=fmkf()

#带训练的数据集合
train_dir='./5-celebrity-faces-dataset/data/train/'
#测试数据集合
test_dir='./5-celebrity-faces-dataset/data/val/'
#提取出的数据集合中的人脸像素数据的保存文件
save_dataset_path="./dataset_test.npz"
#训练出的人脸嵌入数据的保存文件
save_embedding_path='./embedding_test.npz'

#获取训练数据的人脸像素信息和数据标签
trainX,trainy=face.load_dataset(train_dir)
#获取测试数据的人脸像素信息和数据标签
testX,testy=face.load_dataset(test_dir)
#保存训练和测试人脸像素信息和数据标签
savez_compressed(save_dataset_path,trainX,trainy,testX,testy)
#加载人脸像素信息和数据标签

data= load(save_dataset_path,allow_pickle=True)
trainX,  trainy,  testX,  testy  =  data['arr_0'],  data['arr_1'],  data['arr_2'],  data['arr_3']

"""
打印数据信息
Loaded:  (93, 160, 160, 3) (93,) (25, 160, 160, 3) (25,)

"""
# print('Loaded: ',  trainX.shape,  trainy.shape,  testX.shape,  testy.shape)

#训练数据转换成人脸嵌入向量数据，有显示运行时间装饰器
newTrainX=face.dataset2embedding(save_dataset_path)
#测试数据转成人脸嵌入向量数据，有显示运行时间装饰器
newTestX=face.dataset2embedding(save_dataset_path,test=True)
#保存人脸嵌入向量数据
savez_compressed(save_embedding_path,    newTrainX[0],  newTrainX[1],  newTestX[0],  newTestX[1])

#通过数据集对模型评估

face.testRecognition(save_dataset_path,save_embedding_path)