from PIL import Image, ImageDraw, ImageFont

img = Image.open('template.jpg')

d1 = ImageDraw.Draw(img)
myFont = ImageFont.truetype('LiberationMono-Bold.ttf', 72)
d1.text((265, 575), "Иванов\nИван Иванович", fill=(0, 0, 0), font=myFont, align="center")
img.show()
