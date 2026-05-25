import requests
import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import io

# ALWAYS KEEP YOUR API KEY SAFE
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"

# ─── THEMES BY WEATHER CONDITIONS ─────────────────────────────────────────────
TEMALAR = {
    "gunesli": {
        "ad": "Sunny",
        "gradient_ust": (255, 180, 40),
        "gradient_alt": (255, 120, 20),
        "panel_bg": "#c25e00",
        "panel_fg": "#fff8e1",
        "accent": "#FFD700",
        "yildiz_renk": "#FFE566",
        "tablo_bg1": "#d4700a",
        "tablo_bg2": "#b85c00",
        "baslik_bg": "#e87600",
        "emoji": "☀️",
        "particles": "sun_rays",
    },
    "bulutlu": {
        "ad": "Cloudy",
        "gradient_ust": (100, 120, 150),
        "gradient_alt": (60, 75, 100),
        "panel_bg": "#3a4a60",
        "panel_fg": "#d0dce8",
        "accent": "#8ab4d4",
        "yildiz_renk": "#a0b8cc",
        "tablo_bg1": "#2e3d52",
        "tablo_bg2": "#253245",
        "baslik_bg": "#3d5068",
        "emoji": "☁️",
        "particles": "clouds",
    },
    "yagmurlu": {
        "ad": "Rainy",
        "gradient_ust": (40, 60, 90),
        "gradient_alt": (20, 35, 60),
        "panel_bg": "#1a2a40",
        "panel_fg": "#a0c0e0",
        "accent": "#4a9fd4",
        "yildiz_renk": "#6ab0d8",
        "tablo_bg1": "#162235",
        "tablo_bg2": "#0e1a28",
        "baslik_bg": "#1e3050",
        "emoji": "🌧️",
        "particles": "rain",
    },
    "karli": {
        "ad": "Snowy",
        "gradient_ust": (200, 220, 240),
        "gradient_alt": (150, 175, 205),
        "panel_bg": "#c8d8e8",
        "panel_fg": "#1a2a3a",
        "accent": "#5080a0",
        "yildiz_renk": "#ffffff",
        "tablo_bg1": "#d5e5f0",
        "tablo_bg2": "#bfcfdf",
        "baslik_bg": "#a8c0d8",
        "emoji": "❄️",
        "particles": "snow",
    },
    "sisli": {
        "ad": "Foggy",
        "gradient_ust": (160, 165, 170),
        "gradient_alt": (100, 108, 115),
        "panel_bg": "#6a7078",
        "panel_fg": "#e8eaec",
        "accent": "#b0b8c0",
        "yildiz_renk": "#d0d5da",
        "tablo_bg1": "#585f68",
        "tablo_bg2": "#4a5058",
        "baslik_bg": "#626a72",
        "emoji": "🌫️",
        "particles": "fog",
    },
    "gece": {
        "ad": "Night",
        "gradient_ust": (15, 20, 45),
        "gradient_alt": (5, 10, 25),
        "panel_bg": "#0d1428",
        "panel_fg": "#c8d0e8",
        "accent": "#7090d0",
        "yildiz_renk": "#ffffff",
        "tablo_bg1": "#0a1020",
        "tablo_bg2": "#060c18",
        "baslik_bg": "#101830",
        "emoji": "🌙",
        "particles": "stars",
    },
    "firtinali": {
        "ad": "Stormy",
        "gradient_ust": (30, 30, 40),
        "gradient_alt": (10, 10, 20),
        "panel_bg": "#1a1a28",
        "panel_fg": "#c0c8e0",
        "accent": "#6060c0",
        "yildiz_renk": "#9090cc",
        "tablo_bg1": "#141420",
        "tablo_bg2": "#0c0c18",
        "baslik_bg": "#1e1e30",
        "emoji": "⛈️",
        "particles": "lightning",
    },
}

def icon_kod_temasi(icon_kod, durum_id):
    gece = icon_kod.endswith("n")
    if 200 <= durum_id <= 232:
        return "firtinali"
    if 300 <= durum_id <= 531:
        return "yagmurlu"
    if 600 <= durum_id <= 622:
        return "karli"
    if 700 <= durum_id <= 781:
        return "sisli"
    if durum_id == 800:
        return "gece" if gece else "gunesli"
    if 801 <= durum_id <= 804:
        return "gece" if gece else "bulutlu"
    return "gece" if gece else "gunesli"


def bulut_ikonu_olustur(boyut=64):
    img = Image.new("RGBA", (boyut, boyut), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = boyut / 64
    d.ellipse([int(8*s),  int(36*s), int(56*s), int(60*s)], fill=(0, 0, 0, 40))
    d.ellipse([int(4*s),  int(28*s), int(42*s), int(56*s)], fill=(200, 220, 255, 255))
    d.ellipse([int(18*s), int(20*s), int(50*s), int(48*s)], fill=(210, 228, 255, 255))
    d.ellipse([int(30*s), int(16*s), int(60*s), int(44*s)], fill=(220, 235, 255, 255))
    d.ellipse([int(8*s),  int(32*s), int(56*s), int(58*s)], fill=(230, 242, 255, 255))
    d.ellipse([int(20*s), int(18*s), int(44*s), int(34*s)], fill=(255, 255, 255, 160))
    return img


class Partikul:
    def __init__(self, canvas_w, canvas_h, tur):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.tur = tur
        self.id = None
        self.yenile()

    def yenile(self):
        self.x = random.uniform(0, self.canvas_w)
        self.y = random.uniform(-50, self.canvas_h)
        if self.tur == "rain":
            self.hiz_x = random.uniform(-1, -0.5)
            self.hiz_y = random.uniform(8, 14)
            self.boyut = random.uniform(1, 2)
            self.renk = random.choice(["#6ab0d8", "#4a9fd4", "#88c8e8"])
        elif self.tur == "snow":
            self.hiz_x = random.uniform(-0.5, 0.5)
            self.hiz_y = random.uniform(1.5, 4)
            self.boyut = random.uniform(3, 8)
            self.renk = random.choice(["#ffffff", "#e8f4ff", "#d0e8f8"])
        elif self.tur == "stars":
            self.x = random.uniform(0, self.canvas_w)
            self.y = random.uniform(0, self.canvas_h)
            self.hiz_x = 0
            self.hiz_y = 0
            self.boyut = random.uniform(1, 3)
            self.renk = random.choice(["#ffffff", "#ffffc0", "#c0e0ff", "#ffd0d0"])
            self.alpha = random.uniform(0.3, 1.0)
            self.delta_alpha = random.uniform(-0.02, 0.02)
        elif self.tur == "sun_rays":
            self.x = random.uniform(0, self.canvas_w)
            self.y = random.uniform(-100, 0)
            self.hiz_x = 0
            self.hiz_y = random.uniform(0.3, 0.8)
            self.boyut = random.uniform(40, 120)
            self.renk = "#FFE566"
            self.alpha = random.uniform(0.02, 0.08)
        elif self.tur == "clouds":
            self.x = random.uniform(-200, self.canvas_w)
            self.y = random.uniform(20, self.canvas_h // 2)
            self.hiz_x = random.uniform(0.2, 0.6)
            self.hiz_y = 0
            self.boyut = random.uniform(60, 150)
            self.renk = random.choice(["#9fb8cc", "#b0c5d8", "#88a8c0"])
        elif self.tur == "fog":
            self.x = random.uniform(-300, self.canvas_w)
            self.y = random.uniform(0, self.canvas_h)
            self.hiz_x = random.uniform(0.1, 0.4)
            self.hiz_y = 0
            self.boyut = random.uniform(150, 350)
            self.renk = "#c8cdd2"
        elif self.tur == "lightning":
            self.x = random.uniform(0, self.canvas_w)
            self.y = 0
            self.hiz_x = 0
            self.hiz_y = 0
            self.boyut = 3
            self.renk = "#ffffff"
            self.sure = 0
            self.maks_sure = random.randint(100, 500)


class PartikulSistemi:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_w = int(canvas["width"])
        self.canvas_h = int(canvas["height"])
        self.tur = "stars"
        self.parcaciklar = []
        self.arkaplan_id = None
        self.aktif = True
        self._gradient_img = None
        self._gradient_photo = None
        self._tema = None

    def yeniden_boyutlandir(self, w, h):
        self.canvas_w = w
        self.canvas_h = h
        self.canvas.configure(width=w, height=h)
        for p in self.parcaciklar:
            p.canvas_w = w
            p.canvas_h = h
        if self._tema:
            self._arkaplan_ciz(self._tema)

    def tema_guncelle(self, tema_adi, tema):
        self.tur = tema["particles"]
        self._tema = tema
        self.parcaciklar.clear()
        self.canvas.delete("partikul")

        n = {"rain": 80, "snow": 60, "stars": 100,
             "sun_rays": 12, "clouds": 8, "fog": 6, "lightning": 5}
        sayi = n.get(self.tur, 40)

        for _ in range(sayi):
            self.parcaciklar.append(Partikul(self.canvas_w, self.canvas_h, self.tur))

        self._arkaplan_ciz(tema)

    def _arkaplan_ciz(self, tema):
        w, h = self.canvas_w, self.canvas_h
        img = Image.new("RGB", (w, h))
        r1, g1, b1 = tema["gradient_ust"]
        r2, g2, b2 = tema["gradient_alt"]
        draw = ImageDraw.Draw(img)

        for y in range(h):
            t = y / h
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        self._gradient_img = img
        self._gradient_photo = ImageTk.PhotoImage(img)
        if self.arkaplan_id:
            self.canvas.delete(self.arkaplan_id)
        self.arkaplan_id = self.canvas.create_image(0, 0, anchor="nw",
                                                     image=self._gradient_photo,
                                                     tags="bg")
        self.canvas.tag_lower("bg")

    def guncelle(self):
        if not self.aktif:
            return
        self.canvas.delete("partikul")

        for p in self.parcaciklar:
            if self.tur == "rain":
                self.canvas.create_line(
                    p.x, p.y, p.x + p.hiz_x * 3, p.y + p.boyut * 5,
                    fill=p.renk, width=1, tags="partikul"
                )
                p.x += p.hiz_x
                p.y += p.hiz_y
                if p.y > self.canvas_h or p.x < 0:
                    p.x = random.uniform(0, self.canvas_w)
                    p.y = random.uniform(-80, -10)

            elif self.tur == "snow":
                x0, y0 = p.x - p.boyut, p.y - p.boyut
                x1, y1 = p.x + p.boyut, p.y + p.boyut
                self.canvas.create_oval(x0, y0, x1, y1,
                                        fill=p.renk, outline="", tags="partikul")
                p.x += p.hiz_x + math.sin(p.y * 0.05) * 0.4
                p.y += p.hiz_y
                if p.y > self.canvas_h:
                    p.x = random.uniform(0, self.canvas_w)
                    p.y = random.uniform(-30, -5)

            elif self.tur == "stars":
                alpha_hex = format(int(p.alpha * 255), "02x")
                self.canvas.create_oval(
                    p.x - p.boyut, p.y - p.boyut,
                    p.x + p.boyut, p.y + p.boyut,
                    fill=p.renk, outline="", tags="partikul"
                )
                p.alpha = max(0.1, min(1.0, p.alpha + p.delta_alpha))
                if random.random() < 0.01:
                    p.delta_alpha *= -1

            elif self.tur == "sun_rays":
                x0, y0 = p.x - p.boyut, p.y - p.boyut
                x1, y1 = p.x + p.boyut, p.y + p.boyut
                self.canvas.create_oval(x0, y0, x1, y1,
                                        fill=p.renk, outline="",
                                        stipple="gray12", tags="partikul")
                p.y += p.hiz_y
                if p.y > self.canvas_h + p.boyut:
                    p.x = random.uniform(0, self.canvas_w)
                    p.y = -p.boyut

            elif self.tur == "clouds":
                for dx in [-p.boyut * 0.6, 0, p.boyut * 0.6]:
                    for dy in [-p.boyut * 0.2, 0]:
                        r = p.boyut * 0.5
                        self.canvas.create_oval(
                            p.x + dx - r, p.y + dy - r,
                            p.x + dx + r, p.y + dy + r,
                            fill=p.renk, outline="",
                            stipple="gray25", tags="partikul"
                        )
                p.x += p.hiz_x
                if p.x > self.canvas_w + p.boyut:
                    p.x = -p.boyut
                    p.y = random.uniform(20, self.canvas_h // 2)

            elif self.tur == "fog":
                self.canvas.create_oval(
                    p.x - p.boyut, p.y - p.boyut * 0.3,
                    p.x + p.boyut, p.y + p.boyut * 0.3,
                    fill=p.renk, outline="",
                    stipple="gray12", tags="partikul"
                )
                p.x += p.hiz_x
                if p.x > self.canvas_w + p.boyut:
                    p.x = -p.boyut
                    p.y = random.uniform(0, self.canvas_h)

            elif self.tur == "lightning":
                p.sure += 16
                if p.sure >= p.maks_sure:
                    self._simsek_ciz(p.x)
                    p.x = random.uniform(0, self.canvas_w)
                    p.sure = 0
                    p.maks_sure = random.randint(800, 3000)

    def _simsek_ciz(self, x):
        y = 0
        pts = [(x, y)]
        while y < self.canvas_h:
            x += random.uniform(-30, 30)
            y += random.uniform(30, 60)
            pts.append((x, y))
        for i in range(len(pts) - 1):
            self.canvas.create_line(
                pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                fill="#ffffc0", width=2, tags="partikul"
            )

    def durdur(self):
        self.aktif = False

    def baslat(self):
        self.aktif = True


class HavaDurumuUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤 Weather App")
        self.root.geometry("1400x720")
        self.root.minsize(800, 480)          
        self.root.resizable(True, True)      

        self.tam_ekran = False               
        self._debounce_id = None             

        self.mevcut_tema_adi = "gece"
        self.mevcut_tema = TEMALAR["gece"]

        self._pencere_ikonu_ayarla()
        self._arayuz_olustur()

        self.root.bind("<Configure>", self._pencere_degisti)
        self.root.bind("<F11>", self._tam_ekran_toglle)
        self.root.bind("<Escape>", self._tam_ekrandan_cik)

        self._animasyon_dongusu()
        self.root.after(200, self.ara)

    def _pencere_ikonu_ayarla(self):
        try:
            icon_img = bulut_ikonu_olustur(64)
            self._icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, self._icon_photo)
        except Exception:
            pass

    def _tam_ekran_toglle(self, event=None):
        self.tam_ekran = not self.tam_ekran
        self.root.attributes("-fullscreen", self.tam_ekran)
        self.btn_tam_ekran.configure(
            text="⛶ Minimize" if self.tam_ekran else "⛶ Fullscreen"
        )

    def _tam_ekrandan_cik(self, event=None):
        if self.tam_ekran:
            self.tam_ekran = False
            self.root.attributes("-fullscreen", False)
            self.btn_tam_ekran.configure(text="⛶ Fullscreen")

    def _pencere_degisti(self, event=None):
        if event and event.widget != self.root:
            return
        if self._debounce_id:
            self.root.after_cancel(self._debounce_id)
        self._debounce_id = self.root.after(60, self._yeniden_yerles)

    def _yeniden_yerles(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 10 or h < 10:
            return

        sol_w = max(220, min(360, int(w * 0.28)))
        sag_w = w - sol_w

        self.bg_canvas.place(x=0, y=0, width=w, height=h)
        self.partikul_sistemi.yeniden_boyutlandir(w, h)

        self.panel_sol.place(x=0, y=0, width=sol_w, height=h)
        self.panel_sag.place(x=sol_w, y=0, width=sag_w, height=h)

        k = max(0.55, min(1.3, h / 720))
        self.lbl_baslik.configure(font=("Georgia", max(11, int(18 * k)), "bold"))
        self.lbl_alt_baslik.configure(font=("Georgia", max(8, int(10 * k)), "italic"))
        self.lbl_konum.configure(font=("Georgia", max(10, int(18 * k)), "bold"))
        self.lbl_sicaklik.configure(font=("Georgia", max(22, int(54 * k)), "bold"))
        self.lbl_durum.configure(font=("Georgia", max(9, int(14 * k)), "italic"))
        self.lbl_tarih.configure(font=("Segoe UI", max(7, int(10 * k))))
        self.lbl_detay.configure(font=("Segoe UI", max(7, int(10 * k))))
        self.lbl_tablo_baslik.configure(font=("Georgia", max(9, int(15 * k)), "bold"))

        entry_w = max(10, int((sol_w - 100) / 10))
        self.entry_sehir.configure(width=entry_w)

    def _arayuz_olustur(self):
        self.bg_canvas = tk.Canvas(
            self.root, width=1400, height=720,
            highlightthickness=0, bd=0
        )
        self.bg_canvas.place(x=0, y=0, width=1400, height=720)
        self.partikul_sistemi = PartikulSistemi(self.bg_canvas)
        self.partikul_sistemi.tema_guncelle("gece", TEMALAR["gece"])

        # ── Left Panel ──────────────────────────────────────────────────────────
        self.panel_sol = tk.Frame(
            self.root, bg=self.mevcut_tema["panel_bg"],
            width=360, height=720
        )
        self.panel_sol.place(x=0, y=0, width=360, height=720)
        self.panel_sol.pack_propagate(False)

        self.lbl_baslik = tk.Label(
            self.panel_sol,
            text="🌤 Weather App",
            font=("Georgia", 18, "bold"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["accent"]
        )
        self.lbl_baslik.pack(pady=(28, 4))

        self.lbl_alt_baslik = tk.Label(
            self.panel_sol, text="Enter city name",
            font=("Georgia", 10, "italic"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["panel_fg"]
        )
        self.lbl_alt_baslik.pack(pady=(0, 10))

        # Search Frame
        arama_frame = tk.Frame(self.panel_sol, bg=self.mevcut_tema["panel_bg"])
        arama_frame.pack(pady=5)

        self.entry_sehir = tk.Entry(
            arama_frame, font=("Segoe UI", 13), width=17,
            bg=self.mevcut_tema["tablo_bg1"],
            fg=self.mevcut_tema["panel_fg"],
            insertbackground=self.mevcut_tema["accent"],
            relief="flat", bd=6
        )
        self.entry_sehir.insert(0, "London")
        self.entry_sehir.pack(side="left", ipady=5)

        self.btn_ara = tk.Button(
            arama_frame, text="🔍",
            font=("Segoe UI", 13),
            bg=self.mevcut_tema["baslik_bg"],
            fg="white", relief="flat",
            activebackground=self.mevcut_tema["accent"],
            activeforeground="white",
            cursor="hand2", command=self.ara, padx=8, pady=5
        )
        self.btn_ara.pack(side="left", padx=(6, 0))
        self.entry_sehir.bind("<Return>", lambda e: self.ara())

        # Current Weather Info
        self.bilgi_frame = tk.Frame(self.panel_sol, bg=self.mevcut_tema["panel_bg"])
        self.bilgi_frame.pack(pady=15, fill="x", padx=20)

        self.lbl_icon = tk.Label(self.bilgi_frame, bg=self.mevcut_tema["panel_bg"])
        self.lbl_icon.pack()

        self.lbl_konum = tk.Label(
            self.bilgi_frame, text="—",
            font=("Georgia", 18, "bold"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["panel_fg"]
        )
        self.lbl_konum.pack(pady=(5, 0))

        self.lbl_sicaklik = tk.Label(
            self.bilgi_frame, text="—",
            font=("Georgia", 54, "bold"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["accent"]
        )
        self.lbl_sicaklik.pack()

        self.lbl_durum = tk.Label(
            self.bilgi_frame, text="—",
            font=("Georgia", 14, "italic"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["panel_fg"]
        )
        self.lbl_durum.pack()

        self.lbl_tarih = tk.Label(
            self.bilgi_frame, text="—",
            font=("Segoe UI", 10),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["accent"]
        )
        self.lbl_tarih.pack(pady=(8, 0))

        self.lbl_detay = tk.Label(
            self.bilgi_frame, text="",
            font=("Segoe UI", 10),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["panel_fg"],
            justify="left"
        )
        self.lbl_detay.pack(pady=(10, 0))

        # Bottom Bar
        alt_bar = tk.Frame(self.panel_sol, bg=self.mevcut_tema["panel_bg"])
        alt_bar.pack(side="bottom", fill="x", pady=8, padx=8)

        self.lbl_tema = tk.Label(
            alt_bar, text="",
            font=("Georgia", 11, "italic"),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["accent"]
        )
        self.lbl_tema.pack(side="left", padx=4)

        self.lbl_kisayol = tk.Label(
            alt_bar, text="F11",
            font=("Segoe UI", 8),
            bg=self.mevcut_tema["panel_bg"],
            fg=self.mevcut_tema["tablo_bg1"]
        )
        self.lbl_kisayol.pack(side="right", padx=2)

        self.btn_tam_ekran = tk.Button(
            alt_bar, text="⛶ Fullscreen",
            font=("Segoe UI", 9),
            bg=self.mevcut_tema["baslik_bg"],
            fg="white", relief="flat",
            activebackground=self.mevcut_tema["accent"],
            activeforeground="white",
            cursor="hand2",
            command=self._tam_ekran_toglle,
            padx=6, pady=3
        )
        self.btn_tam_ekran.pack(side="right", padx=(0, 3))

        # ── Right Panel ──────────────────────────────────────────────────────────
        self.panel_sag = tk.Frame(self.root, highlightthickness=0)
        self.panel_sag.place(x=360, y=0, width=1040, height=720)
        self.panel_sag.configure(bg=self.mevcut_tema["tablo_bg2"])

        self.lbl_tablo_baslik = tk.Label(
            self.panel_sag,
            text="5-Day Forecast (3-Hour Intervals)",
            font=("Georgia", 15, "bold"),
            bg=self.mevcut_tema["tablo_bg2"],
            fg=self.mevcut_tema["accent"]
        )
        self.lbl_tablo_baslik.pack(pady=(20, 8))

        self._treeview_olustur()

    def _treeview_olustur(self):
        style = ttk.Style()
        style.theme_use("clam")
        tema = self.mevcut_tema

        style.configure(
            "W.Treeview",
            rowheight=28, font=("Segoe UI", 10),
            background=tema["tablo_bg1"],
            foreground=tema["panel_fg"],
            fieldbackground=tema["tablo_bg1"]
        )
        style.configure(
            "W.Treeview.Heading",
            font=("Georgia", 11, "bold"),
            background=tema["baslik_bg"],
            foreground=tema["panel_fg"]
        )
        style.map("W.Treeview", background=[("selected", tema["accent"])])

        kolonlar = ("Date & Time", "Temp", "Feels Like",
                    "Condition", "Precipitation %", "Humidity", "Wind")

        self.tree_frame = tk.Frame(self.panel_sag, bg=tema["tablo_bg2"])
        self.tree_frame.pack(padx=15, pady=5, fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=kolonlar,
                                  show="headings", height=22,
                                  style="W.Treeview")

        genislikler = {
            "Date & Time": 120, "Temp": 100, "Feels Like": 100,
            "Condition": 200, "Precipitation %": 100, "Humidity": 80, "Wind": 110
        }
        for col in kolonlar:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=genislikler[col], anchor="center", minwidth=50)

        scroll = ttk.Scrollbar(self.tree_frame, orient="vertical",
                               command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.tag_configure("tek",
            background=tema["tablo_bg1"], foreground=tema["panel_fg"])
        self.tree.tag_configure("cift",
            background=tema["tablo_bg2"], foreground=tema["panel_fg"])

    def tema_degistir(self, tema_adi):
        if tema_adi == self.mevcut_tema_adi:
            return

        self.mevcut_tema_adi = tema_adi
        self.mevcut_tema = TEMALAR[tema_adi]
        tema = self.mevcut_tema

        self.partikul_sistemi.tema_guncelle(tema_adi, tema)

        self.panel_sol.configure(bg=tema["panel_bg"])
        for widget in [self.lbl_baslik, self.lbl_alt_baslik,
                       self.bilgi_frame, self.lbl_icon, self.lbl_konum,
                       self.lbl_sicaklik, self.lbl_durum, self.lbl_tarih,
                       self.lbl_detay, self.lbl_tema, self.lbl_kisayol]:
            try:
                widget.configure(bg=tema["panel_bg"])
            except Exception:
                pass

        self.lbl_baslik.configure(fg=tema["accent"])
        self.lbl_alt_baslik.configure(fg=tema["panel_fg"])
        self.lbl_konum.configure(fg=tema["panel_fg"])
        self.lbl_sicaklik.configure(fg=tema["accent"])
        self.lbl_durum.configure(fg=tema["panel_fg"])
        self.lbl_tarih.configure(fg=tema["accent"])
        self.lbl_detay.configure(fg=tema["panel_fg"])
        self.lbl_tema.configure(fg=tema["accent"],
            text=f"{tema['emoji']}  {tema['ad']}")
        self.lbl_kisayol.configure(fg=tema["tablo_bg1"])

        self.entry_sehir.configure(
            bg=tema["tablo_bg1"], fg=tema["panel_fg"],
            insertbackground=tema["accent"]
        )
        self.btn_ara.configure(
            bg=tema["baslik_bg"], activebackground=tema["accent"]
        )
        self.btn_tam_ekran.configure(
            bg=tema["baslik_bg"], activebackground=tema["accent"]
        )

        self.panel_sag.configure(bg=tema["tablo_bg2"])
        self.lbl_tablo_baslik.configure(bg=tema["tablo_bg2"], fg=tema["accent"])
        self.tree_frame.configure(bg=tema["tablo_bg2"])

        style = ttk.Style()
        style.configure("W.Treeview",
            background=tema["tablo_bg1"],
            foreground=tema["panel_fg"],
            fieldbackground=tema["tablo_bg1"]
        )
        style.configure("W.Treeview.Heading",
            background=tema["baslik_bg"],
            foreground=tema["panel_fg"]
        )
        style.map("W.Treeview", background=[("selected", tema["accent"])])

        self.tree.tag_configure("tek",
            background=tema["tablo_bg1"], foreground=tema["panel_fg"])
        self.tree.tag_configure("cift",
            background=tema["tablo_bg2"], foreground=tema["panel_fg"])

        for i, row in enumerate(self.tree.get_children()):
            tag = "tek" if i % 2 == 0 else "cift"
            self.tree.item(row, tags=(tag,))

    def hava_durumu_getir(self, sehir):
        # Changed language pack to English
        params = {"q": sehir, "lang": "en", "appid": API_KEY, "units": "metric"}
        try:
            veri = requests.get(BASE_URL, params=params, timeout=8).json()
        except Exception:
            messagebox.showerror("Error", "Could not connect to server.")
            return False

        if veri.get("cod") != 200:
            messagebox.showerror("Error", f"City not found: {sehir}")
            return False

        ad = veri["name"]
        ulke = veri["sys"]["country"]
        sicaklik = veri["main"]["temp"]
        hissed = round(veri["main"]["feels_like"], 1)
        nem = veri["main"]["humidity"]
        ruzgar = round(veri["wind"]["speed"] * 3.6, 1)
        icon_kod = veri["weather"][0]["icon"]
        durum_id = veri["weather"][0]["id"]
        durum = veri["weather"][0]["description"].capitalize()
        tarih = datetime.datetime.now().strftime("%B %d, %Y  %H:%M")

        yeni_tema = icon_kod_temasi(icon_kod, durum_id)
        self.tema_degistir(yeni_tema)

        self.lbl_konum["text"] = f"{ulke} / {ad}"
        self.lbl_sicaklik["text"] = f"{sicaklik:.1f}°C"
        self.lbl_durum["text"] = durum
        self.lbl_tarih["text"] = tarih
        self.lbl_detay["text"] = (
            f"💧 Humidity: {nem}%\n"
            f"🌡 Feels Like: {hissed}°C\n"
            f"💨 Wind: {ruzgar} km/h"
        )

        try:
            icon_resp = requests.get(
                ICON_URL.format(icon_kod), stream=True, timeout=6
            )
            img = Image.open(io.BytesIO(icon_resp.content)).resize((90, 90), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_icon.configure(image=photo)
            self.lbl_icon.image = photo
        except Exception:
            self.lbl_icon.configure(image="")

        return True

    def tahmin_getir(self, sehir):
        # Changed language pack to English
        params = {"q": sehir, "lang": "en", "appid": API_KEY, "units": "metric"}
        try:
            veri = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params=params, timeout=8
            ).json()
        except Exception:
            return

        if str(veri.get("cod")) != "200":
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, eleman in enumerate(veri["list"]):
            dt = datetime.datetime.fromtimestamp(eleman["dt"]).strftime("%b %d  %H:%M")
            sicaklik = f"{eleman['main']['temp']:.1f}°C"
            hissed = f"{eleman['main']['feels_like']:.1f}°C"
            aciklama = eleman["weather"][0]["description"].capitalize()
            yagis = f"{int(eleman.get('pop', 0) * 100)}%"
            nem = f"{eleman['main']['humidity']}%"
            ruzgar = f"{round(eleman['wind']['speed'] * 3.6, 1)} km/h"
            tag = "tek" if i % 2 == 0 else "cift"
            self.tree.insert("", "end",
                values=(dt, sicaklik, hissed, aciklama, yagis, nem, ruzgar),
                tags=(tag,))

        self.lbl_tablo_baslik["text"] = f"{sehir.title()} – 5-Day Forecast (3-Hour Intervals)"

    def ara(self):
        sehir = self.entry_sehir.get().strip()
        if not sehir:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return
        if self.hava_durumu_getir(sehir):
            self.tahmin_getir(sehir)

    def _animasyon_dongusu(self):
        self.partikul_sistemi.guncelle()
        self.root.after(30, self._animasyon_dongusu)


if __name__ == "__main__":
    root = tk.Tk()
    app = HavaDurumuUygulamasi(root)
    root.mainloop()