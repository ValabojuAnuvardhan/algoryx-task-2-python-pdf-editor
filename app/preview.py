import pymupdf
from PIL import Image

from .utils import (
    logger,
    validate_pdf_path,
    FileOperationError,
)


class PDFPreview:
    """Handles rendering PDF pages for preview."""

    def render_page(
        self,
        pdf_path: str,
        page_number: int = 1,
        dpi: int = 100,
    ) -> Image.Image:
        """
        Render one PDF page as a PIL Image.

        Args:
            pdf_path: Path to the PDF.
            page_number: 1-based page number.
            dpi: Rendering resolution.

        Returns:
            PIL Image containing the rendered page.
        """
        try:
            validate_pdf_path(pdf_path)

            if page_number < 1:
                raise ValueError("Page number must be at least 1.")

            if dpi <= 0:
                raise ValueError("DPI must be greater than zero.")

            document = pymupdf.open(pdf_path)

            if page_number > document.page_count:
                document.close()
                raise ValueError(
                    f"Page number {page_number} is outside the PDF. "
                    f"The PDF contains {document.page_count} pages."
                )

            page = document[page_number - 1]

            zoom = dpi / 72
            matrix = pymupdf.Matrix(zoom, zoom)

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                (pixmap.width, pixmap.height),
                pixmap.samples,
            )

            document.close()

            logger.info(
                "Rendered page %d from %s",
                page_number,
                pdf_path,
            )

            return image

        except Exception as exc:
            logger.exception("PDF preview rendering failed.")
            raise FileOperationError(
                f"Failed to render PDF page: {exc}"
            ) from exc

    def get_page_count(self, pdf_path: str) -> int:
        """Return the number of pages in a PDF."""
        try:
            validate_pdf_path(pdf_path)

            document = pymupdf.open(pdf_path)
            page_count = document.page_count
            document.close()

            return page_count

        except Exception as exc:
            logger.exception("Could not get PDF page count.")
            raise FileOperationError(
                f"Failed to get page count: {exc}"
            ) from exc