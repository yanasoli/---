from PIL import Image, ImageFilter
from PIL import ImageEnhance

im = Image.open("фото\prprprpr\pgoto(1).jpg")
res = im.filter(ImageFilter.SMOOTH_MORE())
res.save("фото\prprprpr/file_5.jpg")



