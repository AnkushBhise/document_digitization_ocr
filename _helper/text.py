import os
from typing import Union


def write_text_file(text: Union[list, str] , file_name: str, file_path: str = "data"):
    file = os.path.join(file_path, file_name)
    file = open(file, "w")
    if isinstance(text, list):
        file.writelines(text)
    elif isinstance(text, str):
        file.write(text)
    else:
        print("Please send text in list or string formate")
    file.close()


if __name__ == "__main__":
    text_data = "This is Delhi \nThis is Paris \nThis is London \n"
    write_text_file(text_data, "test_file.txt")
