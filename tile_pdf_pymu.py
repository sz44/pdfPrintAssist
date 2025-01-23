import fitz  # PyMuPDF

def main():
    # US Letter dimensions in points
    LETTER_WIDTH = 612
    LETTER_HEIGHT = 792

    # Read source file
    source_doc = fitz.open("pens.pdf")
    source_page = source_doc[0]

    # Create a destination document
    dest_doc = fitz.open()

    # Add a blank page to the destination document
    dest_page = dest_doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

    # Copy source page to destination page, several times
    for x in range(4):
        for y in range(4):
            # Define the rectangle where the source page will be pasted
            rect = fitz.Rect(
                x * source_page.rect.width,
                y * source_page.rect.height,
                (x + 1) * source_page.rect.width,
                (y + 1) * source_page.rect.height
            )
            
            # Paste the source page into the destination page at the defined rectangle
            dest_page.show_pdf_page(rect, source_doc, 0)

    # Save the destination document
    dest_doc.save("nup-dest3.pdf")

if __name__ == "__main__":
    main()
