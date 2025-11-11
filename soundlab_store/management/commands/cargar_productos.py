from django.core.management.base import BaseCommand
from soundlab_store.models import Product, Category

PRODUCTOS = [
    {"name": "Amplificador Para Bajo Eléctrico 15 Watts 2 X 5 Laney LX15B", "price": 150000, "category": "Amplificadores", "image": "/img/Productos/Amplificador Para Bajo Eléctrico 15 Watts 2 X 5 Laney LX15B.jpg"},
    {"name": "Amplificador Para Guitarra 25 Watts Parlante de 8", "price": 130000, "category": "Amplificadores", "image": "/img/Productos/Amplificador Para Guitarra 25 Watts Parlante de 8.jpg"},
    {"name": "Amplificador Para Guitarra Eléctrica Combo 100W Marshall MG101CFX", "price": 580000, "category": "Amplificadores", "image": "/img/Productos/Amplificador Para Guitarra Eléctrica Combo 100W Marshall MG101CFX.jpg"},
    {"name": "Auricular De Estudio Cerrados AKG K72", "price": 80000, "category": "Home Studio / Auriculares", "image": "/img/Productos/Auricular De Estudio Cerrados AKG K72.jpg"},
    {"name": "Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M20X", "price": 95000, "category": "Home Studio / Auriculares", "image": "/img/Productos/Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M20X.jpg"},
    {"name": "Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M50X", "price": 180000, "category": "Home Studio / Auriculares", "image": "/img/Productos/Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M50X.jpg"},
    {"name": "Bajo Eléctrico PJ Cort Action Bass Plus", "price": 520000, "category": "Guitarras / Bajos", "image": "/img/Productos/Bajo Eléctrico PJ Cort Action Bass Plus.jpg"},
    {"name": "Bajo Eléctrico Precision Modern Pickguard Negro SX SBM23TS", "price": 510000, "category": "Guitarras / Bajos", "image": "/img/Productos/Bajo Eléctrico Precision Modern Pickguard Negro SX SBM23TS.jpg"},
    {"name": "BATERIA MAPEX PDG5254CDK Bat. Std 5 Cpos, Mapex Prodigy, 8T, Redo Madera", "price": 650000, "category": "Baterías", "image": "/img/Productos/BATERIA MAPEX.jpg"},
    {"name": "Guitarra Eléctrica Les Paul SX EF3D-CS", "price": 648000, "category": "Guitarras / Guitarras Eléctricas", "image": "/img/Productos/Guitarra Eléctrica Les Paul SX EF3D-CS.jpg"},
    {"name": "Guitarra Eléctrica Stratocaster SX SST62 Con Funda", "price": 420000, "category": "Guitarras / Guitarras Eléctricas", "image": "/img/Productos/Guitarra Eléctrica Stratocaster SX SST62 Con Funda.jpg"},
    {"name": "Guitarra Eléctrica Super Strato Rock Newen", "price": 350000, "category": "Guitarras / Guitarras Eléctricas", "image": "/img/Productos/Guitarra Eléctrica Super Strato Rock Newen.jpg"},
    {"name": "Guitarra Electro Acústica Ecualizador Con Funda Cort AD810E-BKS", "price": 400000, "category": "Guitarras / Electroacústicas", "image": "/img/Productos/Guitarra Electro Acústica Ecualizador Con Funda Cort AD810E-BKS.jpg"},
    {"name": "Guitarra Electro Acústica Ecualizador Con Funda Cort AF510E-OP", "price": 390000, "category": "Guitarras / Electroacústicas", "image": "/img/Productos/Guitarra Electro Acústica Ecualizador Con Funda Cort AF510E-OP.jpg"},
    {"name": "Kit Pack Micrófono Condenser Cardioide USB Maono AU-PM421", "price": 140000, "category": "Home Studio / Micrófonos", "image": "/img/Productos/Kit Pack Micrófono Condenser Cardioide USB Maono AU-PM421.jpg"},
    {"name": "Micrófono Condenser Cardioide Estudio Profesional AUDIO TECHNICA AT2020", "price": 160000, "category": "Home Studio / Micrófonos", "image": "/img/Productos/Micrófono Condenser Cardioide Estudio Profesional AUDIO TECHNICA AT2020.jpg"},
    {"name": "Micrófono Dinámico Cardioide Estudio Podcast XLR USB Con Control De Volumen Shure MV7+K", "price": 200000, "category": "Home Studio / Micrófonos", "image": "/img/Productos/Micrófono Dinámico Cardioide Estudio Podcast XLR USB Con Control De Volumen Shure MV7+K.jpg"},
    {"name": "MONITOR GENELEC 8010A", "price": 260000, "category": "Home Studio / Monitores", "image": "/img/Productos/MONITOR GENELEC 8010A.jpg"},
    {"name": "Monitores de Estudio Activos KRK CI5 G3 Rokit 5", "price": 310000, "category": "Home Studio / Monitores", "image": "/img/Productos/MonitoresKRK.JPG"},
    {"name": "MONITORES MACKIE CR3-X (AR)", "price": 270000, "category": "Home Studio / Monitores", "image": "/img/Productos/MONITORES MACKIE CR3-X (AR).jpg"},
    {"name": "Pack Placa De Audio 2 Entradas 2 Salidas USB 24-Bits M-AUDIO AIR192X4 Studio Pro", "price": 220000, "category": "Home Studio / Placas de Audio", "image": "/img/Productos/Pack Placa De Audio 2 Entradas 2 Salidas USB 24-Bits M-AUDIO AIR192X4 Studio Pro.jpg"},
    {"name": "Piano Eléctrico 88 Teclas Pesadas Con Sistema GHS 7u 8 Octavas FUENTE YAMAHA P45B", "price": 950000, "category": "Teclados", "image": "/img/Productos/Piano Eléctrico 88 Teclas Pesadas Con Sistema GHS 7u 8 Octavas FUENTE YAMAHA P45B.jpg"},
    {"name": "PIONEER CDJ 900 NXS", "price": 1350000, "category": "Controladores DJ", "image": "/img/Productos/PIONEER CDJ 900 NXS.jpg"},
    {"name": "PIONEER DDJ 200", "price": 450000, "category": "Controladores DJ", "image": "/img/Productos/PIONEER DDJ 200.jpg"},
    {"name": "PIONEER DDJ 800", "price": 850000, "category": "Controladores DJ", "image": "/img/Productos/PIONEER DDJ 800.jpg"},
    {"name": "PIONEER DJM 750 MK2", "price": 1100000, "category": "Controladores DJ", "image": "/img/Productos/PIONEER DJM 750 MK2.jpg"},
    {"name": "Placa De Audio 4 Entradas (2 líneas) 2 Salidas USB 24-Bits Con Midi M-AUDIO AIR192X6", "price": 270000, "category": "Home Studio / Placas de Audio", "image": "/img/Productos/Placa De Audio 4 Entradas (2 líneas) 2 Salidas USB 24-Bits Con Midi M-AUDIO AIR192X6.jpg"},
    {"name": "Placa de audio FOCUSRITE Scarlett 2i2 – 3ra gen", "price": 320000, "category": "Home Studio / Placas de Audio", "image": "/img/Productos/Placa de audio FOCUSRITE Scarlett 2i2 – 3ra gen.jpg"},
    {"name": "Teclado 61 Teclas 5 8 Octavas 122 Sonidos", "price": 420000, "category": "Teclados", "image": "/img/Productos/Teclado 61 Teclas 5 8 Octavas 122 Sonidos.jpg"},
    {"name": "YAMAHA RDP0F5HTR Bateria Acustica", "price": 720000, "category": "Baterías", "image": "/img/Productos/YAMAHA RDP0F5HTR Bateria Acustica.jpg"},
]

class Command(BaseCommand):
    help = 'Carga productos iniciales con sus categorías'

    def handle(self, *args, **kwargs):
        for p in PRODUCTOS:
            category_name = p["category"]
            category, _ = Category.objects.get_or_create(name=category_name)

            Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "price": p["price"],
                    "category": category,
                    "image": p["image"]
                }
            )
        self.stdout.write(self.style.SUCCESS('✅ Productos y categorías cargados correctamente'))

