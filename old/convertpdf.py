from docx2pdf import convert

def convert_to_pdf(input_file):
    file = input_file
    output_file = '.'.join(file.splite('.', 1)[0], 'pdf')
    convert(input_file, output_file)
    return output_file