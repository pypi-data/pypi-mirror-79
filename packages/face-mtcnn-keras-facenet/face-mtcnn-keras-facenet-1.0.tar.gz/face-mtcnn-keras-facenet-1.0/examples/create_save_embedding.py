import sys
sys.path.append("..")
from utils import fmkf
from numpy import savez_compressed
from numpy import  load
face=fmkf()

train_dir='./5-celebrity-faces-dataset/data/train/'
save_dataset_path="./dataset.npz"
save_embedding_path='./embedding.npz'
# trainX,trainy=face.load_dataset(train_dir)
# savez_compressed(save_dataset_path,trainX,trainy)
#有显示运行时间装饰器
data= load(save_dataset_path,allow_pickle=True)
# trainX,  trainy  =  data['arr_0'],  data['arr_1']
# print('Loaded: ',  trainX.shape,  trainy.shape)
newTrainX=face.dataset2embedding(save_dataset_path)
savez_compressed(save_embedding_path,  newTrainX[0],  newTrainX[1])
