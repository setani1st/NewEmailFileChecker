import torch.nn as nn
import torchvision.models as models

def create_model(num_classes=2):
    # Carregar um modelo pré-treinado
    model = models.resnet18(pretrained=True)

    # Congelar as camadas convolucionais (não treinar)
    for param in model.parameters():
        param.requires_grad = False

    # Substituir a última camada totalmente conectada (fc) para ajustar ao número de classes
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model


