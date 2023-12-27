import tkinter as tk
from io import BytesIO
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import pandas
from tkinter import PhotoImage

combobaxOyun = []
combobaxOyunLinkEpic =[]
combobaxOyunLinkSteam =[]
oyunresim="OyunLink"
def boslukbirak(boslukmiktar):
    top_padding = tk.Label(root)  # 2 piksel yükseklikle boşluk ekleyebilirsiniz.
    top_padding.pack(pady=boslukmiktar)

def steamoyunfiyatcek(oyunIndex):
    url = (combobaxOyunLinkSteam[oyunIndex])
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        title = soup.title.string
        elements_with_specific_class = soup.find_all('span', class_='big-text')
        print(title)
        return elements_with_specific_class[0].text

    else:
        print('Sayfa indirme hatası:', response.status_code)
def epicoyunfiyatcek(oyunIndex):
    url = (combobaxOyunLinkEpic[oyunIndex])
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        title = soup.title.string
        elements_with_specific_class = soup.find_all('div', class_='current-price')

        resim_etiketleri = soup.find_all('img',class_='offer-image-tall')
        for resim_etiketi in resim_etiketleri:
            resim_linki = resim_etiketi.get('src')
            global oyunresim
            oyunresim=resim_linki

        print(title)
        for element in elements_with_specific_class:
            return element.text

    else:
        print('Sayfa indirme hatası:', response.status_code)


veri = pandas.read_excel("Database.xlsx", sheet_name="Sayfa1")
combobaxOyun = veri.iloc[:, 0].tolist()
combobaxOyunLinkEpic = veri.iloc[:, 1].tolist()
combobaxOyunLinkSteam=veri.iloc[:,2].tolist()

root = tk.Tk()
arkaplan_resmi = PhotoImage(file="logo.png")
genislik, yukseklik = 200, 180
arkaplan_resmi = arkaplan_resmi.subsample(int(arkaplan_resmi.width() / genislik),
                                               int(arkaplan_resmi.height() / yukseklik))
arkaplan_etiketi = tk.Label(root, image=arkaplan_resmi)
arkaplan_etiketi.place(relwidth=1, relheight=1)
root.title("OYUN FİYAT MADENCİSİ")
root.geometry("600x700")
boslukbirak(10)

label_text = tk.StringVar()
label_text2= tk.StringVar()
label_text3= tk.StringVar()
label_image=tk.PhotoImage()
combo = ttk.Combobox(root, values=combobaxOyun)

def update_label():
    selected_item = combo.current()
    oyunFiyat=epicoyunfiyatcek(selected_item)
    oyunFiyat2=steamoyunfiyatcek(selected_item)
    fiyatEpic=float(oyunFiyat.lstrip(oyunFiyat[0]))
    fiyatSteam=float(oyunFiyat2.lstrip(oyunFiyat[0]))
    if fiyatEpic>fiyatSteam:
        label.config(fg="red")
        label2.config(fg="green")
    elif fiyatEpic==fiyatSteam:
        label.config(fg="blue")
        label2.config(fg="blue")
    label_text.set("Epic Fiyat: " + oyunFiyat)
    label_text2.set("Steam Fiyat: " + oyunFiyat2)
    label_text3.set("Oyun Adı: "+ combo.get())
    image_url = oyunresim
    response1 = requests.get(image_url)
    image_data = response1.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((200, 300))
    photo = ImageTk.PhotoImage(image)
    label5.configure(image=photo)
    label_image.configure(photo)

send_button = tk.Button(root, text="Gönder", command=update_label)
label = tk.Label(root, textvariable=label_text,fg="black")
label2 = tk.Label(root, textvariable=label_text2)
label3=tk.Label(root, textvariable=label_text3)
label5 = tk.Label(root, image=label_image)

# Arayüz elemanlarını yerleştir
combo.pack()
boslukbirak(5)
send_button.pack()
boslukbirak(10)
label.pack()
label2.pack()
label3.pack()
boslukbirak(10)
label5.pack()

root.mainloop()

