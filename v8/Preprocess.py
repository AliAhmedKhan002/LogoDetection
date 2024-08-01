import os
import random
import shutil
import yaml

def split_and_organize_data(dataset_root, output_folder='Dataset', split_ratio=0.8):
    # Specify the paths to the XML and Image folders
    xml_folder = os.path.join(dataset_root, 'labels')
    image_folder = os.path.join(dataset_root, 'images')

    # Specify the paths for the output train and validate folders
    train_folder = os.path.join(output_folder, 'train')
    validate_folder = os.path.join(output_folder, 'validate')

    # Create output folders if they don't exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(validate_folder, exist_ok=True)
    
    # Create subfolders for images and labels inside train and validate folders
    os.makedirs(os.path.join(train_folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(train_folder, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(validate_folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(validate_folder, 'labels'), exist_ok=True)

    # Get a list of all file names without extensions in the Image folder
    all_files = [os.path.splitext(file)[0] for file in os.listdir(image_folder) if file.endswith('.jpg')]

    # Calculate the number of files for each split
    total_files = len(all_files)
    train_size = int(split_ratio * total_files)

    # Randomly shuffle the file names
    random.shuffle(all_files)

    # Split the data into train and validate sets
    train_files = all_files[:train_size]
    validate_files = all_files[train_size:]

    # Move files to respective folders
    for file_name in train_files:
        shutil.copy(os.path.join(image_folder, file_name + '.jpg'), os.path.join(train_folder, 'images', file_name + '.jpg'))
        shutil.copy(os.path.join(xml_folder, file_name + '.txt'), os.path.join(train_folder, 'labels', file_name + '.txt'))

    for file_name in validate_files:
        shutil.copy(os.path.join(image_folder, file_name + '.jpg'), os.path.join(validate_folder, 'images', file_name + '.jpg'))
        shutil.copy(os.path.join(xml_folder, file_name + '.txt'), os.path.join(validate_folder, 'labels', file_name + '.txt'))

    print("Data splitting and organization completed. Files are organized into train and validate folders.")
    classes_file_path = os.path.join(xml_folder, 'classes.txt')
    # Read class names from classes.txt
    with open(classes_file_path, 'r') as f:
        class_names  = f.read().split('\n')
    # Write the dictionary to the data.yaml file
    print(os.path.join(os.getcwd(),train_folder))
    with open(os.path.join(output_folder, 'data.yaml'), 'w') as f:
        f.write("train: " + os.path.join(os.getcwd(),train_folder, 'images') + "\n")
        f.write("val: " + os.path.join(os.getcwd(),validate_folder, 'images') + "\n")
        f.write("nc: " + str(len(class_names)-1) + "\n")
        f.write("names: [" + ", ".join(['"' + name + '"' for name in filter(None, class_names )]) + "]\n")
    
    


    print("data.yaml file created successfully.")