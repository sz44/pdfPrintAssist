import pymupdf
import numpy as np
from PIL import Image


def find_content_bbox(page):
    """Find the bounding box of content on a page using PyMuPDF."""
    # get origianl page dimensions
    page_rect = page.rect

    # Get the page's content as an image
    pix = page.get_pixmap(matrix=pymupdf.Matrix(300 / 72, 300 / 72))  # 300 DPI
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Convert to grayscale and numpy array
    img_gray = np.array(img.convert("L"))

    # Find non-white pixels
    non_white = np.where(img_gray < 250)
    if len(non_white[0]) == 0:
        return None

    # Calculate bounding box in pixels
    top = non_white[0].min()
    bottom = non_white[0].max()
    left = non_white[1].min()
    right = non_white[1].max()


    # Calculate scaling factors based on actual page dimensions
    scale_x = page_rect.width / img_gray.shape[1]
    scale_y = page_rect.height / img_gray.shape[0]
    
    # Add padding (1mm = 2.83465 points)
    padding = 2.83465
    # padding = 0
    
    # Create bbox using page-relative coordinates
    bbox = pymupdf.Rect(
        max(0, left * scale_x - padding),
        max(0, top * scale_y - padding),  # Top margin from top of page
        min(page_rect.width, right * scale_x + padding),
        min(page_rect.height, bottom * scale_y + padding)
    )

    return bbox


def auto_crop_pdf(input_path, output_path):
    """Auto-crop PDF to content area."""
    # Open the PDF
    doc = pymupdf.open(input_path)

    page = doc[0]

    # Find content bbox
    bbox = find_content_bbox(page)

    # Set the mediabox
    # page.set_mediabox([0,0,100,100])
    
    # Set the cropbox
    page.set_cropbox(bbox)
    # Set other boxes to match cropbox
    # page.set_trimbox(bbox)
    # page.set_bleedbox(bbox)
    # page.set_artbox(bbox)

    # Save the cropped PDF
    # doc.save(output_path, clean=True, deflate=True)
    # doc.close()
    return (bbox, page)

boxes = []

def main():
    files = ["pens.pdf", "pens.pdf", "pens.pdf", "pens.pdf"]
    for file in files:
        boxes.append(auto_crop_pdf(file))

    # input_path = "pens.pdf"
    # output_path = "out2.pdf"
    # auto_crop_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
    # import sys
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py input.pdf output.pdf")
    #     sys.exit(1)

    # input_path = sys.argv[1]
    # output_path = sys.argv[2]
    # auto_crop_pdf(input_path, output_path)
