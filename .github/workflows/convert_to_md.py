import mammoth
from markdownify import markdownify as md
import pathlib
import os
import tempfile
import shutil


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

def mirror_structure(folder_path, mirror_name, keep_extension):
    '''
    creates a folder structure identical to folder_path
    but substitutes "<mirror_name>" into the topmost folder
    in folder path
    ''' 
    mirror_name = folder_path.replace(pathlib.PurePath(folder_path).name, mirror_name)

    if os.path.exists(mirror_name):
        shutil.rmtree(mirror_name)
    
    shutil.copytree(folder_path, mirror_name,)

    for root, dirs, files in os.walk(mirror_name):
        for _file in files:
            if not _file.endswith(keep_extension):
                os.remove(os.path.join(root, _file))

    # cleanup original folder
    for root, dirs, files in os.walk(folder_path):
        for _file in files:
            if _file.endswith(keep_extension):
                os.remove(os.path.join(root, _file))

# collect paths
script_path = pathlib.Path(__file__).parent.absolute()
project_folder_path = os.path.dirname(os.path.dirname(script_path))

repo = os.path.join(project_folder_path, 'AVDS_repo')

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

mirror_structure(repo, 'AVDS_repo_markdown', '.md') 