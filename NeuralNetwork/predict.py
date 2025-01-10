import os
import torch
from torchvision import transforms
from PIL import Image
from .model import create_model

# Função para carregar o modelo treinado
def load_model(path='trained_model.pth'):
    model = create_model(num_classes=2)
    model.load_state_dict(torch.load(path, weights_only=True))
    model.eval()  # Coloca o modelo em modo de avaliação
    return model

# Função para realizar a previsão
def predict_image(image_path, model):
    model = load_model(r'C:\Users\Seminario4\AppData\Local\Programs\Python\Python313\NewEmailFileChecker\NeuralNetwork\trained_model.pth')
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Adiciona uma dimensão para o batch

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)  # Pega a classe com a maior probabilidade
        return predicted.item()

def move_file(file_path, category):
    target_dir = os.path.join('classified_files', category)  # カテゴリごとのフォルダ
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # フォルダがなければ作成
    os.rename(file_path, os.path.join(target_dir, os.path.basename(file_path)))  # ファイルを移動

# クラス名リスト（予測されるカテゴリ）
categories = ['パスポート', 'IDカード', '予防接種証明書', '保険加入領収書']

# 使用例
model = load_model('trained_model.pth')  # モデルをロード
image_path = 'path_to_image.jpg'  # 画像のパス
category_index = predict_image(image_path, model)  # 画像を分類
category = categories[category_index]  # 分類結果に基づくカテゴリ名

# ファイルを移動
move_file(image_path, category)
print(f"ファイル '{image_path}' は '{category}' フォルダに移動されました。")