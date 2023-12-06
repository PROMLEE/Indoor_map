import os
import cv2
import numpy as np
import tensorflow as tf

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def read_image(image_path, mask=False):
    image = tf.io.read_file(image_path)
    if mask:
        image = tf.image.decode_png(image, channels=1)
        image.set_shape([None, None, 1])
        image = tf.image.resize(images=image, size=[512, 512])
    else:
        # image = convert_non_greyscale_to_white(image)
        image = tf.image.decode_png(image, channels=3)
        image.set_shape([None, None, 3])
        image = tf.image.resize(images=image, size=[512, 512])
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

# colormap = loadmat("scripts\matlab.mat")["colormap"]
# colormap = colormap * 100
# colormap = colormap.astype(np.uint8)


def infer(model, image_tensor):
    predictions = model.predict(np.expand_dims((image_tensor), axis=0))
    predictions = np.squeeze(predictions)
    predictions = np.argmax(predictions, axis=2)
    return predictions


def decode_segmentaion_masks(mask, n_classes):
    white_color = np.array([255, 255, 255], dtype=np.uint8)
    colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
    colored_mask[mask == 0] = np.array([0, 0, 0], dtype=np.uint8)
    for i in range(1, n_classes):
        colored_mask[mask == i] = white_color

    return colored_mask


def get_overlay(image, colored_mask):
    image = tf.keras.preprocessing.image.array_to_img(image)
    image = np.array(image).astype(np.uint8)
    overlay = cv2.addWeighted(image, 0.35, colored_mask, 0.65, 0)
    return overlay


# def plot_samples_matplotlib(display_list, figsize=(5, 3)):
#     _, axes = plt.subplots(nrows=1, ncols=len(display_list), figsize=figsize)
#     for i in range(len(display_list)):
#         if display_list[i].shape[-1] == 3:
#             axes[i].imshow(tf.keras.preprocessing.image.array_to_img(display_list[i]))
#         else:
#             axes[i].imshow(display_list[i])
#     plt.show()


# def plot_predictions(images_list, colormap, model):
#     if not os.path.exists("result"):
#         os.makedirs("result")

#     for idx, image_file in enumerate(images_list):
#         image_tensor = read_image(image_file)
#         prediction_mask = infer(image_tensor=image_tensor, model=model)
#         prediction_colormap = decode_segmentaion_masks(prediction_mask, colormap, 20)
#         overlay = get_overlay(image_tensor, prediction_colormap)
#         plot_samples_matplotlib(
#             [image_tensor, overlay, prediction_colormap], figsize=(18, 14)
#         )

#         overlay_file = os.path.join("result", f"overlay_{idx}.png")
#         mask_file = os.path.join("result", f"mask_{idx}.png")
#         cv2.imwrite(overlay_file, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
#         cv2.imwrite(mask_file, cv2.cvtColor(prediction_colormap, cv2.COLOR_RGB2BGR))


# def is_greyscale(pixel):
#     return pixel[0] == pixel[1] == pixel[2]
def is_grayscale(rgb, tolerance=30):
    """주어진 픽셀이 무채색인지 확인합니다."""
    # print(rgb)
    r, g, b = rgb
    return max(r, g, b) - min(r, g, b) <= tolerance


def convert_non_greyscale_to_white(image):
    height, width, _ = image.shape
    # white_color = [255, 255, 255]
    for y in range(height):
        for x in range(width):
            if not is_grayscale(image[y, x]):
                image[y, x] = [255, 255, 255]
    overlay_file = os.path.join("sources/CAU208/masks", f"overlay_.png")
    cv2.imwrite(overlay_file, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    return image


def plot_predictions(buildingname):
    model = tf.keras.models.load_model("scripts/example.h5")
    inputurl = f"sources/{buildingname[:-3]}/gray/{buildingname}.png"
    outputurl = f"sources/{buildingname[:-3]}/masks"
    if not os.path.exists(outputurl):
        os.makedirs(outputurl, exist_ok=True)
    image_tensor = read_image(inputurl)
    image_array = tf.keras.preprocessing.image.img_to_array(image_tensor)
    image_array = (image_array + 1) * 127.5  # Convert back to original scale
    image_array = image_array.astype(np.uint8)

    # Convert non-greyscale pixels to white
    # image_array = convert_non_greyscale_to_white(image_array)

    prediction_mask = infer(image_tensor=image_tensor, model=model)
    prediction_colormap = decode_segmentaion_masks(prediction_mask, 5)
    # overlay = get_overlay(image_tensor, prediction_colormap)
    # plot_samples_matplotlib(
    #     [image_tensor, overlay, prediction_colormap], figsize=(18, 14)
    # )

    mask_file = os.path.join(outputurl, f"{buildingname}.png")
    prediction_colormap = cv2.resize(
        prediction_colormap, (1024, 1024), interpolation=cv2.INTER_AREA
    )
    cv2.imwrite(mask_file, cv2.cvtColor(prediction_colormap, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    plot_predictions("동훈궁_01")
