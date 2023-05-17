from PIL import Image
import requests
import os
Image.MAX_IMAGE_PIXELS = None


# Function to resize images
def resize_image(image_url, width):
    response = requests.get(image_url)
    image = Image.open(response.content)
    aspect_ratio = float(image.height) / float(image.width)
    height = int(width * aspect_ratio)
    return image.resize((width, height), Image.LANCZOS)

# Load all image urls from a list
image_urls = ['https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Tux.svg/300px-Tux.svg.png',
               'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/WikiProject_Zoo_Logo.svg/300px-WikiProject_Zoo_Logo.svg.png',
               'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Tux.svg/300px-Tux.svg.png']

# Resize images and store them in a list
resized_images = [resize_image(image_url, int(10 * 300)) for image_url in image_urls]

# Function to create a new canvas and reset offsets
def create_canvas():
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
    x_offset = 0
    y_offset = 0
    previous_resized_image_height = 0
    return canvas, x_offset, y_offset, previous_resized_image_height

# Create a transparent canvas
canvas_width = int(22 * 300)
canvas_height = int(99 * 300)
canvas, x_offset, y_offset, previous_resized_image_height = create_canvas()

# Initialize variables
spacing = int(0.5 * 300)
previous_resized_image_height = 0
canvas_count = 1

def save_canvas(canvas, canvas_count):
    canvas.save(f'output_{canvas_count}.png', format='PNG', dpi=(300, 300))

# Arrange images on the canvas
for resized_image in resized_images:
    if y_offset + resized_image.height > canvas_height-1500:
        save_canvas(canvas, canvas_count)
        canvas_count += 1
        canvas, x_offset, y_offset,previous_resized_image_height = create_canvas()

    if x_offset + resized_image.width > canvas_width:
        x_offset = 0
        y_offset += previous_resized_image_height + spacing
        previous_resized_image_height = 0

    canvas.paste(resized_image, (x_offset, y_offset), resized_image)
    x_offset += resized_image.width + spacing
    if previous_resized_image_height < resized_image.height:
        previous_resized_image_height = resized_image.height

# Save the last canvas
save_canvas(canvas, canvas_count)

# Download the last canvas to the web browser
webbrowser.open(f'file:///home/{os.getlogin()}/output_{canvas_count}.png')