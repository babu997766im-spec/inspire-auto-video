
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import subprocess

WIDTH, HEIGHT = 720, 1280
OUTPUT = "inspire_official.mp4"

script = (
    "জীবনে যত বাধাই আসুক, কখনো হাল ছেড়ো না। "
    "আজ তুমি যত কষ্ট করছ, একদিন সেই কষ্টই "
    "তোমার সাফল্যের গল্প হয়ে উঠবে। "
    "নিজের ওপর বিশ্বাস রাখো, এগিয়ে চলো। "
    "তোমার সময়ও আসবে।"
)

print("Creating Bengali AI voice...")
tts = gTTS(text=script, lang="bn", slow=False)
tts.save("voice.mp3")

print("Creating video background...")
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
    "Stay strong.",
    "Keep believing."
]

y = 350
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
        y += 85
    else:
        y += 35

draw.text(
    (WIDTH // 2, 1100),
    "INSPIRE OFFICIAL",
    font=small_font,
    fill=(255, 210, 80),
    anchor="mm"
)

image.save("background.png")

print("Combining Bengali voice and video...")
subprocess.run([
    "ffmpeg", "-y",
    "-loop", "1",
    "-i", "background.png",
    "-i", "voice.mp3",
    "-c:v", "libx264",
    "-tune", "stillimage",
    "-c:a", "aac",
    "-b:a", "128k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    "-movflags", "+faststart",
    OUTPUT
], check=True)

print("Video created:", OUTPUT)
