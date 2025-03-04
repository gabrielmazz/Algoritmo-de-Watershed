import numpy as np
from collections import deque
from scipy.ndimage import gaussian_filter, sobel
from skimage.morphology import binary_opening

# Constants
MASK = -2
WSHD = 0
INIT = -1
INQE = -3

def _get_neighbors(height, width, pixel):
    """Retorna os vizinhos de um pixel, excluindo o próprio pixel."""
    y, x = pixel
    y_min, y_max = max(0, y - 1), min(height, y + 2)
    x_min, x_max = max(0, x - 1), min(width, x + 2)
    
    neighbors = np.mgrid[y_min:y_max, x_min:x_max].reshape(2, -1).T
    neighbors = np.array([n for n in neighbors if not np.array_equal(n, pixel)])
    return neighbors

def watershed(image, sigma=6, levels=64):
    """
    Aplica o algoritmo de watershed em uma imagem.
    
    Parâmetros:
        image: Imagem de entrada (numpy array 2D).
        sigma: Parâmetro de suavização do filtro Gaussiano (default: 1).
        levels: Número de níveis de intensidade para o watershed (default: 64).
    
    Retorna:
        labels: Matriz de rótulos resultante do watershed.
    """
    # Passo 1: Suavizar a imagem com um filtro Gaussiano
    if sigma > 0:
        image = gaussian_filter(image, sigma=sigma)
    
    height, width = image.shape
    total_pixels = height * width
    labels = np.full((height, width), INIT, dtype=np.int32)
    
    reshaped_image = image.reshape(total_pixels)
    pixels = np.mgrid[0:height, 0:width].reshape(2, -1).T
    
    # Precompute the maximum number of neighbors for padding
    max_neighbors = 8  # Máximo de vizinhos para um pixel (8 em uma grade 2D)
    neighbors = np.full((total_pixels, max_neighbors, 2), -1, dtype=np.int32)
    
    for i, p in enumerate(pixels):
        n = _get_neighbors(height, width, p)
        neighbors[i, :len(n)] = n
    
    neighbors = neighbors.reshape(height, width, max_neighbors, 2)

    # Sort pixels by intensity
    sorted_indices = np.argsort(reshaped_image)
    sorted_image = reshaped_image[sorted_indices]
    sorted_pixels = pixels[sorted_indices]

    # Create levels
    intensity_levels = np.linspace(sorted_image[0], sorted_image[-1], levels)
    level_indices = []
    current_level = 0

    # Determine the indices that separate the levels
    for i in range(total_pixels):
        if sorted_image[i] > intensity_levels[current_level]:
            while sorted_image[i] > intensity_levels[current_level]:
                current_level += 1
            level_indices.append(i)
    level_indices.append(total_pixels)

    # Initialize variables
    current_label = 0
    fifo = deque()
    start_index = 0

    for stop_index in level_indices:
        # Mask all pixels at the current level
        for p in sorted_pixels[start_index:stop_index]:
            labels[p[0], p[1]] = MASK
            for q in neighbors[p[0], p[1]]:
                if q[0] == -1 or q[1] == -1:  # Ignore invalid neighbors
                    continue
                if labels[q[0], q[1]] >= WSHD:
                    labels[p[0], p[1]] = INQE
                    fifo.append(p)
                    break

        # Extend basins
        while fifo:
            p = fifo.popleft()
            for q in neighbors[p[0], p[1]]:
                if q[0] == -1 or q[1] == -1:  # Ignore invalid neighbors
                    continue
                lab_p = labels[p[0], p[1]]
                lab_q = labels[q[0], q[1]]
                if lab_q > 0:
                    if lab_p == INQE or (lab_p == WSHD and flag):
                        labels[p[0], p[1]] = lab_q
                    elif lab_p > 0 and lab_p != lab_q:
                        labels[p[0], p[1]] = WSHD
                        flag = False
                elif lab_q == WSHD:
                    if lab_p == INQE:
                        labels[p[0], p[1]] = WSHD
                        flag = True
                elif lab_q == MASK:
                    labels[q[0], q[1]] = INQE
                    fifo.append(q)

        # Detect and process new minima at the current level
        for p in sorted_pixels[start_index:stop_index]:
            if labels[p[0], p[1]] == MASK:
                current_label += 1
                fifo.append(p)
                labels[p[0], p[1]] = current_label
                while fifo:
                    q = fifo.popleft()
                    for r in neighbors[q[0], q[1]]:
                        if r[0] == -1 or r[1] == -1:  # Ignore invalid neighbors
                            continue
                        if labels[r[0], r[1]] == MASK:
                            fifo.append(r)
                            labels[r[0], r[1]] = current_label

        start_index = stop_index

    # Passo 2: Pós-processamento para suavizar as bordas
    smoothed_labels = np.zeros_like(labels)
    for label in np.unique(labels):
        if label == WSHD:  # Ignorar a borda do watershed
            continue
        mask = (labels == label)
        mask = binary_opening(mask)  # Aplica abertura para suavizar bordas
        smoothed_labels[mask] = label

    return smoothed_labels