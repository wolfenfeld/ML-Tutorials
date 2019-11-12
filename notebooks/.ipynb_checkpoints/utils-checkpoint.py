from pylatex import Document, NoEscape
import os

def tex_to_png(tex_string, file_name, image_height, image_width=330, image_format='jpg'):

    doc = Document(file_name ,
                   geometry_options=[r'paperwidth={0}px'.format(image_width),r'paperheight={0}px'.format(image_height)],
                   page_numbers=False)

    doc.append(NoEscape(tex_string))
    doc.generate_pdf(file_name,clean_tex=True)
    os.system('convert -density 600 {0}.pdf {0}.{1}'.format(file_name, image_format))
