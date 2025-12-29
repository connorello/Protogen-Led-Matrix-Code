import time
import board
import neopixel

# Matrix Sizes (in pixels, (height, width))
matrix_sizes = [
    (8, 8),   # Matrix 1: 8x8
    (8, 8),   # Matrix 2: 8x8
    (32, 8),  # Matrix 3: 32x8 (already rotated)
    (8, 8),   # Matrix 4: 8x8
    (8, 8)    # Matrix 5: 8x8
]

# Total number of pixels in all matrices
total_pixels = sum([size[0] * size[1] for size in matrix_sizes])

# Function to initialize NeoPixels
def init_pixels():
    return neopixel.NeoPixel(board.D18, total_pixels, auto_write=False, pixel_order=neopixel.GRB, brightness=0.5)

# Function to display a pattern on all matrices
def display_pattern(pixels, pattern):
    pixel_offset = 0  # Offset to manage the starting point for each matrix

    for matrix_num in range(len(pattern)):
        matrix_height, matrix_width = matrix_sizes[matrix_num]  # Get matrix size

        # Check if the pattern is the correct size for the matrix
        if len(pattern[matrix_num]) != matrix_height or len(pattern[matrix_num][0]) != matrix_width:
            print(f"Matrix {matrix_num + 1} has an incorrect size!")
            return

        for y in range(matrix_height):
            for x in range(matrix_width):
                pixel_index = pixel_offset + (y * matrix_width) + x  # Calculate the correct pixel index
                if pattern[matrix_num][y][x] == 1:
                    pixels[pixel_index] = (0, 0, 255)  # White color for active pixels
                else:
                    pixels[pixel_index] = (0, 0, 0)  # Off color for inactive pixels

        # Update the offset for the next matrix
        pixel_offset += matrix_height * matrix_width

    pixels.show()  # Update the display

# Function to turn off specific matrices
def turn_off_matrices(pixels, matrix_indices):
    pixel_offset = 0
    for i, (matrix_height, matrix_width) in enumerate(matrix_sizes):
        if i in matrix_indices:
            for y in range(matrix_height):
                for x in range(matrix_width):
                    pixel_index = pixel_offset + (y * matrix_width) + x
                    pixels[pixel_index] = (0, 0, 0)  # Turn off pixels

        pixel_offset += matrix_height * matrix_width

    pixels.show()

# Function to make Matrix 1 and 5 blink
def blink_matrices(pixels, pattern, blink_on_time=0.5, blink_off_time=0.5, iterations=5):
    for _ in range(iterations):
        display_pattern(pixels, pattern)  # Turn on
        time.sleep(blink_on_time)  # Wait while on
        turn_off_matrices(pixels, [0, 4])  # Turn off Matrix 1 and 5
        time.sleep(blink_off_time)  # Wait while off


# Example pattern for 5 matrices (all blank)
pattern = [
    [  # Matrix 1: 8x8 (blank)
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [  # Matrix 2: 8x8 (blank)
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0]
    ],
    [  # Matrix 3: 32x8 (rotated manually)
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [  # Matrix 4: 8x8 (blank)
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0]
    ],
    [  # Matrix 5: 8x8 (blank)
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
]

# Initialize LEDs
pixels = init_pixels()

# Run the blinking animation for Matrix 1 and 5
blink_matrices(pixels, pattern, blink_on_time=5, blink_off_time=0.5, iterations=999999)
