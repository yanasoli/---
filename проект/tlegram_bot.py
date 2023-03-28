import telebot
import os
from PIL import Image, ImageFilter
from PIL import ImageEnhance
import cv2
import numpy as np
from telebot import types
bot = telebot.TeleBot("5993831581:AAH7PiHR4m1EWArXZEuOEiQvcSitEAxoQdc")
@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "hello" or message.text == "/start" or message.text == "привет":
        bot.send_message(message.chat.id, "привет, я обрабатываю фото, отправляй фотографию", parse_mode="html")
    elif message.text == "сделай контраст":
        def contra(im):
            enh = ImageEnhance.Contrast(im)
            enh.enhance(8).save("фото/"+str(message.from_user.first_name)+"/contrast.jpg")
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        contra(im)
        bot.send_message(message.chat.id, "секундочку...", parse_mode="html")
        photo = open("фото/"+str(message.from_user.first_name)+"/contrast.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text == "сделай чёрно-белой":
        def bw(im):
            ehh = ImageEnhance.Color(im)
            ehh.enhance(0.0).save("фото/"+str(message.from_user.first_name)+"/baw.jpg")
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        bw(im)
        bot.send_message(message.chat.id, "секундочку...", parse_mode="html")
        photo = open("фото/"+str(message.from_user.first_name)+"/baw.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text == "сделай освещённой":
        def osv(im):
            ehh = ImageEnhance.Brightness(im)
            ehh.enhance(3.0).save("фото/"+str(message.from_user.first_name)+"/osv.jpg")
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        osv(im)
        bot.send_message(message.chat.id, "секундочку...", parse_mode="html")
        photo = open("фото/"+str(message.from_user.first_name)+"/osv.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text == "сделай лучше":
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        res = im.filter(ImageFilter.UnsharpMask(50,50,0))
        res = res.filter(ImageFilter.DETAIL())
        
        res.save("фото/"+str(message.from_user.first_name)+"/sh.jpg")
        bot.send_message(message.chat.id, "секундочку...", parse_mode="html")
        photo = open("фото/"+str(message.from_user.first_name)+"/sh.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text == "заблюрь":
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        res = im.filter(ImageFilter.BoxBlur(5))
        res.save("фото/"+str(message.from_user.first_name)+"/bl.jpg")
        photo = open("фото/"+str(message.from_user.first_name)+"/bl.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text =="контур":
        im = Image.open("фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg")
        res = im.filter(ImageFilter.CONTOUR())
        res.save("фото/"+str(message.from_user.first_name)+"/con.jpg")
        photo = open("фото/"+str(message.from_user.first_name)+"/con.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    elif message.text =="мультфильм":
        bot.send_message(message.chat.id, "секунду...", parse_mode="html")
        def color_quantization(img, k):
            data = np.float32(img).reshape((-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
            ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            result = result.reshape(img.shape)
            return result
        def edge_mask(img, line_size, blur_value):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray, blur_value)
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
            return edges
        full_path = "фото/"+str(message.from_user.first_name)+"/pgoto(1).jpg"
        img = cv2.imdecode(np.fromfile(full_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        line_size = 7
        blur_value = 7
        edges = edge_mask(img, line_size, blur_value)
        total_color = 9
        img = color_quantization(img, total_color)
        blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200,sigmaSpace=200)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        cv2.imwrite("k/foto.jpg", cartoon)
        photo = open("k/foto.jpg","rb")
        bot.send_photo(message.chat.id,photo)
    else:
        bot.send_message(message.chat.id, "я тебя не понимаю, напиши лучше /start", parse_mode="html")
@bot.message_handler(content_types=['photo'])
def photo(message):
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("сделай контраст")
    item2 = types.KeyboardButton("сделай чёрно-белой")
    item3 = types.KeyboardButton("сделай освещённой")
    item4 = types.KeyboardButton("сделай лучше")
    item5 = types.KeyboardButton("заблюрь")
    item6 = types.KeyboardButton("контур")
    item7 = types.KeyboardButton("мультфильм")
    murkup.add(item1,item2,item3,item4,item5,item6,item7)
    bot.send_message(message.chat.id, "выбирай, что мне с ним сделать", reply_markup=murkup)
    try:
       os.mkdir("фото/"+str(message.from_user.first_name))
    except FileExistsError:
        print("такое уже существует")
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    global src
    src = 'фото/' + str(message.from_user.first_name) +"/"+"pgoto(1).jpg"
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


bot.polling(non_stop=True)