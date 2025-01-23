from pypdf import PdfReader, PdfWriter, Transformation

def resize_pdf(input_path, output_path):
    """
    Copy content from an A6 PDF to the top-left corner of a US Letter size PDF.
    
    Args:
        input_path (str): Path to the input A6 PDF file
        output_path (str): Path where the new US Letter PDF will be saved
    """
    # Open the input PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # A6 dimensions in points (1 point = 1/72 inch)
    A6_WIDTH = 297.64
    A6_HEIGHT = 419.53
    
    # US Letter dimensions in points
    LETTER_WIDTH = 612
    LETTER_HEIGHT = 792
    
    # Process each page
    for page in reader.pages:
        # Create a new blank US Letter size page
        new_page = writer.add_blank_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)
        
        # Calculate scale factors to maintain aspect ratio
        # scale = min(1.0, LETTER_WIDTH/A6_WIDTH, LETTER_HEIGHT/A6_HEIGHT)
        
        # Create transformation matrix to move content to top-left corner
        # Translation is applied after scaling
        # transform = Transformation().scale(scale, scale)
        
        # Merge the original page onto the new page with transformation
        # new_page.merge_transformed_page(page, transform)
        # new_page.merge_page(page)
        new_page.merge_translated_page(page, 0, LETTER_HEIGHT - A6_HEIGHT)
    
    # Save the output PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

# Example usage
if __name__ == "__main__":
    resize_pdf("pens.pdf", "output.pdf")