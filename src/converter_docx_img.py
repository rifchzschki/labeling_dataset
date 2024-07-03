import aspose.words as aw


for i in range(1, 101):
    input = f'./output_docx/output_{i}.docx'
    doc = aw.Document(input)
    for page in range(0, doc.page_count):
        extractedPage = doc.extract_pages(page, 1)
        extractedPage.save(f"inputs_revised/input{page + 1}.jpg")
