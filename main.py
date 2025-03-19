import matplotlib.pyplot as plt
import argparse
import Segmentation.segmentacao as segmentacao
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt
import Utils.utils_imagem as ut_img
import Utils.utils_code as ut_code
import numpy as np
import time
import Utils.library_checker as lib_checker

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')
INFO = parser.add_argument('--info', action='store_true', help='Exibir o tempo de execução')
URL_IMAGE = parser.add_argument('--url', type=str, help='URL da imagem para usar no algoritmo')

def water(imagem_escolhida, tipo, sigma, levels):
        
    tempo_inicio = time.time()
        
    with Progress() as progress:    
    
        # Adiciona uma tarefa barra de progresso
        task = progress.add_task("[cyan]Processando...", total=3)
        
        # Leitura da imagem
        progress.update(task, advance=1, description='[green]Lendo a imagem...')
        Imagem_Original = ut_img.leitura_Imagem('./imagens/{}'.format(imagem_escolhida))    

        time.sleep(1)
        
        # Filtro de Marr-Hildreth
        progress.update(task, advance=1, description='[green]Aplicando o filtro de Marr-Hildreth...')
        Imagem_Filtrada = segmentacao.watershed(Imagem_Original, sigma, levels)
        
        time.sleep(1)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - tempo_inicio - 3
        
        # Realiza a plotagem das imagens
        progress.update(task, advance=1, description='[green]Plotando as imagens...')
        ut_img.plotagem_imagem(Imagem_Original, Imagem_Filtrada)
        
    time.sleep(1)
    ut_code.clear_terminal()
        
    # Salva a imagem na pasta de resultados
    if args.url:
        ut_img.deletar_imagem(imagem_escolhida)

    if args.info:
        ut_code.print_infos_table(tempo_execucao, tipo, imagem_escolhida, sigma, levels)
        
    if args.save:
        ut_img.salvar_imagem(Imagem_Filtrada, './resultados/{}_{}_sigma_{}_levels_{}.png'.format(imagem_escolhida.split('.')[0], tipo, sigma, levels))

if __name__ == '__main__':
    
    # Verifica se o usuário passou uma URL de imagem
    args = parser.parse_args()
    
    # Verifica se todas as bibliotecas estão instaladas
    lib_checker.check_library()
    
    # Funções triviais
    ut_code.clear_terminal()
    ut_code.print_title()
    
    # Baixa a imagem da URL
    if args.url:
        ut_img.download_imagem(args)
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Otsu
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    # Define os valores de sigma e threshold
    sigma = float(Prompt.ask('\nDigite o [bold purple]valor[/bold purple] do [bold purple]sigma[/bold purple] [cyan](sigma)[/cyan] [green](default 1)[/green]', default=1))
    levels = int(Prompt.ask('Digite o [bold purple]número[/bold purple] de [bold purple]níveis[/bold purple] [cyan](levels)[/cyan] [green](default 64)[/green]', default=64))

    water(imagem_escolhida, 'watershed', sigma, levels)