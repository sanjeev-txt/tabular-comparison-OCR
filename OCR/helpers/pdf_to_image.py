from pdf2image import convert_from_path
from OCR.helpers.constants import doc_image_dirctory_name



def convert_pdf_in_images(path):

    with open(f"media/demo.pdf", 'wb+') as destination:
                for chunk in path.chunks():
                    destination.write(chunk)
    # path="/home/sanjeev/Desktop/projects/OCR_Projects/ESP_OCR/ocr_files/images/"
    images = convert_from_path("media/demo.pdf")
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(doc_image_dirctory_name+'page'+ str(i) +'.jpg', 'JPEG')