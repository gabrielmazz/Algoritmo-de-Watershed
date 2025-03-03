import numpy as np
from collections import deque
from PIL import Image
import imageio

# Constants
MASK = -2
WSHD = 0
INIT = -1
INQE = -3

# Neighbour (coordinates of) pixels, including the given pixel.
def _get_neighbors(height, width, pixel):
    neighbors = np.mgrid[
        max(0, pixel[0] - 1):min(height, pixel[0] + 2),
        max(0, pixel[1] - 1):min(width, pixel[1] + 2)
    ].reshape(2, -1).T
    # Remove o próprio pixel da lista de vizinhos
    neighbors = np.array([n for n in neighbors if not np.array_equal(n, pixel)])
    return neighbors

def watershed(image, levels=256):
    current_label = 0
    flag = False
    fifo = deque()

    height, width = image.shape
    total = height * width
    labels = np.full((height, width), INIT, np.int32)

    reshaped_image = image.reshape(total)
    # [y, x] pairs of pixel coordinates of the flattened image.
    pixels = np.mgrid[0:height, 0:width].reshape(2, -1).T
    # Coordinates of neighbour pixels for each pixel.
    neighbours = []
    for p in pixels:
        n = _get_neighbors(height, width, p)
        neighbours.append(n)
    # Transformar em um array numpy com padding para homogeneidade
    max_neighbors = max(len(n) for n in neighbours)
    neighbours = np.array([
        np.pad(n, ((0, max_neighbors - len(n)), (0, 0)), mode='constant', constant_values=-1)
        for n in neighbours
    ])
    neighbours = neighbours.reshape(height, width, max_neighbors, 2)

    indices = np.argsort(reshaped_image)
    sorted_image = reshaped_image[indices]
    sorted_pixels = pixels[indices]

    # levels evenly spaced steps from minimum to maximum.
    levels = np.linspace(sorted_image[0], sorted_image[-1], levels)
    level_indices = []
    current_level = 0

    # Get the indices that delimit pixels with different values.
    for i in range(total):
        if sorted_image[i] > levels[current_level]:
            # Skip levels until the next highest one is reached.
            while sorted_image[i] > levels[current_level]: current_level += 1
            level_indices.append(i)
    level_indices.append(total)

    start_index = 0
    for stop_index in level_indices:
        # Mask all pixels at the current level.
        for p in sorted_pixels[start_index:stop_index]:
            labels[p[0], p[1]] = MASK
            # Initialize queue with neighbours of existing basins at the current level.
            for q in neighbours[p[0], p[1]]:
                if q[0] == -1 or q[1] == -1:  # Ignorar vizinhos inválidos
                    continue
                if labels[q[0], q[1]] >= WSHD:
                    labels[p[0], p[1]] = INQE
                    fifo.append(p)
                    break

        # Extend basins.
        while fifo:
            p = fifo.popleft()
            # Label p by inspecting neighbours.
            for q in neighbours[p[0], p[1]]:
                if q[0] == -1 or q[1] == -1:  # Ignorar vizinhos inválidos
                    continue
                # Don't set lab_p in the outer loop because it may change.
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

        # Detect and process new minima at the current level.
        for p in sorted_pixels[start_index:stop_index]:
            # p is inside a new minimum. Create a new label.
            if labels[p[0], p[1]] == MASK:
                current_label += 1
                fifo.append(p)
                labels[p[0], p[1]] = current_label
                while fifo:
                    q = fifo.popleft()
                    for r in neighbours[q[0], q[1]]:
                        if r[0] == -1 or r[1] == -1:  # Ignorar vizinhos inválidos
                            continue
                        if labels[r[0], r[1]] == MASK:
                            fifo.append(r)
                            labels[r[0], r[1]] = current_label

        start_index = stop_index

    return labels