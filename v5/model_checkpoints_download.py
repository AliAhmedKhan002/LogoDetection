import os
import shutil
import gdown

def delete_and_recreate_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def download_model(drive_link, destination):
    # Delete and recreate the folder
    delete_and_recreate_folder(destination)
    # Download the file from the drive link using gdown
    file_name = f"{destination}/{'best'}.pt"
    gdown.download(drive_link, file_name, quiet=False)

    print("Download complete.")
    return file_name

if __name__ == "__main__":
    # Replace these with your actual Google Drive links and local destination folders
    # link_for_ocr_model = "https://drive.google.com/file/d/1gFZbq_V91vn6nF3ND_IsYPedaSkSPpcV/view?usp=sharing"
    link_for_ocr_model='https://drive.google.com/uc?id=1cNeFbhrDEwW32piQH5Q3Za6INlCygDM8'
    folder_for_ocr_model = "Model_checkpoint\weights"

    path_for_ocr_model = download_model(link_for_ocr_model, folder_for_ocr_model)
    if path_for_ocr_model:
        print(f"\nDownload complete for OCR model. File saved to:\n{path_for_ocr_model}")


