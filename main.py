
from PIL import Image, ImageDraw, ImageFont
import subprocess

WIDTH, HEIGHT = 720, 1280
OUTPUT = "inspire_official.mp4"

image = Image.new("RGB", (WIDTH, HEIGHT))
pixels = image.load()

for y in range(HEIGHT):
    for x in range(WIDTH):
        t = y / HEIGHT
        pixels[x, y] = (
            int(10 + 15 * t),
            int(18 + 10 * t),
            int(45 + 55 * t)
        )

draw = ImageDraw.Draw(image)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 43)
small_font = ImageFont.truetype(font_path, 28)

lines = [
    "NEVER GIVE UP",
    "ON YOUR DREAMS",
    "",
    "Every small step",
    "takes you closer",
    "to your goal.",
    "",
    "Stay strong.",
    "Keep believing."
]

y = 280
for line in lines:
    if line:
        box = draw.textbbox((0, 0), line, font=font)
        text_width = box[2] - box[0]
        draw.text(
            ((WIDTH - text_width) // 2, y),
            line,
            font=font,
            fill=(255, 255, 255)
        )
        y += 75
    else:
        y += 30

draw.text(
    (WIDTH // 2, 1100),
    "INSPIRE OFFICIAL",
    font=small_font,
    fill=(255, 210, 80),
    anchor="mm"
)

image.save("background.png")

subprocess.run([
    "ffmpeg", "-y",
    "-loop", "1",
    "-i", "background.png",
    "-t", "15",
    "-r", "24",
    "-vf", "format=yuv420p",
    "-c:v", "libx264",
    "-movflags", "+faststart",
    OUTPUT
], check=True)

print("Video created:", OUTPUT)
