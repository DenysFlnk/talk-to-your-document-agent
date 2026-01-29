import io
from pathlib import Path

import pandas as pd
from aidial_client import Dial
from aidial_client.types.file import FileDownloadResponse
from docx import Document

from agent.utils.file_content_cache import FileContentCache


class DialFileContentExtractor:
    def __init__(self, endpoint: str, api_key: str, cache: FileContentCache):
        self.dial_client = Dial(base_url=endpoint, api_key=api_key)
        self.cache = cache

    def extract_text(self, file_url: str) -> str:
        if self.cache.get(file_url):
            return self.cache.get(file_url)

        file: FileDownloadResponse = self.dial_client.files.download(file_url)

        file_name = file.filename
        file_extension = Path(file_name).suffix.lower()

        content = file.get_content()

        extracted_text = self.__extract_text(
            file_content=content, file_extension=file_extension, filename=file_name
        )

        self.cache.set(key=file_url, content=extracted_text)

        return extracted_text

    def __extract_text(
        self, file_content: bytes, file_extension: str, filename: str
    ) -> str:
        try:
            if file_extension == ".xlsx":
                buffer = io.BytesIO(file_content)
                data_frame = pd.read_excel(buffer)
                markdown = data_frame.to_markdown(index=False)
                return markdown or ""

            if file_extension == ".docx":
                buffer = io.BytesIO(file_content)
                doc = Document(buffer)
                text_content = [paragraph.text for paragraph in doc.paragraphs]
                return "\n".join(text_content)

            return file_content.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"Error while parsing {filename}: {e}")
            return ""
