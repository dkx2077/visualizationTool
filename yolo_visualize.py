import cv2
import os
import numpy as np
import utils
from color_generate import ColorVisualizer


class YOLOVisualizer:
    def __init__(self, image_folder, label_folder, output_folder):
        self.image_folder = image_folder
        self.label_folder = label_folder
        self.output_folder = output_folder
        self.color_visualizer = ColorVisualizer(filename='./config/colors.yaml')
        self.colors_data = self.color_visualizer.load_colors()

    def process_images(self):
        images = utils.list_files(directory=self.image_folder, file_types="image")
        for image_name in images:
            self.process_single_image(image_name)

    def process_single_image(self, image_name):
        image_path = utils.concat_path(self.image_folder, image_name)
        label_path = utils.concat_path(self.label_folder, utils.get_file_prefix(image_name) + ".txt")
        image = utils.read_image_cv2(image_path)
        height, width, _ = image.shape

        with open(label_path, "r") as file:
            for line in file:
                self.draw_bbox(line, image, width, height)

        output_path = utils.concat_path(self.output_folder, image_name, check_exist=False)
        cv2.imencode(utils.get_file_extension(image_name), image)[1].tofile(output_path)
        print(f"Processed and saved: {output_path}")

    def draw_bbox(self, line, image, width, height):
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1]) * width
        y_center = float(parts[2]) * height
        box_width = float(parts[3]) * width
        box_height = float(parts[4]) * height

        x_min = int(x_center - box_width / 2)
        y_min = int(y_center - box_height / 2)
        x_max = int(x_center + box_width / 2)
        y_max = int(y_center + box_height / 2)

        rgb_color = self.colors_data[class_id]["rgb"]
        text = str(class_id)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), rgb_color, 2)
        cv2.putText(image, text, (x_min + 5, y_min + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, rgb_color, 2)


if __name__ == '__main__':
    abs_path = utils.get_abs_path()
    image_folder = utils.concat_path(abs_path, r"tmp\image")
    label_folder = utils.concat_path(abs_path, r"tmp\label")
    output_folder = utils.concat_path(abs_path, r"tmp\output", mkdir=True)

    processor = YOLOVisualizer(image_folder, label_folder, output_folder)
    processor.process_images()
