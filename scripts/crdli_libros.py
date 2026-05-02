import warnings
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def extract_text_from_item(item):
    soup = BeautifulSoup(item.get_content(), "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n").strip()

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def export_books_from_epub(epub_path, output_dir):
    book = epub.read_epub(epub_path)

    libros = {
        1: (10, 36),
        2: (37, 65),
        3: (66, 91),
        4: (92, 116),
        5: (117, 146),
        6: (147, 183),
        7: (184, 213),
        8: (214, 239),
        9: (240, 280),
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    for libro_num, (start_index, end_index) in libros.items():
        selected_texts = []

        for i, item in enumerate(book.get_items()):
            if start_index <= i <= end_index:
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    text = extract_text_from_item(item)

                    if text:
                        selected_texts.append(text)

        final_text = "\n\n".join(selected_texts)

        header = (
            f"Comentarios reales de los incas\n"
            f"Inca Garcilaso de la Vega\n"
            f"Libro {libro_num:02d}\n"
            f"{'=' * 60}\n\n"
        )

        output_file = output_dir / f"CRDLI_IGDLV_libro{libro_num:02d}.txt"
        output_file.write_text(header + final_text, encoding="utf-8")

        print(f"Libro {libro_num:02d} exportado: {output_file}")


def main():
    epub_path = Path(
        "data/epub/comentarios_reales_de_los_incas__inca_garcilaso_de_la_vega.epub"
    )
    output_dir = Path("data/capitulos/CRDLI_IGDLV")

    if not epub_path.exists():
        print(f"No se encontró el archivo EPUB: {epub_path}")
        return

    export_books_from_epub(epub_path, output_dir)


if __name__ == "__main__":
    main()
