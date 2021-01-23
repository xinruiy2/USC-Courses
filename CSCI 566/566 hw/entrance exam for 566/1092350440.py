import sys
import os
import pickle
import numpy as np
from sklearn.decomposition import PCA


# f = pickle.load(PATH_TO_DATA_DIR + "/train-images.idx3-ubyte", encoding="latin1")
# import matplotlib.pyplot as plt
# image = np.asarray(data[2])
# plt.imshow(image)
# plt.show()

# First part - working on data
K, D, N, PATH_TO_DATA_DIR = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
image_file = PATH_TO_DATA_DIR + "/train-images.idx3-ubyte"
label_file  = PATH_TO_DATA_DIR + "/train-labels.idx1-ubyte"

f = open(image_file, 'rb')
f_1 = open(label_file,'rb')
f.read(16)
f_1.read(8)
num_images = 800

buf = f.read(28 * 28 * num_images)
buf_1 = f_1.read(num_images)

data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
data_1 = np.frombuffer(buf_1, dtype=np.uint8).astype(np.int64)
data_1 = data_1.reshape(num_images, 1)
data = data.reshape(num_images, 28*28)
data = np.asarray(data)
data_1 = np.asarray(data_1)

test_data = data[0:N]
# print(test_data[:, 0].mean())
train_data = data[N:]
test_label = data_1[0:N].flatten()
train_label = data_1[N:].flatten()

# Second part - PCA
pca = PCA(n_components= D, svd_solver='full')
pca.fit(train_data)

train_img = pca.transform(train_data)
test_img = pca.transform(test_data)
# print(test_img[0])

# Third part - KNN

try:
    os.remove("1092350440.txt")
except OSError:
    pass

f_o = open("1092350440.txt", "w")
for i in range(len(test_img)):
    t = test_img[i]
    euclidean_diff = np.array([np.linalg.norm(t - train_img[i]) for i in range(len(train_img))])
    idx = list(np.argsort(euclidean_diff)[:K])
    dict = {}
    for id in idx:
        if train_label[id] in dict:
            dict[train_label[id]] += 1/(euclidean_diff[id])
        else:
            dict[train_label[id]] = 1/(euclidean_diff[id])
    predict_label = list(sorted(dict.items(), key = lambda x: x[1],reverse = True))[0][0]
    f_o.write(str(predict_label) + " " + str(test_label[i]) + '\n')
