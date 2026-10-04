import logging
from pathlib import Path


# Create required project directories
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# Configure application logging
LOG_FILE = LOG_DIR / "pdf_editor.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


logger = logging.getLogger("PDFEditor")


class PDFEditorError(Exception):
    """Base exception for PDF Editor errors."""


class InvalidPDFError(PDFEditorError):
    """Raised when a PDF is invalid or corrupted."""


class PageOperationError(PDFEditorError):
    """Raised when a page operation fails."""


class FileOperationError(PDFEditorError):
    """Raised when a file operation fails."""


def validate_file_exists(file_path: str | Path) -> Path:
    """
    Validate that a file exists and is actually a file.

    Returns:
        Path: Validated file path.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return path


def validate_pdf_path(file_path: str | Path) -> Path:
    """
    Validate that the supplied path exists and has a PDF extension.
    """
    path = validate_file_exists(file_path)

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {path}")

    return path


def ensure_output_directory(output_path: str | Path) -> Path:
    """
    Create the parent directory for an output file if necessary.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def parse_page_numbers(
    page_text: str,
    total_pages: int,
) -> list[int]:
    """
    Convert page input such as:

        "1,3,5"
        "1-4"
        "1,3-5,8"

    into zero-based page indexes while preserving
    the order entered by the user.

    Examples:
        "1,3,5"   -> [0, 2, 4]
        "1-4"     -> [0, 1, 2, 3]
        "3,1,4,2" -> [2, 0, 3, 1]
    """

    if not page_text.strip():
        raise ValueError("Please enter at least one page number.")

    pages: list[int] = []
    seen: set[int] = set()

    try:
        parts = page_text.replace(" ", "").split(",")

        for part in parts:
            if not part:
                continue

            if "-" in part:
                start_text, end_text = part.split("-", 1)

                start = int(start_text)
                end = int(end_text)

                if start > end:
                    raise ValueError(
                        f"Invalid page range: {part}"
                    )

                page_values = range(start, end + 1)

            else:
                page_values = [int(part)]

            for page in page_values:
                if page < 1 or page > total_pages:
                    raise ValueError(
                        f"Page {page} is outside the PDF. "
                        f"Valid pages are 1-{total_pages}."
                    )

                if page not in seen:
                    pages.append(page)
                    seen.add(page)

    except ValueError as exc:
        if "outside the PDF" in str(exc):
            raise

        raise ValueError(
            "Invalid page format. Use examples like 1,3,5 or 1-4."
        ) from exc

    # Convert user-facing 1-based pages to zero-based indexes
    # while preserving the user's original order.
    return [page - 1 for page in pages]