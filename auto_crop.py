import pymupdf
import numpy as np
from PIL import Image
from collections import namedtuple


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


def auto_crop_pdf(input_path):
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
    return Box(bbox, page)

Box = namedtuple('Box', ['bbox', 'page'])

class TreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box = None
        self.left = None
        self.right = None

def insert(node, box:Box):
    if not node:
        return False

    width = box.bbox.width
    height = box.bbox.height
    
    # first check if region occupied
    if node.box:
        # second check if region big enough to try sub regions
        if (node.width >= width and node.height >= width) or (node.width >= height and node.height >= width):
            return insert(node.right, box) or insert(node.left, box)

        print('could not fit box', box.bbox)
        return False
    
    if node.width >= width and node.height >= height:
        node.box = box
    elif node.width >= height and node.height >= width:
        # rotate
        x0,y0,x1,y1 = box.bbox
        new_bbox = pymupdf.Rect(x0,y0,y1,x1)

        node.box = Box(new_bbox, box.page)
    else:
        return False
    
    # create new regions
    nextWidth = node.width - box.bbox.width
    nextHeight = node.height - box.bbox.height
    if nextWidth > 0:
        node.right = TreeNode(node.x + box.bbox.width, node.y, nextWidth, box.bbox.height)
    if nextHeight > 0:
        node.left = TreeNode(node.x, node.y + box.bbox.height, node.width, nextHeight)
    
    return True

def drawToNewPage(page, root):
    def dfs(node):
        if not node or not node.box:
            return
        pos = pymupdf.Rect(node.x, node.y, node.x + node.box.bbox.width, node.y + node.box.bbox.height)
        page.show_pdf_page(pos, node.box.page.parent, 0)
        dfs(node.right)
        dfs(node.left)

    dfs(root)

def main():
    files = ["pens.pdf", "pens.pdf", "pens.pdf", "pens.pdf"]
    boxes = []
    for file in files:
        boxes.append(auto_crop_pdf(file))

    LETTER_WIDTH = 612
    LETTER_HEIGHT = 792

    root = TreeNode(0,0, LETTER_WIDTH, LETTER_HEIGHT)    
    for box in boxes:
        insert(root, box)

    print(root)

    # Create a destination document
    dest_doc = pymupdf.open()

    # Add a blank page to the destination document
    dest_page = dest_doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

    drawToNewPage(dest_page, root) 

    # Save the destination document
    dest_doc.save("out3.pdf")

    print("created new pdf: ", "out3.pdf")

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
