#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import os
from keras.models import load_model
import cv2
from mtcnn import MTCNN
from os import listdir
from os.path import  isdir
from numpy import asarray
from numpy import  load
from PIL import Image
from matplotlib import pyplot
from numpy import  expand_dims
from numpy import  ndarray
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from random import choice
import time


def showtime(func):
    """
    打印运行时间，作为装饰器使用
    """
    def wrapper(*args,**kwargs):
        start=time.time()
        res=func(*args,**kwargs)
        return res
        end=time.time()
        print('耗时:{:.3f}'.format(end-start))
        pass
    return wrapper
    pass


class fmkf:
    """
        * model_path: faceNet 模型文件路径
    face mtcnn keras facenet 整合类
    需要扩展
        * Keras                   2.4.3,
        * matplotlib              3.3.1,
        * mtcnn                   0.1.0,
        * numpy                   1.18.5,
        * sklearn                 0.0,
        * tensorflow              2.3.0,
        * opencv-python           3.4.3.18,
    参考文章<https://www.infoq.cn/article/4wT4mNvKlVvEQZR-JXmp>
    """

    def __init__(self,model_path=""):
        if(os.path.isfile(model_path)):
            self.model_path=model_path
            pass
        else:
            self.model_path='../model/facenet_keras.h5';
            pass
        self.model=load_model(self.model_path,compile=False)
        pass



    def imgCheckFace(self,img_path,save=True,show=True,save_path=""):

        """
        检测出图片中的人脸，框出人脸，保存框出人脸后的图片;
            * img_path:含有人脸的图片路径;
            * save:是否保存框出人脸后的图片;
            * show:使用通过matplotlib展示框出人脸后的图片;
            * save_path:处理后的图片保存路径，默认保存到image_path目录下;
        """
        if(os.path.isfile(img_path)):
            detector = MTCNN()
            frame = cv2.imread(img_path)
            minsize=20
            faceRects = detector.detect_faces(frame)
            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect['box']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


            if save:
                if os.path.isdir(save_path):
                    pass
                else:
                    file, ext = os.path.splitext(img_path)
                    save_path=file+'_check'+ext
                cv2.imwrite(save_path,frame)
            if show:
                cv2.imshow('img', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                pass

        else:
            print('图片文件不存在')
            exit()
        pass


    def load_faces(self,directory):

        """
        获取路径中的人脸图片，并提取图片
            * directory:含有人脸的图片集合路径
        """
        faces = list()
        for filename in listdir(directory):
            path = directory + filename
            face = self.extract_face(path)
            if isinstance(face, ndarray):
                faces.append(face)
                pass
            else:
                print(path)
                pass
            pass
        return faces


    def load_dataset(self,directory):
        """
        加载数据集
            * directory:加载训练数据的目录
        """
        X, y = list(), list()

        for subdir in listdir(directory):
            path = directory + subdir + '/'

            if not isdir(path):
                continue
                pass
            faces = self.load_faces(path)
            labels = [subdir for _ in range(len(faces))]
            X.extend(faces)
            y.extend(labels)
            pass
        return asarray(X), asarray(y)

    def extract_face(self,filename, required_size=(160, 160)):

        """
        通过MTCNN获取图片中人脸，提取人脸，并且重置大小
            * filename:图片路径
            * required_size:元组，调整后的人脸图片大小
        """
        image = Image.open(filename)
        image = image.convert('RGB')
        pixels = asarray(image)
        detector = MTCNN()
        results = detector.detect_faces(pixels)
        face_array = ''
        try:
            x1, y1, width, height = results[0]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            face = pixels[y1:y2, x1:x2]
            image = Image.fromarray(face)
            image = image.resize(required_size)
            face_array = asarray(image)
            pass
        except IndexError:
            print(filename)
            pass
        return face_array

    def get_embedding(self,face_pixels):

        """
        把人脸像素信息转成人脸嵌入向量信息
            * face_pixels：人脸像素集合
        """

        if isinstance(face_pixels,ndarray):
            face_pixels==face_pixels.astype('float32')
            mean,std =face_pixels.mean(),face_pixels.std()
            face_pixels=(face_pixels-mean)/std
            samples=expand_dims(face_pixels,axis=0)
            yhat=self.model.predict(samples)
            return yhat[0]
        else:
            print("格式不正确")
            print(type(face_pixels))
            print(face_pixels)
            exit()

    def showImageFace(self,folder):
        """
        提取路径中所有图片的人脸，并且通过matplotlib.pyplot 展示出来
            * folder:图片集合路径
        """
        i=1
        for filename in listdir(folder):
            path=folder+filename
            face=self.extract_face(path)
            if isinstance(face, ndarray):
                pyplot.subplot(10,7,i)
                pyplot.axis('off')
                pyplot.imshow(face)
                i+=1
            pass
        pyplot.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出
            pyplot.close()

    def assessmentModel(self,embedding_path):

        """
        模型评估，必须含有测试数据，才能调用这个模型评估，如果文件中只有训练数据，无法正常运行
            * embedding_path：人脸嵌入数据集合文件路径
        """
        data = load(embedding_path)
        trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
        print('Dataset: train=%d, test=%d' % (trainX.shape[0], testX.shape[0]))

        in_encoder = Normalizer(norm='l2')
        trainX = in_encoder.transform(trainX)
        testX = in_encoder.transform(testX)

        out_encoder = LabelEncoder()
        out_encoder.fit(trainy)
        trainy = out_encoder.transform(trainy)
        testy = out_encoder.transform(testy)

        # fit model
        model = SVC(kernel='linear', probability=True)
        model.fit(trainX, trainy)
        # predict
        yhat_train = model.predict(trainX)
        yhat_test = model.predict(testX)
        # score
        score_train = accuracy_score(trainy, yhat_train)
        score_test = accuracy_score(testy, yhat_test)
        # summarize
        print('Accuracy: train=%.3f, test=%.3f' % (score_train * 100, score_test * 100))
        pass

    def testRecognition(self,dataset_path,embedding_path):

        """
        通过数据集对模型评估
            * dataset_path：数据集路径
            * embedding_path：人脸嵌入数据集路径

        """
        data = load(dataset_path)
        testX_faces = data['arr_2']
        # load face embeddings
        data = load(embedding_path)
        trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
        # normalize input vectors
        in_encoder = Normalizer(norm='l2')
        trainX = in_encoder.transform(trainX)
        testX = in_encoder.transform(testX)
        # label encode targets
        out_encoder = LabelEncoder()
        out_encoder.fit(trainy)
        trainy = out_encoder.transform(trainy)
        testy = out_encoder.transform(testy)
        # fit model
        model = SVC(kernel='linear', probability=True)
        model.fit(trainX, trainy)
        # test model on a random example from the test dataset
        selection = choice([i for i in range(testX.shape[0])])
        random_face_pixels = testX_faces[selection] #ndarray
        random_face_emb = testX[selection]
        random_face_class = testy[selection]
        print("random_face_pixels:{};random_face_emb:type:{},data:{};random_face_class:type:{},data:{}".format(type(random_face_pixels),type(random_face_emb),random_face_emb,type(random_face_class),random_face_class))
        random_face_name = out_encoder.inverse_transform([random_face_class])
        print(random_face_name)
        # prediction for the face
        samples = expand_dims(random_face_emb, axis=0)
        yhat_class = model.predict(samples)
        yhat_prob = model.predict_proba(samples)
        # get name
        class_index = yhat_class[0]
        class_probability = yhat_prob[0, class_index] * 100
        predict_names = out_encoder.inverse_transform(yhat_class)
        print('Predicted: %s (%.3f)' % (predict_names[0], class_probability))
        print('Expected: %s' % random_face_name[0])
        # plot for fun
        pyplot.imshow(random_face_pixels)
        title = '%s (%.3f)' % (predict_names[0], class_probability)
        pyplot.title(title)
        pyplot.show()
        pass

    @showtime
    def recognition(self,face_img_path,embedding_path,show=True,recognition_low=65):

        """
        识别传入图片
            * face_img_path:待识别的图片
            * embedding_path：人脸嵌入数据
            * show:是否通过matplotlib.pyplot展示识别后的图片
            * recognition_low：最低识别百分比。低于这个值返回无法识别
        """
        face_pixels=self.extract_face(face_img_path)
        if not isinstance(face_pixels, ndarray):
            print("No ace Detected")
            return
        face_emb=self.get_embedding(face_pixels)
        data = load(embedding_path)
        trainX, trainy= data['arr_0'], data['arr_1']
        in_encoder = Normalizer(norm='l2')
        trainX = in_encoder.transform(trainX)

        # label encode targets
        out_encoder = LabelEncoder()
        out_encoder.fit(trainy)
        trainy = out_encoder.transform(trainy)
        # fit model
        model = SVC(kernel='linear', probability=True)
        model.fit(trainX, trainy)
        samples = expand_dims(face_emb, axis=0)
        yhat_class = model.predict(samples)
        yhat_prob = model.predict_proba(samples)
        # get name
        class_index = yhat_class[0]
        class_probability = yhat_prob[0, class_index] * 100
        predict_names = out_encoder.inverse_transform(yhat_class)
        if class_probability >= recognition_low :
            pyplot.title('{} ({:.3f})'.format(predict_names[0], class_probability))
            pass
        else:
            pyplot.title('Unknown')
            print('Unrecognized')
            pass
        if show:
            pyplot.imshow(face_pixels)
            pyplot.show()
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出
                pyplot.close()
            pass
        pass


    @showtime
    def dataset2embedding(self,dataset_path,test=False):

        """
        人脸像素数据集转成人脸嵌入数据
            * dataset_path:数据集路径
            * test:数据集中如果含有测试数据集，请把test数据集也转成嵌入数据
        """
        data = load(dataset_path)
        if test:
            train_pixels, train_label = data['arr_2'], data['arr_3']
            pass
        else:
            train_pixels, train_label = data['arr_0'], data['arr_1']
            pass
        embedding_list=list()
        for face_pixels in train_pixels:
            embedding = self.get_embedding(face_pixels)
            embedding_list.append(embedding)
            pass
        return [embedding_list,train_label]



if __name__=='__main__':

    pass