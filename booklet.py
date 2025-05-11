#!/usr/bin/env python3
"""
booklet_impose.py

Impose an A4 PDF into A5 booklet form:
 - Scales each A4 page down to A5
 - Puts two A5 pages per A4 landscape sheet
 - Reorders pages so that, when printed double-sided, folded in half, the pages appear in correct order

Usage:
    pip install pypdf
    python booklet_impose.py "C:/path/to/input.pdf"

The script will create “input_booklet.pdf” alongside your original file.
If the number of pages in input.pdf is not a multiple of 4, blank pages will be appended.
"""
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject


def create_booklet(input_pdf: Path, output_pdf: Path) -> None:
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    # Determine original page size (A4)
    first = reader.pages[0]
    w_in = float(first.mediabox.width)
    h_in = float(first.mediabox.height)

    # Pad to multiple of 4 pages
    total_pages = len(reader.pages)
    pad = (4 - total_pages % 4) % 4
    for _ in range(pad):
        reader.add_blank_page(width=w_in, height=h_in)
    total = len(reader.pages)

    # Booklet imposition sequence
    seq = []
    for i in range(total // 4):
        seq += [total - 2*i, 1 + 2*i, 2 + 2*i, total - 1 - 2*i]

    # Sheet dims (A4 landscape) and A5 slots
    sheet_w = max(w_in, h_in)
    sheet_h = min(w_in, h_in)
    a5_w = sheet_w / 2
    a5_h = sheet_h
    scale = min(a5_w / w_in, a5_h / h_in)
    x_off_left = (a5_w - w_in * scale) / 2
    y_off = (a5_h - h_in * scale) / 2
    x_off_right = a5_w + x_off_left

    # Impose pages onto sheets
    for idx in range(0, len(seq), 2):
        sheet = PageObject.create_blank_page(width=sheet_w, height=sheet_h)
        for j in (0, 1):
            page_num = seq[idx + j] - 1
            page = reader.pages[page_num]
            tx = x_off_left if j == 0 else x_off_right
            ctm = Transformation().scale(sx=scale, sy=scale).translate(tx=tx, ty=y_off)
            sheet.merge_transformed_page(page, ctm, expand=False)
        writer.add_page(sheet)

    writer.write(str(output_pdf))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} \"C:/path/to/input.pdf\"")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists() or input_path.suffix.lower() != '.pdf':
        print("Error: input must be a valid PDF file path.")
        sys.exit(1)

    output_path = input_path.with_name(input_path.stem + '_booklet.pdf')
    create_booklet(input_path, output_path)
    print(f"Booklet PDF saved to: {output_path}")

if __name__ == '__main__':
    main()
