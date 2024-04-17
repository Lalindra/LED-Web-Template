from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__, static_url_path='/static')

# Predefined color palettes
COLOR_PALETTES = {
    "Bright Room": ["#EF476F", "#FAB151", "#06D67C", "#118ab2", "#86498E"],
    "Muted Pastel": ["#355070", "#6D597A", "#B56576", "#E56B6F", "#EAAC8B"],
    "Colourful constrasts": ["#69cc00", "#08bdbd", "#d76733", "#f21b3f", "#6d5a72"],
    "Dark but happy": ["#0b6884", "#db504a", "#dcb104", "#8b5588", "#2eb26c"],
    "When eveything pops nothing pops": ["#ffbb00", "#ff4e21", "#ff006e", "#8338ec", "#3381ff"],
    "Black Holes": ["#000000", "#000000", "#000000", "#000000", "#000000"],
    "5 shades of grey": ["#a2a2a2", "#7f7f7f", "#646464", "#363636", "#2f2f2f"],
}

# Function to generate PNG image template
def generate_image(width, height, num_horizontal, num_vertical, palette, draw_circle=True, draw_lines=True, draw_rgb_blocks=False, text_scale=0.2, border_width=3):
    image_width = width * num_horizontal
    image_height = height * num_vertical

    image = Image.new("RGB", (image_width, image_height), color="white")
    draw = ImageDraw.Draw(image)
    font_size = int(min(width, height) * text_scale)
    # font = ImageFont.truetype("arial.ttf", font_size)

     # Load Lato font
    font = ImageFont.truetype("fonts\Roboto-Medium.ttf", font_size)

    # Draw cubes
    for i in range(num_horizontal):
        start_index = i % len(palette)
        for j in range(num_vertical):
            x = i * width
            y = (num_vertical - j - 1) * height  # Adjust y-coordinate to start from bottom-most row
            # Calculate cube number in the format 'row-column'
            cube_number = f"{j + 1}-{i + 1}"
            color_index = (start_index + j) % len(palette)
            color = palette[color_index]
            draw.rectangle([x, y, x + width, y + height], fill=color, outline="white", width=1)

            # Draw RGB color blocks
            if draw_rgb_blocks:
                rgb_height = height // 15  # Height of each RGB color block
                rgb_width = width // 5  # Width of each RGB color block, equal width for all three blocks
                rgb_y = y + height - 2 * rgb_height - height // 20  # Position RGB blocks slightly above the bottom
                # Center the RGB strip horizontally
                rgb_x = x + (width - 3 * rgb_width) // 2
                draw.rectangle([rgb_x, rgb_y, rgb_x + rgb_width, rgb_y + rgb_height], fill="#FF0000")  # Red block
                draw.rectangle([rgb_x + rgb_width, rgb_y, rgb_x + 2 * rgb_width, rgb_y + rgb_height], fill="#00FF00")  # Green block
                draw.rectangle([rgb_x + 2 * rgb_width, rgb_y, rgb_x + 3 * rgb_width, rgb_y + rgb_height], fill="#0000FF")  # Blue block

            # Calculate center of the cube for text positioning
            text_bbox = draw.textbbox((0, 0), cube_number, font=font)
            text_width = text_bbox[2] - text_bbox[0]  # Right x - Left x
            text_height = text_bbox[3] - text_bbox[1]  # Bottom y - Top y
            text_x = x + (width - text_width) // 2 - text_bbox[0]
            text_y = y + (height - text_height) // 2 - text_bbox[1]
            draw.text((text_x, text_y), cube_number, fill="white", font=font)

    # Draw border
    draw.rectangle([0, 0, image_width - 1, image_height - 1], outline="white", width=border_width)

    # Calculate radius of circle
    circle_radius = min(image_width, image_height) / 2 - border_width # Adjust the fraction as needed

    # Draw circle
    if draw_circle:
        center_x = image_width // 2
        center_y = image_height // 2
        draw.ellipse([center_x - circle_radius, center_y - circle_radius, center_x + circle_radius, center_y + circle_radius], outline="white", width=2)

    # Draw lines
    if draw_lines:
        # Calculate the starting and ending points for the lines to intersect exactly in the middle of the image
        line_start = (0, 0)
        line_end = (image_width - 1, image_height - 1)
        draw.line(line_start + line_end, fill="white", width=2)
        line_start = (0, image_height - 1)
        line_end = (image_width - 1, 0)
        draw.line(line_start + line_end, fill="white", width=2)
    
    return image


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cube_width = int(request.form["cube_width"])
        cube_height = int(request.form["cube_height"])
        num_horizontal = int(request.form["num_horizontal"])
        num_vertical = int(request.form["num_vertical"])
        palette_name = request.form["palette"]
        draw_circle = "draw_circle" in request.form
        draw_lines = "draw_lines" in request.form
        draw_rgb_blocks = "draw_rgb_blocks" in request.form

        palette = COLOR_PALETTES[palette_name]

        image = generate_image(cube_width, cube_height, num_horizontal, num_vertical, palette, draw_circle, draw_lines, draw_rgb_blocks)
        image_path = f"LED_Template_{cube_width*num_horizontal}x{cube_height*num_vertical}.png"
        image.save(image_path)

        return send_file(image_path, as_attachment=True)

    return render_template("index.html", palettes=COLOR_PALETTES.keys(), COLOR_PALETTES=COLOR_PALETTES) 


if __name__ == "__main__":
    app.run(debug=True)