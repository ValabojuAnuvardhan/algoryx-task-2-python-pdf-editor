from pathlib import Path

import pymupdf

from .utils import (
    FileOperationError,
    InvalidPDFError,
    PageOperationError,
    ensure_output_directory,
    logger,
    parse_page_numbers,
    validate_pdf_path,
)


class PDFOperations:
    """
    Core PDF manipulation engine for the PDF Editor.

    This class contains the application's main PDF operations.
    The GUI should call these methods instead of manipulating
    PDF files directly.
    """

    def open_pdf(self, pdf_path: str | Path) -> pymupdf.Document:
        """
        Open and validate a PDF document.

        Raises:
            InvalidPDFError: If the PDF is corrupted or cannot be opened.
        """
        path = validate_pdf_path(pdf_path)

        try:
            document = pymupdf.open(path)

            if document.page_count == 0:
                document.close()
                raise InvalidPDFError(
                    f"The PDF contains no pages: {path}"
                )

            logger.info(
                "Opened PDF: %s (%d pages)",
                path,
                document.page_count,
            )

            return document

        except InvalidPDFError:
            raise

        except Exception as exc:
            logger.exception("Failed to open PDF: %s", path)

            raise InvalidPDFError(
                f"Unable to open PDF. It may be corrupted or invalid: {path}"
            ) from exc

    def merge_pdfs(
        self,
        input_files: list[str | Path],
        output_path: str | Path,
    ) -> Path:
        """
        Merge multiple PDF files into a single PDF.
        """

        if len(input_files) < 2:
            raise FileOperationError(
                "At least two PDF files are required for merging."
            )

        output = ensure_output_directory(output_path)
        merged_document = pymupdf.open()

        opened_documents = []

        try:
            for file_path in input_files:
                document = self.open_pdf(file_path)
                opened_documents.append(document)

                merged_document.insert_pdf(document)

            merged_document.save(output)

            logger.info(
                "Merged %d PDFs into %s",
                len(input_files),
                output,
            )

            return output

        except Exception as exc:
            logger.exception("PDF merge failed.")

            if isinstance(exc, PDFOperationsError):
                raise

            raise FileOperationError(
                f"Failed to merge PDFs: {exc}"
            ) from exc

        finally:
            merged_document.close()

            for document in opened_documents:
                document.close()

    def split_pdf(
        self,
        input_file: str | Path,
        output_directory: str | Path,
    ) -> list[Path]:
        """
        Split a PDF into individual one-page PDF files.
        """

        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        document = self.open_pdf(input_file)
        output_files: list[Path] = []

        try:
            source_name = Path(input_file).stem

            for page_number in range(document.page_count):
                output_file = (
                    output_dir
                    / f"{source_name}_page_{page_number + 1}.pdf"
                )

                new_document = pymupdf.open()

                try:
                    new_document.insert_pdf(
                        document,
                        from_page=page_number,
                        to_page=page_number,
                    )

                    new_document.save(output_file)
                    output_files.append(output_file)

                finally:
                    new_document.close()

            logger.info(
                "Split %s into %d pages.",
                input_file,
                len(output_files),
            )

            return output_files

        except Exception as exc:
            logger.exception("PDF split failed.")

            raise FileOperationError(
                f"Failed to split PDF: {exc}"
            ) from exc

        finally:
            document.close()

    def rotate_pages(
        self,
        input_file: str | Path,
        output_path: str | Path,
        pages: str,
        angle: int,
    ) -> Path:
        """
        Rotate selected pages.

        pages:
            Example: "1,3-5"

        angle:
            Must be one of 90, 180, 270.
        """

        if angle not in (90, 180, 270):
            raise PageOperationError(
                "Rotation angle must be 90, 180, or 270 degrees."
            )

        document = self.open_pdf(input_file)
        output = ensure_output_directory(output_path)

        try:
            page_indexes = parse_page_numbers(
                pages,
                document.page_count,
            )

            for page_index in page_indexes:
                page = document[page_index]
                page.set_rotation(
                    (page.rotation + angle) % 360
                )

            document.save(output)

            logger.info(
                "Rotated pages %s in %s by %d degrees.",
                pages,
                input_file,
                angle,
            )

            return output

        except Exception as exc:
            logger.exception("Page rotation failed.")

            if isinstance(exc, PageOperationError):
                raise

            raise PageOperationError(
                f"Failed to rotate pages: {exc}"
            ) from exc

        finally:
            document.close()

    def delete_pages(
        self,
        input_file: str | Path,
        output_path: str | Path,
        pages: str,
    ) -> Path:
        """
        Delete selected pages from a PDF.

        Example:
            pages="2,4-6"
        """

        document = self.open_pdf(input_file)
        output = ensure_output_directory(output_path)

        try:
            page_indexes = parse_page_numbers(
                pages,
                document.page_count,
            )

            if len(page_indexes) >= document.page_count:
                raise PageOperationError(
                    "Cannot delete all pages from the PDF."
                )

            # Delete from highest index to lowest index so that
            # removing one page does not change the indexes of
            # pages that still need to be removed.
            for page_index in reversed(page_indexes):
                document.delete_page(page_index)

            document.save(output)

            logger.info(
                "Deleted pages %s from %s.",
                pages,
                input_file,
            )

            return output

        except Exception as exc:
            logger.exception("Page deletion failed.")

            if isinstance(exc, PageOperationError):
                raise

            raise PageOperationError(
                f"Failed to delete pages: {exc}"
            ) from exc

        finally:
            document.close()

    def reorder_pages(
        self,
        input_file: str | Path,
        output_path: str | Path,
        page_order: str,
    ) -> Path:
        """
        Reorder pages using a comma-separated order.

        Example for a 4-page PDF:

            "3,1,4,2"

        means:

            New page 1 = old page 3
            New page 2 = old page 1
            New page 3 = old page 4
            New page 4 = old page 2
        """

        document = self.open_pdf(input_file)
        output = ensure_output_directory(output_path)

        try:
            order = parse_page_numbers(
                page_order,
                document.page_count,
            )

            if len(order) != document.page_count:
                raise PageOperationError(
                    "The reorder list must contain every page exactly once."
                )

            if len(set(order)) != document.page_count:
                raise PageOperationError(
                    "Each page must appear exactly once in the new order."
                )

            # Create a new document and copy pages in the requested order.
            reordered_document = pymupdf.open()

            try:
                for page_index in order:
                    reordered_document.insert_pdf(
                        document,
                        from_page=page_index,
                        to_page=page_index,
                    )

                reordered_document.save(output)

            finally:
                reordered_document.close()

            logger.info(
                "Reordered pages of %s using order %s.",
                input_file,
                page_order,
            )

            return output

        except Exception as exc:
            logger.exception("Page reordering failed.")

            if isinstance(exc, PageOperationError):
                raise

            raise PageOperationError(
                f"Failed to reorder pages: {exc}"
            ) from exc

        finally:
            document.close()

    def extract_text(
        self,
        input_file: str | Path,
        output_path: str | Path,
    ) -> Path:
        """
        Extract text from every page of a PDF and save it as TXT.
        """

        document = self.open_pdf(input_file)
        output = ensure_output_directory(output_path)

        try:
            text_parts: list[str] = []

            for page_number, page in enumerate(document, start=1):
                text_parts.append(
                    f"--- Page {page_number} ---\n"
                )
                text_parts.append(
                    page.get_text()
                )
                text_parts.append("\n")

            output.write_text(
                "".join(text_parts),
                encoding="utf-8",
            )

            logger.info(
                "Extracted text from %s to %s.",
                input_file,
                output,
            )

            return output

        except Exception as exc:
            logger.exception("Text extraction failed.")

            raise FileOperationError(
                f"Failed to extract text: {exc}"
            ) from exc

        finally:
            document.close()

    def add_watermark(
        self,
        input_path: str,
        output_path: str,
        watermark_text: str = "WATERMARK",
    ) -> str:
        """
        Add a diagonal semi-transparent watermark to every page.
        """
        try:
            if not watermark_text.strip():
                raise ValueError("Watermark text cannot be empty.")

            document = self.open_pdf(input_path)

            for page in document:
                rect = page.rect

                center_x = rect.width / 2
                center_y = rect.height / 2

                font_size = min(rect.width, rect.height) / 10

                # Create a text shape so we can apply a custom
                # transformation instead of using rotate=45.
                shape = page.new_shape()

                shape.insert_text(
                    (center_x - (len(watermark_text) * font_size * 0.25),
                     center_y),
                    watermark_text,
                    fontsize=font_size,
                    fontname="helv",
                    color=(0.5, 0.5, 0.5),
                    fill_opacity=0.35,
                    stroke_opacity=0.35,
                )

                shape.commit(overlay=True)

            ensure_output_directory(output_path)
            document.save(output_path)

            logger.info("Watermark added successfully: %s", output_path)
            return output_path

        except PDFOperationsError:
            raise

        except Exception as exc:
            logger.exception("Watermark operation failed.")
            raise FileOperationError(
                f"Failed to add watermark: {exc}"
            ) from exc

        finally:
            if document is not None:
                document.close()

    def password_protect(
        self,
        input_file: str | Path,
        output_path: str | Path,
        password: str,
    ) -> Path:
        """
        Create a password-protected copy of a PDF.
        """

        if not password:
            raise ValueError("Password cannot be empty.")

        source = self.open_pdf(input_file)
        output = ensure_output_directory(output_path)

        try:
            permissions = (
                pymupdf.PDF_PERM_ACCESSIBILITY
                | pymupdf.PDF_PERM_PRINT
            )

            encryption = pymupdf.PDF_ENCRYPT_AES_256

            source.save(
                output,
                encryption=encryption,
                owner_pw=password,
                user_pw=password,
                permissions=permissions,
            )

            logger.info(
                "Password protection applied to %s.",
                input_file,
            )

            return output

        except Exception as exc:
            logger.exception("Password protection failed.")

            raise FileOperationError(
                f"Failed to password-protect PDF: {exc}"
            ) from exc

        finally:
            source.close()


# Alias used to make exception handling cleaner inside the class.
PDFOperationsError = (
    InvalidPDFError,
    PageOperationError,
    FileOperationError,
)