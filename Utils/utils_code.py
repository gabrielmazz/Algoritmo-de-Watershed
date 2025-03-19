import os
from rich.console import Console
from rich.table import Table

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_title():
    console = Console()
    
    # Título
    title = '𝙰𝚕𝚐𝚘𝚛𝚒𝚝𝚖𝚘 𝚍𝚎 𝚆𝚊𝚝𝚎𝚛𝚜𝚑𝚎𝚍'
    
    subtitle = '𝚃𝚛𝚊𝚋𝚊𝚕𝚑𝚘 𝚍𝚎 𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚊𝚖𝚎𝚗𝚝𝚘 𝚍𝚎 𝙸𝚖𝚊𝚐𝚎𝚗𝚜 𝙳𝚒𝚐𝚒𝚝𝚊𝚒𝚜'
    
    # Calcula o comprimento da linha mais longa
    max_length = max(len(title), len(subtitle))
    
    # Cria a borda superior
    border_top = '┌' + '─' * (max_length + 2) + '┐'
    
    # Cria a borda inferior
    border_bottom = '└' + '─' * (max_length + 2) + '┘'
    
    # Centraliza o título e o subtítulo
    centered_title = title.center(max_length)
    centered_subtitle = subtitle.center(max_length)
    
    # Imprime a borda superior
    console.print(f'[bold purple]{border_top}[/bold purple]')
    
    # Imprime o título
    console.print(f'[bold purple]│ {centered_title} │[/bold purple]')
    
    # Imprime o subtítulo
    console.print(f'[purple]│ {centered_subtitle} │[/purple]')
    
    # Imprime a borda inferior
    console.print(f'[bold purple]{border_bottom}[/bold purple]')
    console.print('\n')
    
def print_infos_table(tempo_execucao, tipo, imagem_escolhida, sigma, levels):
    
    console = Console()
    
    # Cria uma tabela
    table = Table(title='Informações do Processamento', show_lines=True)
    
    # Adiciona as colunas
    table.add_column('Tempo de Execução', width=40, style='red')
    table.add_column('Filtro', width=40, style='cyan')
    table.add_column('Imagem Escolhida', width=40, style='blue')
    table.add_column('Sigma', width=40, style='green')
    table.add_column('Levels', width=40, style='yellow')

    # Adiciona uma única linha com todos os valores
    table.add_row(
        str(round(tempo_execucao, 2)) + 's',
        tipo,
        imagem_escolhida,
        str(sigma), 
        str(levels) 
    )
    
    # Printa a tabela
    console.print(table)