import pymupdf

def main():
  SRC_FILE = "pens.pdf"
  DEST_FILE = "out4.pdf"

  LETTER_WIDTH = 612
  LETTER_HEIGHT = 792

  source_doc = pymupdf.open(SRC_FILE)

  dest_doc = pymupdf.open()
  dest_page = dest_doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

  position = pymupdf.Rect(0,0, source_doc[0].rect.height, source_doc[0].rect.width)
  dest_page.show_pdf_page(position, source_doc, 0, rotate=90)

  dest_doc.save(DEST_FILE)

if __name__ == "__main__":
  main()