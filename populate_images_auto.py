# populate_images_auto.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soundlab.settings")  # <-- tu settings
django.setup()



from soundlab_store.models import Product  # <-- reemplazá "soundlab_store" por tu app


# Lista de imágenes disponibles
imagenes = [
    "Amplificador Para Bajo Eléctrico 15 Watts 2 X 5 Laney LX15B.jpg",
    "Amplificador Para Guitarra 25 Watts Parlante de 8.jpg",
    "Amplificador Para Guitarra Eléctrica Combo 100W Marshall MG101CFX.jpg",
    "Auricular De Estudio Cerrados AKG K72.jpg",
    "Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M20X.jpg",
    "Auriculares De Estudio Profesional AUDIO TECHNICA ATH-M50X.jpg",
    "Bajo Eléctrico Pj Cort Action Bass Plus.jpg",
    "Bajo Eléctrico Precision Modern Pickguard Negro SX SBM22TS.jpg",
    "BATERIA MAPEX.jpg",
    "Guitarra Eléctrica Les Paul SX EF30-CS.jpg",
    "Guitarra Eléctrica Stratocaster SX SST62 Con Funda.jpg",
    "Guitarra Eléctrica Súper Strato Rock Newen.jpg",
    "Guitarra Electro Acústica Ecualizador Con Funda Cort AD810E-BKS.jpg",
    "Guitarra Electro Acústica Ecualizador Con Funda Cort AF510E-OP.jpg",
    "Kit Pack Micrófono Condenser Cardioide USB Maono AU-PM421.jpg",
    "Micrófono Condenser Cardioide Estudio Profesional AUDIO TECHNICA AT2020.jpg",
    "Micrófono Dinámico Cardioide Estudio Podcast XLR USB Con Control De Volumen Shure MV7+K.jpg",
    "MONITOR GENELEC 8010A.jpg",
    "MONITORES MACKIE CR3-X (AR).jpg",
    "MonitoresKRK.jpg",
    "Pack Placa De Audio 2 Entradas 2 Salidas USB 24-Bits M-AUDIO AIR192X4 Studio Pro.jpg",
    "Piano Eléctrico 88 Teclas Pesadas Con Sistema GHS YU 8 Octavas FUENTE YAMAHA P45B.jpg",
    "PIONEER CDJ 900 NXS.jpg",
    "PIONEER DDJ 200.jpg",
    "PIONEER DDJ 800.jpg",
    "PIONEER DJM 750 MK2.jpg",
    "Placa De Audio 4 Entradas (2 líneas) 2 Salidas USB 24-Bits Con MIDI M-AUDIO AIR192X6.jpg",
    "Placa de audio FOCUSRITE Scarlett 2i2 – 3ra gen.jpg",
    "Teclado 61 Teclas 5 8 Octavas 122 Sonidos.jpg",
    "YAMAHA RDRFV5HTR Bateria Acustica.jpg",
]

def asignar_imagenes():
    for producto in Product.objects.all():
        nombre_producto = producto.name.lower()
        imagen_asignada = None

        # Busca la primera imagen que contenga palabras del nombre del producto
        for img in imagenes:
            if all(word.lower() in img.lower() for word in nombre_producto.split()):
                imagen_asignada = img
                break

        # Si no se encuentra exacta, intenta coincidencia parcial con alguna palabra clave
        if not imagen_asignada:
            for img in imagenes:
                for word in nombre_producto.split():
                    if word.lower() in img.lower():
                        imagen_asignada = img
                        break
                if imagen_asignada:
                    break

        # Asigna la imagen si se encontró
        if imagen_asignada:
            producto.image = imagen_asignada
            producto.save()
            print(f"Producto '{producto.name}' -> Imagen: {producto.image}")
        else:
            print(f"No se encontró imagen para '{producto.name}'")

# Ejecutar la función
asignar_imagenes()
