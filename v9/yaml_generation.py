# import shutil
# dataset_root = r"D:\Forbmax User Data\waqar sahi\Dataset\Logo Dataset"
# # Copy code folder to the current working directory
# shutil.copytree(dataset_root, "Dataset")
import os
import random
import yaml
import shutil

def split_dataset(dataset_path, train_ratio=0.8):
    image_paths = [os.path.join(dataset_path, 'images', file) for file in os.listdir(os.path.join(dataset_path, 'images')) if file.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_paths)

    total_images = len(image_paths)
    train_size = int(total_images * train_ratio)

    train_paths = image_paths[:train_size]
    val_paths = image_paths[train_size:]

    with open(os.path.join(dataset_path,'train.txt'), 'w') as train_file:
        train_file.write('\n'.join(train_paths))

    with open(os.path.join(dataset_path, 'val.txt'), 'w') as val_file:
        val_file.write('\n'.join(val_paths))

def create_data_yaml(dataset_path, train_file, val_file):
    classes_path = os.path.join(dataset_path, 'labels', 'classes.txt')
    with open(classes_path, 'r') as classes_file:
        classes = [line.strip() for line in classes_file.readlines()]

    classes_mapping = {idx: class_name for idx, class_name in enumerate(classes)}

    data = {
        'path': os.path.abspath(dataset_path),
        'train': train_file,
        'val': val_file,
        'names': classes_mapping,
      
    }

    with open(os.path.join(dataset_path, 'data.yaml'), 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

# Example usage
dataset_path = 'Dataset'  # Assuming it's in the current working directory

# Split dataset into train and val
split_dataset(dataset_path)

# Create data.yaml file
create_data_yaml(dataset_path, 'train.txt', 'val.txt')

