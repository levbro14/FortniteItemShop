from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import requests
import json
from datetime import date
import crayons
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

today = date.today()

day = today.strftime("Item Shop - %b %d, %Y")

def getShop():
    
    shop = []
    rawEntries = []

    url = "https://fortniteapi.io/v2/shop"

    querystring = {"lang":"ru","renderData":"true"}

    auth = "8b51be2d-db634a1e-7603810f-980ab67f"
    headers = {
        'authorization': auth,
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        data = json.loads(response.text)

        storeItems = data['shop']

    except:
        shop = None
        return shop

    for i in storeItems:
        item = {}
        item['name'] = i['displayName']
        item['price'] = i['price']['finalPrice']
        item['rarity'] = i['rarity']['id']
        item['images'] = {}
        item['images']['icon'] = i['displayAssets'][0]['url']
        item['images']['background'] = i['displayAssets'][0]['url']
        item['size'] = i['tileSize']
        item['section'] = i['section']['name']
        rawEntries.append(item)


    sections = []
    for i in rawEntries:
        if i['section'] not in sections:
            sections.append(i['section'])

    for i in sections:
        section = {}
        section['name'] = i
        section['entries'] = []

        shop.append(section)

    for r in rawEntries:
        for i in shop:
            if(r['section'] == i['name']):
                i['entries'].append(r)

    return shop

def printShop(shop):
    for i in shop:
        print(i)


def makeImage(shop):
    width = 0
    ad1 = "                       !"
    ad2 = "                       !"
    if not shop:
        print("Пожалуйста, укажите правильный fortniteapi.io токен авторизации! Вы можете получить его здесь: https://dashboard.fortniteapi.io/")
        time.sleep(10)
        return None
    for j in shop:
        w = 250
        for i in j['entries']:
            if (i['size'] == "DoubleWide"):
                w += 1060
            elif (i['size'] == "Small"):
                w += 250
            elif (i['size'] == "Normal"):
                w += 500
            else: 
                w += 500
            w += 60

        if (w > width):
            width = w


    height = (len(shop) * 1600)
    print(f"Размер изображения магазина: {width} x {height}")

    sectionY = 600

    img = Image.new('RGB', (width, height), color = (22, 112, 222))

    W = img.width
    H = img.height 
    
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("fortnitebattlefest.ttf", 300)

    w, h = draw.textsize(day, font=font)
    centerW = (W-w)/2
    draw.text((centerW,150), day, fill="white", font=font)
    font = ImageFont.truetype("fortnitebattlefest.ttf", 250)
    w, h = draw.textsize(ad1, font=font)
    draw.text((width-w-100,650), ad1, fill="white", font=font)
    font = ImageFont.truetype("fortnitebattlefest.ttf", 200)
    w, h = draw.textsize(ad2, font=font)
    draw.text((width-w-100,950), ad2, fill="white", font=font)
    
    for i in shop:
        data = i['entries']
        if(i['name']):
            section = i['name']
            print(crayons.blue("Создание вкладки: " + section))
            font = ImageFont.truetype("fortnitebattlefest.ttf", 125)
            w, h = draw.textsize(section, font=font)
            W = (W-w)
            clock = Image.open("./assets/clockicon.png")
            clock = clock.resize((clock.width*2, clock.height*2))
            draw.text((185, sectionY), section, fill="white", font=font)
            img.paste(clock, (w+200, sectionY-10), clock)

        
        itemY = sectionY+160
        itemX = 185
        priceX = itemX
        size = 900

        for j in range(len(data)):
            item = data[j]
            if(j==7):
                itemY += size + 110
                itemX = 185
                sectionY += size + 100
            if(item['images']['icon']):
                url = item['images']['icon']
                itemImg = Image.open(requests.get(url, stream=True).raw)
            elif(item['images']['background']):
                url = item['images']['background']
                itemImg = Image.open(requests.get(url, stream=True).raw)
            else:
                itemImg = Image.open("./assets/placeholder.png")

            itemImg = itemImg.resize((size, size))
            
            bg = Image.open(f"./assets/rarities/{item['rarity']}.png")
            bg = bg.resize((size, size))

            down = Image.open(f"./assets/rarities/{item['rarity']}Down.png")
            down = down.resize((size, size))

            img.paste(bg, (itemX, itemY))
            img.paste(itemImg, (itemX, itemY))
            img.paste(down, (itemX, itemY), down)

            name = item['name']
            font = ImageFont.truetype("fortnitebattlefest.ttf", 75)
            nWidth, nHeight = draw.textsize(name, font=font)
            
            fsize = 60
            while (nWidth > size-20):
                fsize-=1
                font = ImageFont.truetype("fortnitebattlefest.ttf", fsize)
                nWidth, h = draw.textsize(name, font=font)

            draw.text((itemX+450-(nWidth/2), itemY+itemImg.width-125), name, fill="white", font=font)
           
            

            price = str(item['price'])
            font = ImageFont.truetype("fortnitebattlefest.ttf", 90)
            nWidth, nHeight = draw.textsize(price, font=font)
            priceX = itemX+450-(nWidth/2)
            draw.text((priceX, itemY+itemImg.width+10), price, fill="white", font=font)

            vbuck = Image.open("./assets/vbuck.png")
            vbuck = vbuck.resize((90,90))
            img.paste(vbuck, (round(priceX+nWidth+10), round(itemY+itemImg.width)), vbuck)

            itemX += itemImg.width+40
        sectionY += 1200
    font = ImageFont.truetype("fortnitebattlefest.ttf", 60)
    W = img.width
    w, h = draw.textsize("Создано: Levletsplay", font=font)
    centerW = (W-w)/2

    draw.text((centerW, img.height-100), "Создано: Levletsplay", fill="white", font=font)
    print(crayons.green("Загрузка магазина..."))
    day2 = today.strftime("%b_%d_%Y")
    print(crayons.green("Магазин сгенерирован!"))
    try:
        img.save(f"itemshop_{day2}.png", "JPEG", optimize = True, quality = 25)
        print(crayons.green(f"Изображение магазина сохранено как: itemshop_{day2}.png"))
    except:
        print(crayons.red("Error: Incorrect File Path (Set a file path in config.json or leave blank)"))
        img.save(f"./itemshop_{day2}.png", "JPEG", optimize = True, quality = 25)
        print(crayons.green(f"Магазин сохранен в папку по умолчанию как: itemshop_{day2}.png"))
    print(crayons.yellow(f"Создано: Levletsplay"))
    
    
    time.sleep(10)
    
makeImage(shop=getShop())