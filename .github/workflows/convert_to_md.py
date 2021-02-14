import mammoth
from markdownify import markdownify as md
import pathlib
import os
import tempfile


def collect_files_by_extension(path='.', extension=''):
    files_w_extension = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if extension in name:
                files_w_extension.append(os.path.join(root, name))
    return files_w_extension

def convert_docx_to_md(docx_file):
    with open(doc, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        messages = result.messages
        # if successful create new html file
        md_file_name = doc.replace("docx", "md")

        markdown = md(html)
    return markdown

# collect paths
script_path = pathlib.Path(__file__).parent.absolute()
project_folder_path = os.path.dirname(os.path.dirname(script_path))

# collect all docx docs
docx_docs = collect_files_by_extension(path=project_folder_path, extension='.docx')

# create md directories for md docs
dirnames = [os.path.dirname(doc) for doc in docx_docs]

# convert docx to html -> md
for doc in docx_docs:
    markdown = convert_docx_to_md(doc)
    md_file_name = doc.replace("docx", "md")
    with open(md_file_name, 'w') as markdown_file:
        markdown_file.write(markdown)
 