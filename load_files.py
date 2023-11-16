import os

def load_files() -> list:
    texts = []
    folder = "files"
    if os.path.exists(folder):
        files = os.listdir(folder)
        for file in files:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r',encoding='utf-8') as file:
                    description = file.read()
                    texts.append(description)
    else:
        print("The folder doesn't exist")

    return texts