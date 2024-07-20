

import pygame
import random
import math
import time

pygame.init()


# Here we are creating a class DrawInformation to store a global_variable (global value) like background color, font_type, font_size, etc. that will be used in the entire program easily.

# In this DrawInformation class, we will be setting up the pygame window and list(array) that will be used for visualization.

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    VIOLET = 127, 0, 255
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150
    BOTTOM_PAD = 30  # Added bottom padding

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode(
            (width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD - self.BOTTOM_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

# Initially, this draw() funtion helps to display the unsorted list(array) on the screen and it also display every control type on screen.

def draw(draw_info, algo_name, ascending, time_taken=None):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start Sorting | P - Pause/Resume | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(
        controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(
        sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    if time_taken is not None:
        time_display = draw_info.FONT.render(
            f"Time Taken: {time_taken:.4f} seconds", 1, draw_info.RED)
        draw_info.window.blit(
            time_display, (draw_info.width/2 - time_display.get_width()/2, 105))

    draw_list(draw_info)
    pygame.display.update()


#  This draw_list() function helps to draw the sorted list(array) and display for every swap() in the list(array).

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width -
                      draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD - draw_info.BOTTOM_PAD)
        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - draw_info.BOTTOM_PAD - \
            (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,
                         (x, y, draw_info.block_width, draw_info.height - draw_info.BOTTOM_PAD))

    if clear_bg:
        pygame.display.update()


#  Here we are generating our starting list(array)
#  List will depend on n = number of element, minimum_value and maximum_value

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


#  Implementing the Bubble Sort Algorithm

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN,
                          j + 1: draw_info.RED}, True)
                yield True

    return lst


#  Implementing the Insertion Sort Algorithm
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,
                      i: draw_info.RED}, True)
            yield True

    return lst



#  Implementing the Merge Sort Algorithm

def merge(draw_info, l, mid, r, ascending=True):
    lst = draw_info.lst
    an = mid - l + 1
    bn = r - mid
    a = lst[l:mid + 1]
    b = lst[mid + 1:r + 1]

    i = 0
    j = 0
    k = l

    while i < an and j < bn:
        color_positions = {k: draw_info.GREEN}
        if (a[i] < b[j] and ascending) or (a[i] > b[j] and not ascending):
            lst[k] = a[i]
            i += 1
        else:
            lst[k] = b[j]
            j += 1
        k += 1
        draw_list(draw_info, color_positions, True)
        yield True

    while i < an:
        lst[k] = a[i]
        i += 1
        k += 1
        draw_list(draw_info, {k: draw_info.RED}, True)
        yield True

    while j < bn:
        lst[k] = b[j]
        j += 1
        k += 1
        draw_list(draw_info, {k: draw_info.RED}, True)
        yield True


def merge_sort(draw_info, l, r, ascending=True):
    if l < r:
        mid = (l + r) // 2
        yield from merge_sort(draw_info, l, mid, ascending)
        yield from merge_sort(draw_info, mid + 1, r, ascending)
        yield from merge(draw_info, l, mid, r, ascending)





#  Implementing the Quick Sort Algorithm

def quick_sort(draw_info, low, high, ascending=True):
    if low < high:
        pi = yield from partition(draw_info, low, high, ascending)
        yield from quick_sort(draw_info, low, pi - 1, ascending)
        yield from quick_sort(draw_info, pi + 1, high, ascending)


def partition(draw_info, low, high, ascending=True):
    lst = draw_info.lst
    pivot = lst[high]
    i = low - 1

    for j in range(low, high):
        if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN,
                      j: draw_info.RED, high: draw_info.VIOLET}, True)
            yield True

    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_list(draw_info, {i + 1: draw_info.GREEN,
              high: draw_info.VIOLET}, True)
    yield True
    return i + 1


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1300, 720, lst)
    sorting = False
    ascending = True
    paused = False

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    time_taken = None

    while run:
        clock.tick(60)    # This will determine the speed of while_loop (speed of sorting)

        if sorting:
            try:
                if not paused:
                    next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                time_taken = time.time() - start_time
        else:
            draw(draw_info, sorting_algo_name, ascending, time_taken)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                    paused = False
                    time_taken = None
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    # Here taking note of time_taken to sort the algorithm
                    time_taken = None
                    start_time = time.time()
                    sorting_algorithm_generator = (
                        merge_sort(draw_info, 0, len(lst) - 1, ascending)
                        if sorting_algorithm == merge_sort
                        else quick_sort(draw_info, 0, len(lst) - 1, ascending)
                        if sorting_algorithm == quick_sort
                        else sorting_algorithm(draw_info, ascending)
                    )
                    paused = False
                elif event.key == pygame.K_p:
                    paused = not paused  # pause/resume
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_m and not sorting:
                    sorting_algorithm = merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pygame.K_q and not sorting:
                    sorting_algorithm = quick_sort
                    sorting_algo_name = "Quick Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
