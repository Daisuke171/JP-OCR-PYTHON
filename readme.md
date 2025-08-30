# 🖥️ Live Japanese OCR Translator

Este proyecto permite **capturar texto en japonés desde la pantalla**, reconocerlo con **OCR**, convertirlo a **romaji** y traducirlo automáticamente al inglés (o a otro idioma).  
La base del código está inspirada en **Linkfy**.

---

## ✨ Características

- 📸 Captura un área específica de la pantalla en tiempo real.
- 🔎 Reconocimiento de texto japonés con **Tesseract OCR**.
- 🔤 Conversión a **romaji** usando [cutlet](https://github.com/polm/cutlet).
- 🌍 Traducción automática mediante [translators](https://pypi.org/project/translators/).
- 🪟 Interfaz simple con **wxPython** para seleccionar el área de captura.
- ⚡ Actualización en vivo con muy baja latencia.

---

## 📦 Requisitos

Asegúrate de tener instalado:

- **Python 3.8+**
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) con soporte para japonés (`jpn.traineddata`).

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

1. Clona este repositorio o descarga los archivos.
2. Lanza el programa:

```bash
python main.py
```

3. Aparecerá una pequeña ventana transparente con un botón.

4. Haz clic en el botón para iniciar la traducción.
    - El programa tomará el área del botón como zona de captura.
    - El texto detectado aparecerá en consola con:
        - 🗨️ Texto original en japonés.
        - 👀 Romaji.

---

## 🙌 Créditos
- OCR: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract?utm_source=chatgpt.com)
- Romaji: [cutlet](https://github.com/polm/cutlet?utm_source=chatgpt.com)
- Traduccion: [translators](https://pypi.org/project/translators/?utm_source=chatgpt.com)
- GUI: [wxPython](https://wxpython.org/?utm_source=chatgpt.com)

---

#### 💡 Base del código: Linkfy