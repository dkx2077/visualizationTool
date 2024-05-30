import random
import yaml
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgb


class ColorUtils:
    """颜色相关的工具类"""

    @staticmethod
    def random_color():
        """生成一种随机颜色的16进制表示"""
        return '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def hex_to_rgb(hex_color):
        """将16进制颜色转换为RGB元组"""
        return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb_to_hex(rgb_color):
        """将RGB元组转换为16进制颜色"""
        return '#%02X%02X%02X' % rgb_color

    @staticmethod
    def color_distance(c1, c2):
        """计算两种颜色之间的欧几里德距离"""
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


class ColorGenerator:
    """生成具有足够差异的颜色"""

    def __init__(self, min_distance=200):
        self.colors = []
        self.min_distance = min_distance

    def generate_colors(self, num_colors=100):
        """生成指定数量的具有足够差异的颜色"""
        color_hex = ColorUtils.random_color()
        color_rgb = ColorUtils.hex_to_rgb(color_hex)
        self.colors.append({'id': 1, 'hex': color_hex, 'rgb': list(color_rgb)})

        for i in range(2, num_colors + 1):
            new_color = ColorUtils.random_color()
            min_distance = float('inf')
            for color in self.colors:
                distance = ColorUtils.color_distance(new_color, color['hex'])
                if distance < min_distance:
                    min_distance = distance
            if min_distance < self.min_distance:
                new_color = ColorUtils.random_color()
                min_distance = float('inf')
                for color in self.colors:
                    distance = ColorUtils.color_distance(new_color, color['hex'])
                    if distance < min_distance:
                        min_distance = distance
            self.colors.append({'id': i, 'hex': new_color, 'rgb': list(ColorUtils.hex_to_rgb(new_color))})

    def save_colors(self, filename='./config/colors.yaml'):
        """将生成的颜色保存到YAML文件"""
        with open(filename, 'w') as f:
            yaml.dump({'colors': self.colors}, f)


class ColorVisualizer:
    """颜色可视化器"""

    def __init__(self, filename='./config/colors.yaml'):
        self.filename = filename
        self.colors_data = self.load_colors()

    def load_colors(self):
        """从YAML文件加载颜色数据"""
        with open(self.filename, 'r') as file:
            colors_data = yaml.safe_load(file)['colors']
        return colors_data

    def visualize_colors(self, save_filename=None):
        """将颜色可视化为正方形,保存到图像文件中"""
        fig, ax = plt.subplots(figsize=(10, 10))

        for i, color in enumerate(self.colors_data):
            hex_value = color['hex']
            rgb_value = to_rgb(hex_value)
            x = i // 10
            y = i % 10
            rect = patches.Rectangle((y, x), 1, 1, facecolor=hex_value, edgecolor='black')
            ax.add_patch(rect)
            ax.text(y + 0.1, x + 0.5, hex_value, fontsize=8, ha='left', va='center',
                    color='white' if sum(rgb_value) < 0.5 else 'black')

        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-0.5, 10.5)
        ax.set_xticks(range(11))
        ax.set_yticks(range(11))
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')

        if save_filename:
            plt.savefig(save_filename)
        plt.show()


if __name__ == '__main__':
    if not os.path.exists('./config/colors.yaml'):
        print('colors.yaml文件已存在,正在读取...')
        color_generator = ColorGenerator()
        color_generator.generate_colors()
        color_generator.save_colors()

    color_visualizer = ColorVisualizer(filename='./config/colors.yaml')
    color_visualizer.visualize_colors(save_filename='colors_map.png')