import random
from openpyxl import load_workbook
import docx
import pdfkit
from PIL import Image
from spire.doc import *
from spire.doc.common import *
from docx2pdf import convert
from pdf2image import convert_from_path

for i in range(1, 101):
    output_docx_path = f'./output_docx/output_{i}.docx'
    document = docx.Document()
    document.LoadFromFile(output_docx_path)
    # Convert the document to a list of image streams
    image_streams = document.SaveImageToStreams(ImageType.Bitmap)

    # Save each image stream to a PNG file
    for image in image_streams:
        image_name = f"./inputs_revised/input_{i}.png"
        with open(image_name,'wb') as image_file:
            image_file.write(image.ToArray())

    # Close the document
    document.Close()
    

# def convert_docx_to_images(docx_path):
#     pdf_path = docx_path.replace('.docx', '.pdf')
#     convert(docx_path, pdf_path)
#     image = convert_from_path(pdf_path)

#     image_name = f"./inputs_revised/output_{i + 1}.png"
#     image.save(image_name, 'PNG')
    
#     os.remove(pdf_path)  # Cleanup PDF file after conversion
    
# for i in range(1, 101):
#     output_docx_path = f'./output_docx/output_{i}.docx'
#     convert_docx_to_images(output_docx_path)


