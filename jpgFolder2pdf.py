import re
from fpdf import FPDF
from pdf2image import convert_from_path
import os
from sys import argv
from commons import showProgress

RE_JPG = 'jp[e]{0,1}g$'
RE_PDF = 'pdf$'
JPG_REGEX = ".+\.(({})|({}))".format(RE_JPG, RE_PDF)

class PDF(FPDF):
    def footer(self):
        self.set_y(-15) # Position at 1.5 cm from bottom
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'R') # Page number

if __name__ == '__main__':
    page_numbering, folder, out_path = argv[1:]
    if page_numbering == '0':
        pdf = FPDF()
    elif page_numbering == '1':
        pdf = PDF()
    else:
        raise Exception("The 1st shell argument 'page_numbering' must be either 0 or 1")
    input_files = sorted(filter(lambda n: re.match(JPG_REGEX, n, re.IGNORECASE), os.listdir(folder)))
    for j, image in enumerate(input_files):
        path_in = os.path.join(folder, image)
        if re.search(RE_JPG, image, re.IGNORECASE) is not None:
            pdf.add_page()
            pdf.image(path_in, x=0, y=1, w=210, h=297)
        elif re.search(RE_PDF, image, re.IGNORECASE) is not None:
            for k, page in enumerate(convert_from_path(path_in, 400)):
                path_tmp = os.path.join(folder, '.tmp_{}_{}.JPEG'.format(k, image))
                page.save(path_tmp, 'JPEG')
                pdf.add_page()
                pdf.image(path_tmp, x=0, y=1, w=210, h=297) 
                os.remove(path_tmp)
        else:
            raise Exception(image + ': format not handled!')
        showProgress(j, len(input_files))
    pdf.output(out_path, "F")
