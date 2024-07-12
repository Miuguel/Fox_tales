from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    """
    Importa um layout de mapa a partir de um arquivo CSV.

    Args:
    - path (str): Caminho para o arquivo CSV contendo o layout do mapa.

    Returns:
    - terrain_map (list): Lista de listas representando o layout do mapa.
    Cada lista interna representa uma linha do mapa.
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    """
    Importa uma lista de superfícies (imagens) de uma pasta.

    Args:
    - path (str): Caminho para a pasta contendo as imagens.

    Returns:
    - surface_list (list): Lista de superfícies (imagens) carregadas com Pygame.
    """
    surface_list = []

    # Itera sobre os arquivos na pasta fornecida
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            # Carrega a imagem e a converte para o formato Pygame
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
