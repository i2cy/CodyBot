#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: NSFW_classification
# Created on: 2020/8/28

import os, time, psutil
import random
import pathlib

# *屏蔽tensorflow警告信息输出
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

# *RTX硬件兼容性修改配置
if tf.config.list_physical_devices('GPU') != []:
    tf.config.experimental.set_memory_growth(
        tf.config.list_physical_devices('GPU')[0], True)


DATASET_ROOT = "../../DeepLearning/Datasets/nsfw_image_classification"
TEST_RATE = 0.15
BATCH_SIZE = 16
EPOCHES = 20
BUFF_RATE = 0.1
LEARNING_RATE = 0.0001
MODEL_FILE = "../models/pic_classification_model.h5"
NAME = "Pic_Classification"


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
        inputs = tf.keras.Input(shape=self.data_shape)

        self.base_model = tf.keras.applications.Xception(input_shape=(256, 256, 3),
                                                            include_top=False,
                                                            weights=None)

        x = self.base_model(inputs)

        x = tf.keras.layers.GlobalAveragePooling2D()(x)  # 全局平均池化层

        x = tf.keras.layers.Dense(2048, activation="relu")(x)
        x = tf.keras.layers.Dense(2048, activation="relu")(x)

        out = tf.keras.layers.Dense(2, activation="softmax",
                                    name="out")(x)

        model = tf.keras.Model(inputs=inputs,
                               outputs=out,
                               name=self.name)

        self.model = model

        self.compile_model()

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

    def compile_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
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
        if len(data.shape) != len(self.data_shape) + 1:
            data = tf.expand_dims(data, 0)
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
        if img.shape[0] < 256 or img.shape[1] < 256:
            if img.shape[0] > img.shape[1]:
                rate = 256 / img.shape[1]
                img = tf.image.resize(img, [int(img.shape[0] * rate), 256])
            else:
                rate = 256 / img.shape[0]
                img = tf.image.resize(img, [256, int(img.shape[1] * rate)])
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_crop(img, [256, 256, 3])
    img = tf.cast(img, tf.float32)
    img = img / 127.5 - 1  # 图像归一化，使得输入数据在（-1,1）区间范围内
    return img


def read_preprocess_image_test(img_path):
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
        if img.shape[0] < 256 or img.shape[1] < 256:
            if img.shape[0] > img.shape[1]:
                rate = 256 / img.shape[1]
                img = tf.image.resize(img, [int(img.shape[0] * rate), 256])
            else:
                rate = 256 / img.shape[0]
                img = tf.image.resize(img, [256, int(img.shape[1] * rate)])
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_crop(img, [256, 256, 3])
    img = tf.cast(img, tf.float32)
    img = img / 127.5 - 1  # 图像归一化，使得输入数据在（-1,1）区间范围内
    return img


def read_preprocess_image_check(img_path):
    img = tf.io.read_file(img_path)
    if tf.image.is_jpeg(img):
        img = tf.image.decode_jpeg(img, channels=3)
    else:
        img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, [300, 300])
    img = tf.image.random_crop(img, [256, 256, 3])
    return img


class predictor:
    def __init__(self, dnn):
        self.dnn = dnn
        self.labels_converter = []
        self.pre_process_func = self._default_preprocess

    def _default_preprocess(self, data):
        return data

    def load_labels(self, label_names):  # label_names 必须为列表 [[标签列表1], [标签列表2]]
        for label in label_names:
            converter = dict((index, name)
                             for index, name in enumerate(label))
            self.labels_converter.append(converter)

    def set_preprocess_func(self, func):
        self.pre_process_func = func

    def predict(self, data):
        res_raw = self.dnn.predict(
            self.pre_process_func(data)
        )
        res = []
        for index, converter in enumerate(self.labels_converter):
            res.append(converter.get(tf.argmax(res_raw[index][0]).numpy()))
        return res


def check_data_safety(paths):
    unsafe = []
    stamp = time.time()
    total = len(paths)
    print("checked {} file, total {}".format(0, total), end="")
    for index, i in enumerate(paths):
        try:
            t = read_preprocess_image_check(i)
        except Exception as err:
            print("\ngot an unsafe file \"{}\"".format(i))
            unsafe.append(i)
        if time.time() - stamp > 1:
            stamp = time.time()
            print("\rchecked {} file, total {}".format(index+1, total), end="")
    print("")
    return unsafe



def main():
    print("initializing...")
    data_root = pathlib.Path(DATASET_ROOT)
    train_img_paths = [str(ele) for ele in data_root.glob("train/*/*/*.*")]
    test_img_paths = [str(ele) for ele in data_root.glob("test/*/*/*.*")]

    img_paths = []

    img_counts = len(train_img_paths) + len(test_img_paths)
    print("loaded", img_counts, "image paths")

    # 生成标签集转换字典
    label_types = list(set(pathlib.Path(path).parent.parent.name for path in test_img_paths))
    label_types = sorted(label_types)

    print("loaded labels:", label_types)

    type_to_label = dict((name, index)
                         for index, name in enumerate(label_types))

    print("labels and indexs:", type_to_label)

    random.shuffle(train_img_paths)

    # 检查数据集安全性
    #print("checking data safety...")
    #res = check_data_safety(train_img_paths+test_img_paths)
    #for i in res:
    #    os.remove(i)
    #    print("removed unsafe file \"{}\"".format(i))


    # 生成标签集
    train_labels = [type_to_label[pathlib.Path(path).parent.parent.name]
                    for path in train_img_paths]

    test_labels = [type_to_label[pathlib.Path(path).parent.parent.name]
                   for path in test_img_paths]

    print("dataset head:")
    print("============================================")
    print("Label\t\t\tIMG_Path")
    for i, l in enumerate(train_img_paths):
        if i > 9:
            break
        print(" " + str(train_labels[i]) + "\t" + str(l))
    print("============================================")

    # 初始化神经网络
    cnn = customNN(NAME)
    cnn.load_dataset((train_img_paths, train_labels),
                     (test_img_paths, test_labels),
                     mapFunc=read_preprocess_image,
                     batchSize=BATCH_SIZE,
                     shufflePercentage=BUFF_RATE,
                     mapFuncTest=read_preprocess_image_test
                     )

    # 初始化网络模型并执行设置
    if os.path.exists(MODEL_FILE):
        cnn.load_model(MODEL_FILE)
        print("loaded model file from \"{}\"".format(MODEL_FILE))
    else:
        cnn.init_model()

    print(cnn.model.summary())

    cnn.set_model_file(MODEL_FILE)

    #cnn.enable_tensorboard()
    #cnn.enable_checkpointAutosave(MODEL_FILE)

    # 检查数据集匹配是否有错
    print("datasets:\n{}".format(str(cnn.train_db)))

    # 初次训练网络
    choice = input("start training for {} epoch(s)? (Y/n): ".format(str(EPOCHES)))
    trained = False
    if EPOCHES > 0 and choice in ("Y", "y", "yes"):
        cnn.train(epochs=EPOCHES, verbose=1, validation=False)
        trained = True

    # 微调模型
    # cnn.postProc_model()

    # 再次训练网络
    # cnn.train(epochs=100)

    # 保存模型
    if trained:
        cnn.save_model()
        print("model saved to \"{}\"".format(MODEL_FILE))

    # 测试模型
    print("evaluating trained model...")
    cnn.evaluate()


'''
{'drawing': 0, 'hentai': 1}
'''

if __name__ == "__main__":
    main()
