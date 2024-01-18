from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import PIL
import customtkinter
import threading
from datetime import date
import os
import requests
import webbrowser
from tkinter.messagebox import showerror, showwarning, showinfo
import json
from datetime import date
import crayons
import time
import warnings



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

today = date.today()
day = today.strftime("%b_%d_%Y")


def change_appearance_mode_event(new_scaling: str):
    if new_scaling == "Тёмная":
        customtkinter.set_appearance_mode("Dark")
    elif new_scaling == "Светлая":
        customtkinter.set_appearance_mode("Light")
    elif new_scaling == "Системная":
        customtkinter.set_appearance_mode("System")


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

def long_running_task():

    pb = customtkinter.CTkProgressBar(master=sidebar_frame, width=200, height=15)
    pb.place(x=15, y=300)
    pb.set(0)
    
    tbprogr = customtkinter.CTkTextbox(master=sidebar_frame, width=220, height=50, fg_color="transparent", font=customtkinter.CTkFont(size=13, weight="bold", family="Segui UI"))
    tbprogr.place(x=5, y=240)
    tbprogr.insert("0.0", text="Ожидание создания...")
    tbprogr.configure(state="disabled")
    
    
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    today = date.today()

    day1 = today.strftime("%d.%m.%Y")
    day = f"Магазин на {day1}"

    
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



    ad1 = ""
    ad2 = ""
    

    width = 10000
    height = (len(shop) * 2500)
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
    a = 0
    for i in shop:
        data = i['entries']
        if(i['name']):
            section = i['name']
            print(crayons.blue("Создание вкладки: " + section))
            
            tbprogr.configure(state="normal")
            tbprogr.delete("0.0", "end")
            tbprogr.insert("0.0", text=f"Создание вкладки: {section}")
            tbprogr.configure(state="disabled")
                
            font = ImageFont.truetype("fortnitebattlefest.ttf", 125)
            w, h = draw.textsize(section, font=font)
            W = (W-w)
            clock = Image.open("./assets/clockicon.png")
            clock = clock.resize((clock.width*2, clock.height*2))
            draw.text((185, sectionY), section, fill="white", font=font)
            img.paste(clock, (w+200, sectionY-10), clock)
            a += 0.05
            pb.set(a)

        itemY = sectionY+160
        itemX = 185
        priceX = itemX
        size = 900
        
        for j in range(len(data)):
            item = data[j]
            if(j==9):
                itemY += size + 110
                itemX = 185
                sectionY += size + 100
            elif(j==18):
                itemY += size + 160
                itemX = 200
                sectionY += size + 150
            elif(j==27):
                itemY += size + 210
                itemX = 215
                sectionY += size + 200
                
                
                
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
            img.paste(itemImg, (itemX, itemY), mask=itemImg.convert('RGBA'))
            img.paste(down, (itemX, itemY), down)

            name = item['name']
            font = ImageFont.truetype("fortnitebattlefest.ttf", 100)
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
            draw.text((priceX, itemY+itemImg.width - 10), price, fill="white", font=font)

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
    day2 = today.strftime("%d.%m.%Y")
    print(crayons.green("Магазин сгенерирован!"))
        
        
    tbprogr.configure(state="normal")
    tbprogr.delete("0.0", "end")
    tbprogr.insert("0.0", text="Загрузка магазина...")
    tbprogr.configure(state="disabled")
        
    try:
        img.save(f"itemshop_{day2}.png", "JPEG", optimize = True, quality = 25)
        print(crayons.green(f"Изображение магазина сохранено как: itemshop_{day2}.png"))
    except:
        print(crayons.red("Error: Incorrect File Path (Set a file path in config.json or leave blank)"))
        img.save(f"./itemshop_{day2}.png", "JPEG", optimize = True, quality = 25)
        print(crayons.green(f"Магазин сохранен в папку по умолчанию как: itemshop_{day2}.png"))
    print(crayons.yellow(f"Создано: Levletsplay"))
    pb.set(1)
    



    click()
    


task_thread = threading.Thread(target=long_running_task)
def click():
    frame.place_forget()
    scrollnews.grid_forget()
    framecosm.place_forget()
    
    day2 = today.strftime("%d.%m.%Y")
    
    if os.path.exists(f"itemshop_{day2}.png"):
        scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame_switches = []
        print("ФАЙЛ ЕСТЬ!")
        PIL.Image.MAX_IMAGE_PIXELS = None
        
        im = Image.open(f'itemshop_{day2}.png')
        width, height = im.size
        width, height = width / 13, height / 13
        logo_image = customtkinter.CTkImage(im, size=(width, height))
        
        navigation_frame_label = customtkinter.CTkLabel(master=scrollable_frame, image=logo_image, compound="center", font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        navigation_frame_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        scrollable_frame_switches.append(navigation_frame_label)

    else:
        task_thread.start()



def uistats():
    scrollable_frame.grid_forget()
    label_stats.place_forget()
    scrollnews.grid_forget()
    framecosm.place_forget()
    
    label = customtkinter.CTkLabel(master=frame, compound="center", font=customtkinter.CTkFont(size=50, weight="bold"), text="Статистика: ")
    label.place(x=340, y=50, anchor="center")
    
    Entry.place(x=200, y=150, anchor="center")
    
    label_stats.place(x=150, y=200)
    
    frame.place(x=600, y=300, anchor="center")

    def stats():
        nick = Entry.get()
        
        api_key = 'e6854e8f-b89c-4011-9a17-dcdfee426b8e'
        url = f"https://fortnite-api.com/v2/stats/br/v2?name={nick}"
        headers = {'Authorization': api_key}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        text = data.get("data")
        status = data.get("status")
        if(status != 200):
            label_stats.configure(text=f"Игрок: {nick} не найден!")
        else:
            a = data.get("data")
            acc = a.get("account")
            name = acc.get("name")
            id = acc.get("id")
            BP = a.get("battlePass")
            lvl = BP.get("level")
            percent = BP.get("progress")
            stats = a.get("stats")
            all = stats.get("all")
            overall = all.get("overall")
            score = overall.get("score")
            wins = overall.get("wins")
            top3 = overall.get("top3")
            top5 = overall.get("top5")
            top6 = overall.get("top6")
            top10 = overall.get("top10")
            top12 = overall.get("top12")
            top25 = overall.get("top25")
            kills = overall.get("kills")
            deaths = overall.get("deaths")
            kd = overall.get("kd")
            matches = overall.get("matches")
            winRate = overall.get("winRate")
            minutesPlayed = overall.get("minutesPlayed")
            playersOutlived = overall.get("playersOutlived")
            lastModified = overall.get("lastModified")
            label_stats.configure(text=f"Ваш ник: {name}\n" + f"Ваш id Epic: {id}\n" + f"Уровень бп: {lvl}| {percent}%\n" + f"Счет: {score}\n" + f"Побед: {wins}\n" + f"Топ 3: {top3}\n" + f"Топ 5: {top5}\n" + f"Топ 6: {top6}\n" + f"Топ 10: {top10}\n" + f"Топ 12: {top12}\n"
                      + f"Топ 25: {top25}\n" + f"Убийства: {kills}\n" + f"Смерти: {deaths}\n" + f"КД: {kd}\n" + f"Матчей: {matches}\n" + f"Процент победы: {winRate}\n"
                      + f"Сыгранные минуты: {minutesPlayed}\n" + f"Игроков пережил: {playersOutlived}\n" + f"Последнее обновление: {lastModified}\n")
            
    btn = customtkinter.CTkButton(master=frame, corner_radius=150, text="Найти", command=stats)
    btn.place(x=400, y=150, anchor="center")
            
    
    
def news():
    frame.place_forget()
    framecosm.place_forget()
    api_key = 'e6854e8f-b89c-4011-9a17-dcdfee426b8e'
    url = f"https://fortnite-api.com/v2/news/br?language=ru"
    headers = {'Authorization': api_key}
    response = requests.get(url, headers=headers)
    text = response.json()
    data = text.get("data")
    motds = data.get("motds")
    PIL.Image.MAX_IMAGE_PIXELS = None
    img = ""
    text = ""
    description = ""
    for i in motds:
        title = i.get("title")
        body = i.get("body")
        image = i.get("image")
        img += f"{image} "
        text += f"{title}."
        description += f"{body};"
    
        print(title + body + image)
        
    print("Изображения: " + img)
    a = 0
    url = img.split()
    for link in url:
        a += 1
        req = requests.get(link)
        file = BytesIO(req.content)
        image = customtkinter.CTkImage(Image.open(file), size=(340, 200))
        
        lbl = customtkinter.CTkLabel(master=scrollnews, image=image, compound="center", font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        lbl.grid(row=a, column=0, padx=20, pady=(20, 10), rowspan=1)
   
    titles = text.split('.')
    b = 0
    for tit in titles:
        b += 1
        lbltext = customtkinter.CTkLabel(master=scrollnews, font=customtkinter.CTkFont(size=15, weight="bold"), text=f"{tit}")
        lbltext.grid(row=b, column=0, padx=20, pady=(20, 10), rowspan=2)
        if lbltext.cget("text") == "":
            lbltext.destroy()
     

    descr = description.split(';')
    c = 0
    for i in descr:
        c += 1
        
        txtdes = customtkinter.CTkTextbox(master=scrollnews, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"), width=350, height=200, fg_color="transparent")
        txtdes.grid(row=c, column=1, padx=20, pady=(20, 10))
        txtdes.insert("0.0", f"{i}")
        txtdes.configure(state="disabled")
                
        if txtdes.compare("end-1c", "==", "1.0"):
            txtdes.destroy()
            fillframe = customtkinter.CTkFrame(master=scrollnews, width=200, height=200, fg_color="transparent")
            fillframe.grid(row=c, column=1, padx=20, pady=(20, 10))
            
            

    
    scrollnews.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

    

def donat():
    webbrowser.open_new_tab("https://www.donationalerts.com/r/levletsplay")
    showinfo(title="Информация", message="СПАСИБО!")
    

def getcosmetics():
    scrollable_frame.grid_forget()
    label_stats.place_forget()
    scrollnews.grid_forget()

    framecosm.place(x=600, y=300, anchor="center")
    
    Entrycosm.place(x=200, y=150, anchor="center")
    
    label = customtkinter.CTkLabel(master=framecosm, compound="center", font=customtkinter.CTkFont(size=50, weight="bold"), text="Поиск косметики: ")
    label.place(x=340, y=50, anchor="center")
    
    
    
    textbox_cosm.place(x=100, y=200)
    textbox_cosm.insert("0.0", f"Здесь будет косметика")
    textbox_cosm.configure(state="disabled")
    
    def getcosm():
        cosmetics = Entrycosm.get()
    

        lbl_skin = customtkinter.CTkLabel(master=framecosm, compound="center", font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        lbl_skin.place(x=100, y=300)
        
        lbl_lego = customtkinter.CTkLabel(master=framecosm, compound="center", font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        lbl_lego.place(x=400, y=300)
        
        api_key = 'e6854e8f-b89c-4011-9a17-dcdfee426b8e'
        url = f"https://fortnite-api.com/v2/cosmetics/br/search?language=ru&searchLanguage=ru&name={cosmetics}"
        headers = {'Authorization': api_key}
        response = requests.get(url, headers=headers)
        text = response.json()
        print(text)
        status = text.get("status")
        if(status != 200):
            textbox_cosm.configure(state="normal")
            textbox_cosm.delete("0.0", "end")
            textbox_cosm.insert("0.0", f"Предмет: {cosmetics} не найден. Убедитесь, что написали правильно.")
            textbox_cosm.configure(state="disabled")
        else:
            data = text.get("data")
            name = data.get("name")
            description = data.get("description")
            
            type = data.get("type")
            displayValue = type.get("displayValue")
        
            introduction = data.get("introduction")
            introduction_text = introduction.get("text")
        
            images = data.get("images")
            featured = images.get("featured")
            if featured != None:
                req = requests.get(featured)
                file = BytesIO(req.content)
                im = Image.open(file).convert('RGBA')
                img = customtkinter.CTkImage(im, size=(200, 200))
        
                lbl_skin.configure(image=img)
            else:
                icon = images.get("icon")
                req = requests.get(icon)
                file = BytesIO(req.content)
                im = Image.open(file).convert('RGBA')
                
                img = customtkinter.CTkImage(im, size=(200, 200))
        
                lbl_skin.configure(image=img)
        
            lego = images.get("lego")
            if lego != None:
                large = lego.get("large")
                req = requests.get(large)
                file = BytesIO(req.content)
                im = Image.open(file)
                img = customtkinter.CTkImage(im, size=(150, 150))
        
                lbl_lego.configure(image=img)
        
            
        
            
        
            textbox_cosm.configure(state="normal")
            textbox_cosm.delete("0.0", "end")
            textbox_cosm.insert("0.0", f"Имя: {name}\nОписание: {description}\nПоявление: {introduction_text}\nТип: {displayValue}")
            textbox_cosm.configure(state="disabled")
        
    btn = customtkinter.CTkButton(master=framecosm, corner_radius=150, text="Найти", command=getcosm)
    btn.place(x=400, y=150, anchor="center")
    
    


# configure window
app = customtkinter.CTk()
app.title("Fortnite assistent")
app.geometry(f"{1100}x{580}")
app.wm_iconbitmap("Icon.ico")


# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

# create sidebar frame with widgets
sidebar_frame = customtkinter.CTkFrame(master=app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = customtkinter.CTkLabel(master=sidebar_frame, text="Fortnite assistent", font=customtkinter.CTkFont(size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))






sidebar_button_1 = customtkinter.CTkButton(master=sidebar_frame, text="Магазин предметов", command=click, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
sidebar_button_2 = customtkinter.CTkButton(master=sidebar_frame,text="Статистика", command=uistats, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
sidebar_button_3 = customtkinter.CTkButton(master=sidebar_frame, text="Новости", command=news, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
sidebar_button_4 = customtkinter.CTkButton(master=sidebar_frame, text="Поиск косметики", command=getcosmetics, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
sidebar_button_4.grid(row=4, column=0, padx=20, pady=10, sticky="n")


image = customtkinter.CTkImage(Image.open("DonatLogo.png"), size=(15, 20))
donatbutton = customtkinter.CTkButton(master=sidebar_frame, text="Донат", command=donat, image=image)
donatbutton.grid(row=10, column=0, padx=20, pady=10)


appearance_mode_label = customtkinter.CTkLabel(master=sidebar_frame, text="Изменить тему приложения:", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(master=sidebar_frame, values=["Светлая", "Тёмная", "Системная"], command=change_appearance_mode_event, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))


scaling_label = customtkinter.CTkLabel(master=sidebar_frame, text="Масштабирование интерфейса:", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
scaling_optionemenu = customtkinter.CTkOptionMenu(master=sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"))
scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))



# set default values
appearance_mode_optionemenu.set("Системная")
scaling_optionemenu.set("100%")






scrollable_frame = customtkinter.CTkScrollableFrame(label_text="МАГАЗИН ПРЕДМЕТОВ", master=app, width=1000, height=1000, label_anchor="center")
frame = customtkinter.CTkFrame(master=app, width=650, height=650, fg_color="transparent")
label_stats = customtkinter.CTkLabel(master=frame, compound="center", font=customtkinter.CTkFont(size=15, weight="bold"), text="Здесь будет ваша статистика")
Entry = customtkinter.CTkEntry(master=frame, placeholder_text="Введите ник Epic", width=180, height=30)
scrollnews = customtkinter.CTkScrollableFrame(label_text="НОВОСТИ", master=app, width=1000, height=1000, label_anchor="center")
framecosm = customtkinter.CTkFrame(master=app, width=650, height=650, fg_color="transparent")
Entrycosm = customtkinter.CTkEntry(master=framecosm, placeholder_text="Введите название предмета", width=250, height=30)
textbox_cosm = customtkinter.CTkTextbox(master=framecosm, font=customtkinter.CTkFont(size=15, weight="bold", family="Arial"), width=500, height=500, fg_color="transparent")




app.mainloop()
