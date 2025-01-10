import os
import shutil
from NeuralNetwork.predict import predict_image  

BASE_FOLDER = r'G:\共有ドライブ\Publico\6) 研修・講座 (Curso e Seminário)\c) 汎米研修\2025\3) 研修生\6 研修生書類\certo'

def classify_and_move_file(file_path, user_name):
   
    classification_result = predict_image(file_path)

    # ユーザー名のフォルダーを作成（存在しない場合のみ）
    user_folder = os.path.join(BASE_FOLDER, user_name)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # ファイルの新しい保存先（ユーザーごとのフォルダー内にサブフォルダを作成）
    category_folder = os.path.join(user_folder, classification_result)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    # 新しいファイルの保存場所
    destination_path = os.path.join(category_folder, os.path.basename(file_path))

    # ファイルを新しい場所に移動
    shutil.move(file_path, destination_path)
    print(f"Moved {file_path} to {destination_path}")
