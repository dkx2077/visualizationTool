import cv2
import subprocess
import numpy as np
import os


def read_image_cv2(image_path):
    return cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), flags=cv2.IMREAD_COLOR)


def get_abs_path():
    return os.path.abspath(os.path.dirname(__file__))


def concat_path(path1, path2, mkdir=False, check_exist=True):
    out_path = os.path.normpath(os.path.join(path1, path2))
    if check_exist and not mkdir:
        if not os.path.exists(out_path):
            raise Exception('{} 不存在'.format(out_path))
    if mkdir:
        os.makedirs(out_path, exist_ok=True)

    return out_path


def list_files(directory, file_types=None):
    """
    在指定目录中查找与给定文件类型列表匹配的所有文件。

    参数:
    directory (str): 需要搜索的目录路径。
    file_types (tuple): 一个包含文件扩展名的元组，例如 ('.txt', '.jpg')。

    返回:
    list: 匹配指定文件类型的文件名列表。
    """

    if file_types is None:
        files = [file for file in os.listdir(directory)]
    elif file_types == "image":
        files = [file for file in os.listdir(directory) if file.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    elif file_types == "txt":
        files = [file for file in os.listdir(directory) if file.endswith('.txt')]

    return files


def get_file_prefix(filename):
    return os.path.splitext(filename)[0]


def get_file_extension(filename):
    return os.path.splitext(filename)[-1]
