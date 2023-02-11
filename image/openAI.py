from PIL import Image

def find_shapes(image):
    # Open the image file
    img = Image.open("provinces.bmp")

    # Get the image dimensions
    width, height = img.size

    # Load the pixel data into a list
    pixels = img.load()

    # Create a list to store the shapes
    shapes = []

    # Iterate over the pixels in the image
    for x in range(width):
        for y in range(height):
            # Check if the pixel is of color [255, 255, 255]
            if pixels[x, y] == (255, 255, 255):
                # Create a new shape if this pixel is the first pixel in a new shape
                if (x, y) not in shapes:
                    shapes.append([(x, y)])
                # Otherwise, add this pixel to the existing shape
                else:
                    shape = shapes[shapes.index((x, y))]
                    shape.append((x, y))
    return shapes

# Call the function to find the shapes in the image
shapes = find_shapes("provinces.bmp")

# Print the shapes
for shape in shapes:
    print(shape)
    print("/n/n")
