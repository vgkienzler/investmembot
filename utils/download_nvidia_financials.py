from __future__ import annotations

from pathlib import Path
from typing import Optional

import requests


def download_nvidia_financials(folder_path: Optional[str]):
    """Load Nvidia financials as test file."""
    # Load and save test pdf file
    pdf_url = 'https://s201.q4cdn.com/141608511/files/doc_financials/2024/q4/1cbe8fe7-e08a-46e3-8dcc-b429fc06c1a4.pdf'
    filename = 'nvidia-earnings.pdf'
    path_to_file = Path(folder_path if folder_path else '.') / filename

    if path_to_file.exists():
        return f"File exists: {filename}"

    response = requests.get(pdf_url)

    if response.status_code == 200:
        with open(path_to_file, 'wb') as f:
            f.write(response.content)
        return f'Download successful: {path_to_file}'
    else:
        return f'Failed to download the file. Status code: {response.status_code}'
