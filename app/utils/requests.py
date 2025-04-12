import os
from datetime import datetime
from mimetypes import guess_extension

import requests
from colorama import Fore, init

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def obtener_data_img(media_id, token, numero_telefono):
    """
    Función principal que orquesta la descarga y almacenamiento de media.
    """
    media_url, mime_type = obtener_url_imagen(media_id, token)
    if media_url and mime_type:
        url = guardar_imagen(media_url, token, numero_telefono, mime_type)

        url_ocr = "http://localhost:4321/procesar-comprobante"

        try:
            with open(url, "rb") as imagen:
                files = {
                    "file": (url, imagen, "image/jpeg")
                }  # puedes ajustar el tipo MIME si es necesario
                response = requests.post(url_ocr, files=files)

            if response.status_code == 200:
                return response.json()
            else:
                print(
                    Fore.RED
                    + "ERROR:\t"
                    + Fore.WHITE
                    + f"Error en OCR: {response.status_code} - {response.content}"
                )
                return None
        except Exception as e:
            print(
                Fore.RED
                + "ERROR:\t"
                + Fore.WHITE
                + f"Error al enviar la imagen al servicio OCR: {e}"
            )
            return None
    else:
        print(
            Fore.RED
            + "ERROR:\t"
            + Fore.WHITE
            + "No fue posible obtener la URL o el tipo del archivo."
        )
        return None


def obtener_url_imagen(media_id, token):
    """
    Obtiene la URL temporal y el tipo mime de un archivo multimedia recibido en WhatsApp.
    """
    url = f"https://graph.facebook.com/v22.0/{media_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        media_data = response.json()
        media_url = media_data.get("url")
        mime_type = media_data.get("mime_type")
        return media_url, mime_type
    else:
        print(
            Fore.RED
            + "ERROR:\t"
            + Fore.WHITE
            + f"Error al obtener URL de la imagen: {response.status_code} - {response.content}"
        )
        return None, None


def guardar_imagen(media_url, token, numero_telefono, mime_type):
    """
    Descarga y guarda la imagen/media desde la URL en una carpeta local.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(media_url, headers=headers)

    if response.status_code == 200:
        # Determinar extensión desde el mime_type
        extension = guess_extension(mime_type) or ".bin"

        # Crear nombre más útil: {número}_{timestamp}.{ext}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{numero_telefono}_{timestamp}{extension}"

        os.makedirs("images", exist_ok=True)
        ruta_completa = os.path.join("images", nombre_archivo)

        with open(ruta_completa, "wb") as f:
            f.write(response.content)

        print(
            Fore.GREEN
            + "INFO:\t  "
            + Fore.WHITE
            + f"Archivo guardado como {ruta_completa}"
        )
        return ruta_completa
    else:
        print(
            Fore.RED
            + "ERROR:\t"
            + Fore.WHITE
            + f"Error al descargar el archivo: {response.status_code} - {response.content}"
        )
        return None
