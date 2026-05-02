import warnings
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def extract_text_from_item(item):
    """
    Extrae texto limpio desde un archivo interno XHTML del EPUB.
    """
    soup = BeautifulSoup(item.get_content(), "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n").strip()

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def export_parts_from_epub(epub_path, output_dir):
    book = epub.read_epub(epub_path)

    # Diccionario para acceder rápido a cada archivo interno por su nombre
    items_by_name = {
        item.get_name(): item
        for item in book.get_items()
        if item.get_type() == ebooklib.ITEM_DOCUMENT
    }

    partes = {
        1: {
            "titulo": "UNO",
            "archivos": [
                "Text/index_split_003.xhtml",
                "Text/index_split_004.xhtml",
                "Text/index_split_005.xhtml",
                "Text/index_split_006.xhtml",
                "Text/index_split_007.xhtml",
                "Text/index_split_008.xhtml",
                "Text/index_split_009.xhtml",
                "Text/index_split_010.xhtml",
                "Text/index_split_011.xhtml",
                "Text/index_split_012.xhtml",
            ],
        },
        2: {
            "titulo": "DOS",
            "archivos": [
                "Text/index_split_013.xhtml",
                "Text/index_split_014.xhtml",
                "Text/index_split_015.xhtml",
                "Text/index_split_016.xhtml",
                "Text/index_split_017.xhtml",
                "Text/index_split_018.xhtml",
                "Text/index_split_019.xhtml",
                "Text/index_split_020.xhtml",
                "Text/index_split_021.xhtml",
            ],
        },
        3: {
            "titulo": "TRES",
            "archivos": [
                "Text/index_split_022.xhtml",
                "Text/index_split_023.xhtml",
                "Text/index_split_024.xhtml",
                "Text/index_split_025.xhtml",
            ],
        },
        4: {
            "titulo": "CUATRO",
            "archivos": [
                "Text/index_split_026.xhtml",
                "Text/index_split_027.xhtml",
                "Text/index_split_028.xhtml",
                "Text/index_split_029.xhtml",
                "Text/index_split_030.xhtml",
                "Text/index_split_031.xhtml",
                "Text/index_split_032.xhtml",
                "Text/index_split_033.xhtml",
            ],
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    for parte_num, data in partes.items():
        textos = []

        header = (
            "Conversación en La Catedral\n"
            "Mario Vargas Llosa\n"
            f"Parte {parte_num}: {data['titulo']}\n"
            f"{'=' * 60}\n\n"
        )

        for archivo in data["archivos"]:
            item = items_by_name.get(archivo)

            if item is None:
                print(f"Advertencia: no se encontró {archivo}")
                continue

            text = extract_text_from_item(item)

            if text:
                textos.append(text)

        final_text = header + "\n\n".join(textos)

        output_file = output_dir / f"CELC_MVLL_parte{parte_num}.txt"
        output_file.write_text(final_text, encoding="utf-8")

        print(f"Parte {parte_num} exportada: {output_file}")


def main():
    epub_path = Path("data/epub/conversacion_en_la_catedral__mario_vargas_llosa.epub")
    output_dir = Path("data/txt/CELC_MVLL")

    if not epub_path.exists():
        print(f"No se encontró el EPUB: {epub_path}")
        return

    export_parts_from_epub(epub_path, output_dir)


if __name__ == "__main__":
    main()
