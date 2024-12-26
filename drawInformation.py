import random
import pygame
pygame.init()
class DrawInformation:
    # define constants
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    DARK_GRAY = 128, 128, 128
    MEDIUM_GRAY = 160, 160, 160
    LIGHT_GRAY = 192, 192, 192
    
    
    BACKGROUND_COLOR = WHITE


    GRADIENTS = [
        DARK_GRAY, 
        MEDIUM_GRAY,
        LIGHT_GRAY
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
  

    SIDE_PAD = 100 # Padding from left and right edges of the window
    TOP_PAD = 150 # Padding from top of window

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Initialize display of window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    # Set the list and calculate the width and height of each bar 
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) # get min value of list
        self.max_val = max(lst) # get max value of list

        # Calculate width and height of each bar based on number of elements in list, size of window, and range of elements in the list
        self.block_width = (self.width - self.SIDE_PAD) // len(lst)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

# Generate a list of random integers
def generate_starting_list(n, min, max):
    lst = []
    for i in range(n):
        val = random.randint(min, max)
        lst.append(val)

    return lst

# Draw the visualizer elements on the screen
def draw(draw_info, algo_name, ascending):
    # Fill background
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Draw title of algorithm
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    
    # Draw instructions for sorting, resetting, switching order
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    # Draw instructions for different algorithms
    sorts = draw_info.FONT.render("B | Bubble Sort | I - Insertion Sort | M - Merge Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorts, (draw_info.width // 2 - sorts.get_width() // 2, 75))

    more_sorts = draw_info.FONT.render("Q | Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(more_sorts, (draw_info.width // 2 - more_sorts.get_width() // 2, 105))

    draw_list(draw_info)
    pygame.display.update()


# Draw the list of bars on the screen
def draw_list(draw_info, color_positions = {}, clear_bg=False):
    lst = draw_info.lst

    # Clear the background if clear_bg is true
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    # Loop through the list to get the starting x and y of each bar
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        # Rotate through different shades of gray
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]
        
        # Draw the bar (a rectangle)
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()



# Bubble sort algorithm implementation
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    # Loop through list in reverse order
    for i in range(len(lst)-1, -1, -1):
        # Compare each pair of adjacent elements from beginning to i
        for j in range(1, i + 1):
            # Check if elements should be swapped based on sorting order
            if (lst[j-1] > lst[j] and ascending) or (lst[j-1] < lst[j] and not ascending):
                # Swap elements
                temp = lst[j-1]
                lst[j-1] = lst[j]
                lst[j] = temp

                # Highlight elements being compared and swapped
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst

# Insertion sort algorithm implementation
def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range (1, len(lst)):
        key = lst[i] # The element to be inserted into the sorted portion
        j = i
        if ascending:
            # Shift elements larger than key to the right
            while j > 0 and lst[j - 1] > key:
                lst[j] = lst[j - 1]
                j = j - 1
                lst[j] = key # Insert key at correct position

                # Highlight elements being compared during insertion
                draw_list(draw_info, {j - 1: draw_info.GREEN, j: draw_info.RED}, True)
                yield True
        else:
            # Shift elements smaller than key to the right for descending order
            while j > 0 and lst[j-1] < key:
                lst[j] = lst[j-1]
                j = j-1 
                lst[j] = key # Insert key at correct position
                draw_list(draw_info, {j - 1: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

    return lst


# Merge sort algorithm implementation
def merge_sort(draw_info, ascending = True):
    lst = draw_info.lst
    # Call recursive helper function
    yield from merge_sort_helper(draw_info, lst, 0, len(lst) - 1, ascending)


def merge_sort_helper(draw_info, lst, left, right, ascending):
    # Base case: if length of list is 1, don't split further
    if left < right:
        middle = (left + right) // 2

        # Recursively sort left half
        yield from merge_sort_helper(draw_info, lst, left, middle, ascending)
        # Recursively sort right half
        yield from merge_sort_helper(draw_info, lst, middle + 1, right, ascending)
        # Merge halves after sorting
        yield from merge(draw_info, lst, left, middle, right, ascending)
    


def merge(draw_info, lst, left, middle, right, ascending):
    # Create lists to hold each half
    left_half = lst[left : middle + 1]
    right_half = lst[middle + 1 : right + 1]

    i = 0 # Index for left half
    j = 0 # Index for right half
    k = left # Index for main list

    # Merge two halves to original lists
    while i < len(left_half) and j < len(right_half):
        if(left_half[i] < right_half[j] and ascending) or (left_half[i] > right_half[j] and not ascending):
            lst[k] = left_half[i]
            i += 1
        else:
            lst[k] = right_half[j]
            j += 1
        k += 1
        # Visualize merge
        draw_list(draw_info, {k: draw_info.GREEN, k-1: draw_info.RED}, True)
        yield True

    # Copy remaining elements from either half and visualize merge
    while i < len(left_half):
        lst[k] = left_half[i]
        i += 1
        k += 1
        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True

    while j < len(right_half):
        lst[k] = right_half[j]
        j += 1
        k += 1
        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True
    
    

# Selection sort algorithm implementation
def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    # Iterate through list
    for i in range(len(lst)):
        # Get index of next left most element 
        imin = i
        # Iterate starting at next index over
        for j in range(i+1, len(lst)):
            # Find index of smallest element if ascending or largest if ascending
            if (lst[j] < lst[imin] and ascending) or (lst[j] > lst[imin] and not ascending) :
                imin = j
        # Swap next left most element with the one we found
        lst[i], lst[imin] = lst[imin], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, imin: draw_info.RED}, True)
        yield True
   
    return lst




def quick_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst) - 1
    yield from quick_sort_helper(draw_info, lst, 0, n, ascending)

def quick_sort_helper(draw_info, lst, low, high, ascending):
    if low < high:
        pi = yield from quick_sort_partition(draw_info, lst, low, high, ascending)
        yield from quick_sort_helper(draw_info, lst, low, pi - 1, ascending)
        yield from quick_sort_helper(draw_info, lst, pi + 1, high, ascending)

def quick_sort_partition(draw_info, lst, low, high, ascending):
    i = low - 1
    pivot = lst[high] 
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending) :
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            yield True
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_list(draw_info, {i+1: draw_info.GREEN, high: draw_info.RED}, True)
    yield True
    return i + 1





def main():
    run = True
    clock = pygame.time.Clock()

    n = 50 # Number of elements in list
    min = 0 # Minimum value in list
    max = 100 # Maximum value in list

    # Generate starting list
    lst = generate_starting_list(n, min, max)

    draw_info = DrawInformation(800,600, lst) # Create DrawInformation object
    sorting = False  
    ascending = True

    # Initial algorithm is bubble sort
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try: 
                # Go to next step of sorting algorithm
                next(sorting_algorithm_generator)
            except StopIteration:
                # Sorting is complete
                sorting = False
        else:
            # Draw current list and controls
            draw(draw_info, sorting_algo_name, ascending)

    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Exit loop if user closes window

            if event.type != pygame.KEYDOWN:
                continue

            # Handle key events
            if event.key == pygame.K_r and not sorting:
                # Reset list with new random values
                lst = generate_starting_list(n, min, max)
                draw_info.set_list(lst)

            elif event.key == pygame.K_SPACE and not sorting:
                # Start sorting if not already sorting
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
                
            
            elif event.key == pygame.K_d and not sorting: 
                ascending = False

            elif event.key == pygame.K_i and not sorting: 
                # Switch to insertion sort
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting: 
                # Switch to bubble sort
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_m and not sorting: 
                # Switch to merge sort
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

            elif event.key == pygame.K_s and not sorting: 
                # Switch to merge sort
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            
            elif event.key == pygame.K_q and not sorting: 
                # Switch to quick sort
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            

    pygame.quit()

if __name__ == "__main__":
    main()
        





