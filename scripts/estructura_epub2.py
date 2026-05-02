import warnings
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def clean_text_from_item(item):
    soup = BeautifulSoup(item.get_content(), "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n").strip()

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def export_epub_preview(epub_path, output_path, max_chars=800):
    book = epub.read_epub(epub_path)

    lines = []

    for i, item in enumerate(book.get_items()):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text = clean_text_from_item(item)

            lines.append(f"Índice: {i}")
            lines.append(f"Archivo interno: {item.get_name()}")
            lines.append("-" * 50)

            if text:
                lines.append(text[:max_chars])
            else:
                lines.append("[SIN TEXTO DETECTADO]")

            lines.append("\n" + "=" * 80 + "\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Vista previa exportada en: {output_path}")


def main():
    epub_path = Path("data/epub/conversacion_en_la_catedral__mario_vargas_llosa.epub")
    output_path = Path("data/txt/CLC_MVLL_preview_estructura.txt")

    if not epub_path.exists():
        print(f"No se encontró el EPUB: {epub_path}")
        return

    export_epub_preview(epub_path, output_path)


if __name__ == "__main__":
    main()
