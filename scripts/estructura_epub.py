from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def export_epub_structure_to_txt(epub_path, output_path):
    book = epub.read_epub(epub_path)

    lines = []

    for i, item in enumerate(book.get_items()):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            title = soup.find(["h1", "h2", "h3"])

            title_text = title.get_text(strip=True) if title else "Sin título"

            lines.append(f"Índice: {i}")
            lines.append(f"Archivo interno: {item.get_name()}")
            lines.append(f"Título detectado: {title_text}")
            lines.append("-" * 50)

    output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Archivo exportado correctamente en: {output_path}")


def main():
    epub_path = Path("data/epub/conversacion_en_la_catedral__mario_vargas_llosa.epub")
    output_path = Path("data/txt/estructura_CELC_MVLL.txt")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    export_epub_structure_to_txt(epub_path, output_path)


if __name__ == "__main__":
    main()
