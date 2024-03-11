import os
import cv2
import numpy as np
from glob import glob
from scipy.io import loadmat
import matplotlib.pyplot as plt
import pickle
import tensorflow as tf


os.environ["CUDA_VISIBLE_DEVICES"] = "0"


DIR = "h5examples/v3+/"
test_images = sorted(glob(os.path.join("Test/*")))
# test_images = sorted(glob(os.path.join("Validation/images/*")))
model = tf.keras.models.load_model(DIR + "example.h5")
history = pickle.load(open(DIR + "Dict.txt", "rb"))


IMAGE_SIZE = 512


def read_image(image_path, mask=False):
    image = tf.io.read_file(image_path)
    if mask:
        image = tf.image.decode_png(image, channels=1)
        image.set_shape([None, None, 1])
        image = tf.image.resize(images=image, size=[IMAGE_SIZE, IMAGE_SIZE])
    else:
        image = tf.image.decode_png(image, channels=3)
        image.set_shape([None, None, 3])
        image = tf.image.resize(images=image, size=[IMAGE_SIZE, IMAGE_SIZE])
        image = image / 127.5 - 1

    return image


# loss = history["loss"]
# val_loss = history["val_loss"]

# fig = plt.figure(figsize=(12, 5))

# ax1 = fig.add_subplot(1, 2, 1)
# ax1.plot(loss, color="blue", label="train_loss")
# ax1.plot(val_loss, color="red", label="val_loss")
# ax1.set_title("Train and Validation Loss")
# ax1.set_xlabel("Epochs")
# ax1.set_ylabel("Loss")
# ax1.grid()
# ax1.legend()


# accuracy = history["accuracy"]
# val_accuracy = history["val_accuracy"]

# ax2 = fig.add_subplot(1, 2, 2)
# ax2.plot(accuracy, color="blue", label="train_Accuracy")
# ax2.plot(val_accuracy, color="red", label="val_Accuracy")
# ax2.set_title("Train and Validation Accuracy")
# ax2.set_xlabel("Epochs")
# ax2.set_ylabel("Accuracy")
# ax2.grid()
# ax2.legend()

# plt.show()

colormap = loadmat("./matlab.mat")["colormap"]
colormap = colormap * 100
colormap = colormap.astype(np.uint8)


def infer(model, image_tensor):
    predictions = model.predict(np.expand_dims((image_tensor), axis=0))
    predictions = np.squeeze(predictions)
    predictions = np.argmax(predictions, axis=2)
    return predictions


def decode_segmentaion_masks(mask, colormap, n_classes):
    r = np.zeros_like(mask).astype(np.uint8)
    g = np.zeros_like(mask).astype(np.uint8)
    b = np.zeros_like(mask).astype(np.uint8)
    for i in range(0, n_classes):
        idx = mask == i
        r[idx] = colormap[i, 0]
        g[idx] = colormap[i, 1]
        b[idx] = colormap[i, 2]
    rgb = np.stack([r, g, b], axis=2)
    return rgb


def get_overlay(image, colored_mask):
    image = tf.keras.preprocessing.image.array_to_img(image)
    image = np.array(image).astype(np.uint8)
    overlay = cv2.addWeighted(image, 0.35, colored_mask, 0.65, 0)
    return overlay


def plot_samples_matplotlib(display_list, figsize=(5, 3)):
    _, axes = plt.subplots(nrows=1, ncols=len(display_list), figsize=figsize)
    for i in range(len(display_list)):
        if display_list[i].shape[-1] == 3:
            axes[i].imshow(tf.keras.preprocessing.image.array_to_img(display_list[i]))
        else:
            axes[i].imshow(display_list[i])
    plt.show()


def plot_predictions(images_list, colormap, model):
    # for image_file in images_list:
    #     image_tensor = read_image(image_file)
    #     prediction_mask = infer(image_tensor=image_tensor, model=model)
    #     prediction_colormap = decode_segmentaion_masks(prediction_mask, colormap, 20)
    #     overlay = get_overlay(image_tensor, prediction_colormap)
    #     plot_samples_matplotlib(
    #         [image_tensor, overlay, prediction_colormap], figsize=(18, 14)
    #     )
    if not os.path.exists("result"):
        os.makedirs("result")

    for idx, image_file in enumerate(images_list):
        image_tensor = read_image(image_file)
        prediction_mask = infer(image_tensor=image_tensor, model=model)
        prediction_colormap = decode_segmentaion_masks(prediction_mask, colormap, 20)
        overlay = get_overlay(image_tensor, prediction_colormap)

        # 결과를 matplotlib으로 표시 (선택적)
        plot_samples_matplotlib(
            [image_tensor, overlay, prediction_colormap], figsize=(18, 14)
        )

        # 결과 파일 저장
        overlay_file = os.path.join("result", f"overlay_{idx}.png")
        mask_file = os.path.join("result", f"mask_{idx}.png")
        cv2.imwrite(overlay_file, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
        cv2.imwrite(mask_file, cv2.cvtColor(prediction_colormap, cv2.COLOR_RGB2BGR))


plot_predictions(test_images, colormap, model=model)
