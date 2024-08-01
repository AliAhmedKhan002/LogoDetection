import os
import random
import numpy as np

def process_data(root_dir):
    img_dir = os.path.join(root_dir, 'images')
    train_txt_path = os.path.join(root_dir, 'train.txt')
    validate_txt_path = os.path.join(root_dir, 'validate.txt')
    labels_path = os.path.join(root_dir, 'labels/classes.txt')
    data_yaml_path = os.path.join(root_dir, 'data.yaml')

    img_paths = []
    for dirname, _, filenames in os.walk(img_dir):
        for filename in filenames:
            img_paths.append(os.path.join(img_dir, filename))

    random.shuffle(img_paths)
    train, validate = np.split(img_paths, [int(len(img_paths) * 0.8)])

    with open(train_txt_path, 'w') as f:
        lines = list('\n'.join(train))
        f.writelines(lines)

    with open(validate_txt_path, 'w') as f:
        lines = list('\n'.join(validate))
        f.writelines(lines)

    with open(labels_path, 'r') as f:
        names = f.read().split('\n')

    with open(data_yaml_path, 'w') as f:
        f.write("train: " + os.path.join(root_dir, 'train.txt') + "\n")
        f.write("val: " + os.path.join(root_dir, 'validate.txt') + "\n")
        f.write("nc: " + str(len(names)-1) + "\n")
        f.write("names: [" + ", ".join(['"' + name + '"' for name in filter(None, names)]) + "]\n")


# Example usage
root_directory =r"D:\Forbmax User Data\waqar sahi\Dataset\Logo Dataset"
process_data(root_directory)
