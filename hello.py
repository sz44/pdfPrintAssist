from pypdf import PaperSize, PdfReader, PdfWriter, Transformation

def main():
    # US Letter dimensions in points
    LETTER_WIDTH = 612
    LETTER_HEIGHT = 792

    # Read source file
    reader = PdfReader("pens.pdf")
    sourcepage = reader.pages[0]

    # Create a destination file, and add a blank page to it
    writer = PdfWriter()
    destpage = writer.add_blank_page(width=612, height=792)

    # Copy source page to destination page, several times
    for x in range(4):
        for y in range(4):
            destpage.merge_translated_page(sourcepage, x * sourcepage.mediabox.width, LETTER_HEIGHT - y * sourcepage.mediabox.height) 

    # Write file
    with open("nup-dest2.pdf", "wb") as fp:
        writer.write(fp)

if __name__ == "__main__":
    main()
