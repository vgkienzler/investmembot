from pathlib import Path


def list_files_in_folder(folder_path: str) -> list:
    """List all files in a folder"""
    types_to_include = ['.pdf', '.xml.doc', '.docx', '.pptx', '.rtf', '.pages', '.key', '.epub']

    path = Path(folder_path)
    return [str(file) for file in path.iterdir() if file.is_file() and file.suffix in types_to_include]
