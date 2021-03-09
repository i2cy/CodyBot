#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: lewdity_api.py
# Created on: 2020/9/13

import psutil
import os
import time
import random

# *屏蔽tensorflow警告信息输出
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

# *RTX硬件兼容性修改配置
if len(tf.config.list_physical_devices('GPU')) > 0:
    tf.config.experimental.set_memory_growth(
        tf.config.list_physical_devices('GPU')[0], True)

global typeClassificationCNN
global PaintingClassificationCNN
global PhotoClassificationCNN


TYPE_MODEL = "./models/pic_classification_model.h5"
PAINTING_MODEL = './models/NSFW_painting_model.h5'
PHOTO_MODEL = './models/NSFW_photo_model.h5'

LEWD_THRESHOLD = 0.997
SEXY_THRESHOLD = 0.99
LEWDITY_THRESHOLD = 0.02
CROP_TIMES = 40
BATCH_SIZE = 1


class customNN:
    def __init__(self, model_name="MLP"):
        self.name = model_name
        self.train_db = None
        self.test_db = None
        self.model = None
        self.train_size = 0
        self.test_size = 0
        self.data_shape = []
        self.batch_size = 8
        self.train_history = None
        self.tensorboard_enable = False
        self.log_root = "./tensorflow_log"
        self.callbacks = []
        self.callback_file_writer = None
        self.base_model = None
        self.epoch = 0
        self.model_file = "{}.h5".format(self.name)
        self.autosave = False
        self.output_counts = 0

    def _get_freeRAM(self):
        free_ram = psutil.virtual_memory().free
        return free_ram

    def _init_tensorboard(self):
        log_dir = os.path.join(self.log_root,
                               time.strftime("%Y%m%d-%H:%M:%S_") +
                               self.name
                               )
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir,
                                                              histogram_freq=1)
        self.callbacks.append(tensorboard_callback)
        self.callback_file_writer = tf.summary.create_file_writer(os.path.join(
            log_dir, "train"))
        self.callback_file_writer.set_as_default()

    def load_dataset(self, trainset, testset=None,
                     mapFunc=None, testRate=0.15, batchSize=8,
                     shufflePercentage=0.3, mapFuncTest=None,
                     mapFuncLabel=None, mapFuncLabelTest=None):  # dataset has to be formated tensors: (data, labels)
        self.batch_size = batchSize
        if testset == None:
            # randomly split trainset and testset
            datasets = [ele for ele in trainset]
            train_size = len(datasets[0]) - int(len(datasets[0]) * testRate)
            all_indexs = list(range(len(datasets[0])))
            random.shuffle(all_indexs)
            features = []
            labels = []
            if (type(datasets[1][0]) in (type([0]), type((0,)))) and len(datasets[1][0]) == len(all_indexs):
                for i in enumerate(datasets[1]):
                    labels.append([])
                    self.output_counts += 1
                for index in all_indexs[:train_size]:
                    data = datasets[0][index]
                    features.append(data)
                    for i, l in enumerate(datasets[1]):
                        label = datasets[1][i][index]
                        labels[i].append(label)
                if type(labels[0]) == type([0]):
                    labels = tuple(labels)
            else:
                self.output_counts += 1
                for index in all_indexs[:train_size]:
                    features.append(datasets[0][index])
                    labels.append(datasets[1][index])
            trainset = (features, labels)
            features = []
            labels = []
            if (type(datasets[1][0]) in (type([0]), type((0,)))) and len(datasets[1][0]) == len(all_indexs):
                for i in enumerate(datasets[1]):
                    labels.append([])
                for index in all_indexs[train_size:]:
                    data = datasets[0][index]
                    features.append(data)
                    for i, l in enumerate(datasets[1]):
                        label = datasets[1][i][index]
                        labels[i].append(label)
                if type(labels[0]) == type([0]):
                    labels = tuple(labels)
            else:
                for index in all_indexs[train_size:]:
                    features.append(datasets[0][index])
                    labels.append(datasets[1][index])
            testset = (features, labels)

        self.data_shape = tf.constant(trainset[0][0]).shape
        self.train_size = len(trainset[0])
        self.test_size = len(testset[0])

        print("trainset sample number: {}".format(str(self.train_size)))
        print("testset sample number: {}".format(str(self.test_size)))

        if mapFunc == None:
            if mapFuncLabel == None:
                train_db = tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(trainset[0]),
                                                tf.data.Dataset.from_tensor_slices(trainset[1])))
                test_db = tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(testset[0]),
                                               tf.data.Dataset.from_tensor_slices(testset[1])))
            else:
                if mapFuncLabelTest == None:
                    mapFuncLabelTest = mapFuncLabel
                train_db = tf.data.Dataset.zip((
                    tf.data.Dataset.from_tensor_slices(trainset[0]), tf.data.Dataset.from_tensor_slices(
                        trainset[1]).map(mapFuncLabel, num_parallel_calls=tf.data.experimental.AUTOTUNE)))

                test_db = tf.data.Dataset.zip((
                    tf.data.Dataset.from_tensor_slices(testset[0]), tf.data.Dataset.from_tensor_slices(
                        testset[1]).map(mapFuncLabelTest, num_parallel_calls=tf.data.experimental.AUTOTUNE)))

        else:
            if mapFuncTest == None:
                mapFuncTest = mapFunc
            self.data_shape = mapFunc(trainset[0][0]).shape
            train_db = tf.data.Dataset.from_tensor_slices(trainset[0])
            train_db = train_db.map(mapFunc, num_parallel_calls=tf.data.experimental.AUTOTUNE)
            test_db = tf.data.Dataset.from_tensor_slices(testset[0])
            test_db = test_db.map(mapFuncTest)

            if mapFuncLabel == None:
                train_db = tf.data.Dataset.zip((
                    train_db, tf.data.Dataset.from_tensor_slices(trainset[1])))
                test_db = tf.data.Dataset.zip((
                    test_db, tf.data.Dataset.from_tensor_slices(testset[1])))
            else:
                if mapFuncLabelTest == None:
                    mapFuncLabelTest = mapFuncLabel
                train_db = tf.data.Dataset.zip((
                    train_db, tf.data.Dataset.from_tensor_slices(
                        trainset[1]).map(mapFuncLabel, num_parallel_calls=tf.data.experimental.AUTOTUNE)))

                test_db = tf.data.Dataset.zip((
                    train_db, tf.data.Dataset.from_tensor_slices(
                        testset[1]).map(mapFuncLabelTest, num_parallel_calls=tf.data.experimental.AUTOTUNE)))

        datasize = 1
        for size in self.data_shape:
            datasize *= size
        freeRAM = int(self._get_freeRAM() * shufflePercentage)
        print("free RAM size: {} MB".format(str(freeRAM // 1048576)))

        shuffle_MaxbuffSize = int((freeRAM * 0.8) // datasize)
        prefetch_buffSize = int((freeRAM * 0.2) // (datasize * self.batch_size))

        print("automatically allocated data buffer size: {} MB".format(str(shuffle_MaxbuffSize * datasize // 1048576)))

        shuffle_buffSize = shuffle_MaxbuffSize
        if shuffle_MaxbuffSize > self.train_size:
            shuffle_buffSize = self.train_size
        train_db = train_db.shuffle(shuffle_buffSize).repeat().batch(self.batch_size).prefetch(prefetch_buffSize)
        shuffle_buffSize = shuffle_MaxbuffSize
        if shuffle_MaxbuffSize > self.test_size:
            shuffle_buffSize = self.test_size
        test_db = test_db.shuffle(shuffle_buffSize).repeat().batch(self.batch_size).prefetch(prefetch_buffSize)

        self.train_db = train_db
        self.test_db = test_db

    def set_model_file(self, path):
        self.model_file = path

    def enable_tensorboard(self, log_dir_root="./tensorflow_log"):
        self.log_root = log_dir_root
        self.tensorboard_enable = True

    def enable_checkpointAutosave(self, path=None):
        if path != None:
            self.model_file = path
        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=self.model_file)
        self.add_callback(checkpoint)
        self.autosave = True

    def add_callback(self, callback_func):  # all callbacks added will be reset after training
        self.callbacks.append(callback_func)

    def init_model(self):  # 神经网络模型
        pass

    def postProc_model(self):  # 模型后期处理（微调）
        model = self.model

        fine_tune_at = -33

        self.base_model.trainable = True

        for layer in self.base_model.layers[:fine_tune_at]:
            layer.trainable = False

        model.compile(optimizer="adam",
                      loss="binary_crossentropy",  # 2分类问题
                      metrics=["acc"]
                      )

        self.model = model
        print(model.summary())

    def compile_model(self, learningRate=0.0001):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learningRate),
                           loss="sparse_categorical_crossentropy",
                           metrics=["acc"]
                           )

    def save_model(self, path=None):
        if path != None:
            self.model_file = path
        self.model.save(self.model_file)

    def load_model(self, path=None):
        if path != None:
            self.model_file = path
        self.model = tf.keras.models.load_model(self.model_file, compile=True)
        self.compile_model()

    def train(self, epochs=100, verbose=1, validation=True):
        if self.tensorboard_enable and self.epoch == 0:
            self._init_tensorboard()
        try:
            if validation:
                self.train_history = self.model.fit(self.train_db,
                                                    epochs=epochs,
                                                    initial_epoch=self.epoch,
                                                    steps_per_epoch=self.train_size // self.batch_size,
                                                    validation_data=self.test_db,
                                                    validation_steps=self.test_size // self.batch_size,
                                                    callbacks=self.callbacks,
                                                    verbose=verbose
                                                    )
            else:
                self.train_history = self.model.fit(self.train_db,
                                                    epochs=epochs,
                                                    initial_epoch=self.epoch,
                                                    steps_per_epoch=self.train_size // self.batch_size,
                                                    callbacks=self.callbacks,
                                                    verbose=verbose
                                                    )
            self.epoch += epochs
        except KeyboardInterrupt:
            print("\ntraining process stopped manually")
            if self.autosave:
                self.load_model(self.model_file)

    def evaluate(self):
        print("evaluating model with test datasets...")

        acc = self.model.evaluate(self.test_db, return_dict=True,
                                  steps=self.test_size // self.batch_size)

        return acc

    def predict(self, data):
        res = self.model.predict(data)
        return res


def read_preprocess_image(img_path):
    img = tf.io.read_file(img_path)
    if tf.image.is_jpeg(img):
        img = tf.image.decode_jpeg(img, channels=3)
    else:
        img = tf.image.decode_png(img, channels=3)
    if img.shape[0] == None:
        print(img.shape)
        print(img)
        img = tf.image.resize(img, [300, 300])
    else:
        if img.shape[0] <= 256 and img.shape[1] <= 256:
            img = tf.image.resize(img, [300, 300])
        else:
            if img.shape[0] > img.shape[1]:
                rate = 300 / img.shape[1]
                img = tf.image.resize(img, [int(img.shape[0] * rate), 300])
            else:
                rate = 300 / img.shape[0]
                img = tf.image.resize(img, [300, int(img.shape[1] * rate)])
    imgs = []
    for i in range(BATCH_SIZE):
        img = tf.image.random_crop(img, [256, 256, 3], seed=int(time.time()*1000))
        img = tf.cast(img, tf.float32)
        img = img / 127.5 - 1  # 图像归一化，使得输入数据在（-1,1）区间范围内
        imgs.append(img)
    imgs = tf.convert_to_tensor(imgs)
    return imgs


def classificateImage(filename):
    img = read_preprocess_image(filename)
    sample_number = img.shape[0]

    lewd = False    # 是否为涩图
    sexy = False    # 是否为擦边球
    picType = 0     # 图片类型 （0 漫画  1 照片）
    sexility = 0    # 性感检出率
    sexyMax = 0     # 神经网络性感度最大输出
    lewdity = 0     # 色情检出率
    lewdMax = 0     # 神经网络色情度最大输出


    # 判断图片是漫画还是照片 (0 漫画  1 照片)
    picType = TypeClassificationCNN.predict(img)
    picType = picType.argmax(axis=1).mean()

    if picType < 0.5:
        # 漫画特化神经网络鉴黄 （0 正常  1 色情）
        lewdityRes = PaintingClassificationCNN.predict(img)
        for i in lewdityRes:
            if i[1] > LEWD_THRESHOLD:
                lewd = True
                lewdity += 1
            if i[1] > lewdMax:
                lewdMax = i[1]

    else:
        # 照片特化神经网络鉴黄 （0 正常  1 色情  2 擦边球）
        lewdityRes = PhotoClassificationCNN.predict(img)
        for i in lewdityRes:
            if i[1] > LEWD_THRESHOLD:
                lewd = True
                lewdity += 1
            if i[1] > lewdMax:
                lewdMax = i[1]
            if i[2] > SEXY_THRESHOLD:
                sexy = True
                sexility += 1
            if i[2] > sexyMax:
                sexyMax = i[2]

    sexility /= sample_number
    lewdity /= sample_number

    return {"lewd": lewd,
            "sexy": sexy,
            "lewdity": lewdity,
            "sexility": sexility,
            "lewdMax": lewdMax,
            "sexyMax": sexyMax,
            "picType": picType}


def classificateAPI(filename):  # API入口
    timetick = time.time()
    if len(filename) > 3 and filename[-3:] == "gif":
        return {"lewd": False}

    lewd = False
    sexy = False
    lewdity = 0
    sexility = 0
    lewdMax = 0
    sexyMax = 0
    picType = 0

    for i in range(CROP_TIMES):
        res = classificateImage(filename)
        if res["lewd"] == True:
            lewd = True
        if res["sexy"] == True:
            sexy = True
        lewdity += res["lewdity"]
        sexility += res["sexility"]
        if lewdMax < res["lewdMax"]:
            lewdMax = res["lewdMax"]
        if sexyMax < res["sexyMax"]:
            sexyMax = res["sexyMax"]
        picType += res["picType"]

    lewdity /= CROP_TIMES
    sexility /= CROP_TIMES
    picType /= CROP_TIMES

    if picType < 0.5:
        sexy = False

    if lewdity < LEWDITY_THRESHOLD:
        lewd = False

    return {"lewd": lewd,
            "sexy": sexy,
            "lewdity": lewdity,
            "sexility": sexility,
            "lewdMax": lewdMax,
            "sexyMax": sexyMax,
            "picType": picType,
            "timeSpend": time.time()-timetick}





def init():
    global TypeClassificationCNN
    global PaintingClassificationCNN
    global PhotoClassificationCNN

    print("initializing lewdity API...")

    # 初始化图片类型鉴定神经网络（底层）
    TypeClassificationCNN = customNN("Pic_Type_Classification")
    try:
        TypeClassificationCNN.load_model(TYPE_MODEL)
        print("loaded model \"{}\"".format(TYPE_MODEL))
    except Exception as err:
        print("failed to load model,", err)

    # 初始化漫画鉴黄神经网络（顶层分支）
    PaintingClassificationCNN = customNN("Painting_Classification")
    try:
        PaintingClassificationCNN.load_model(PAINTING_MODEL)
        print("loaded model \"{}\"".format(PAINTING_MODEL))
    except Exception as err:
        print("failed to load model,", err)


    # 初始化照片鉴黄神经网络（顶层分支）
    PhotoClassificationCNN = customNN("Photo_Classification")
    try:
        PhotoClassificationCNN.load_model(PHOTO_MODEL)
        print("loaded model \"{}\"".format(PHOTO_MODEL))
    except Exception as err:
        print("failed to load model,", err)

    print("lewdity API initializied")


def main():
    pass


if __name__ == "__main__":
    main()
else:
    init()