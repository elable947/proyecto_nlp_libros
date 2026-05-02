import warnings
from pathlib import Path

# para trabajar con archivos .epub
import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

# ignoramos advertencias de ebooklib que suelen ser comunes al procesar EPUBs
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    text_content = []

    # Recorrer los items del libro buscando documentos HTML/XHTML
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text(separator="\n").strip()

            if text:
                text_content.append(text)
    return "\n\n".join(text_content)


def main():
    epub_dir = Path("data/epub")
    capitulos_dir = Path("data/capitulos")

    # crea carpeta de salida si no existe
    capitulos_dir.mkdir(parents=True, exist_ok=True)

    # verifica si existe la carpeta de EPUBs
    if not epub_dir.exists():
        print(f"Error: No se encontró la carpeta de origen: {epub_dir}")
        return

    # buscamos archivos .epub
    files = list(epub_dir.glob("*.epub"))

    if not files:
        print("No se encontraron archivos .epub para procesar.")
        return

    for epub_path in files:
        txt_filename = epub_path.stem + ".txt"
        txt_path = capitulos_dir / txt_filename
        print(f"Convirtiendo: {epub_path.name}...")

        try:
            content = extract_text_from_epub(epub_path)
            txt_path.write_text(content, encoding="utf-8")
            print(f"Éxito: Guardado como {txt_filename}")
        except Exception as e:
            print(f"Error al procesar {epub_path.name}: {e}")


if __name__ == "__main__":
    main()
