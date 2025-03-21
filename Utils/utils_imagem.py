import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os
import cv2
from PIL import Image
from io import BytesIO
import requests


def leitura_Imagem(nome):
    
    # Carrega a imagem
    Imagem = cv2.imread(nome, cv2.IMREAD_GRAYSCALE)
    
    # Retorna a imagem
    return Imagem


# Realiza a plotagem das imagens com o matplotlib
def plotagem_imagem(Imagem_Original, Imagem_Filtrada):
    
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    # Adiciona as imagens nos subplots
    axs[0].imshow(Imagem_Original)
    axs[0].set_title('Imagem Original')
    
    axs[1].imshow(Imagem_Filtrada, cmap='gray')
    axs[1].set_title('Imagem Filtrada')
    
    # Remove os eixos dos subplots
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
    
    # Mostra a figura com os subplots
    plt.show()
    
def salvar_imagem(Imagem, nome):
    
    plt.imsave(nome, Imagem, cmap='gray')
    
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        console.print('{}. {}'.format(i+1, imagem))
        
    return imagens

def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o Watershed
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o [bold purple]Watershed[/bold purple]', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')
            
def download_imagem(args):
    
    console = Console()
    
    # Baixa a imagem da URL
    response = requests.get(args.url)
    
    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        # Lê a imagem
        Imagem = Image.open(BytesIO(response.content))
        
        # Define o nome da imagem
        nome_imagem = "IMAGEM_BAIXADA_URL"  # Nome fixo
        extensao = args.url.split('.')[-1]  # Extrai a extensão da URL (ex: jpg, png, etc.)
        
        # Salva a imagem com o novo nome
        Imagem.save(f'./imagens/{nome_imagem}.{extensao}')
        
    else:
        console.print('Erro ao baixar a imagem. Tente novamente.')

def deletar_imagem(nome):
    
    # Deleta a imagem
    os.remove('./imagens/{}'.format(nome))