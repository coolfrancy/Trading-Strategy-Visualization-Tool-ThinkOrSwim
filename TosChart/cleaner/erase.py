def clean_folder(folder_path):
    import os
    
    # List all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)


if __name__=='__main__':
    clean_folder()