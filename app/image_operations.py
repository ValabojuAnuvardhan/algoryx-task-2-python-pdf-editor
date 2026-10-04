import pymupdf
from PIL import Image
from pathlib import Path

from .utils import (
    logger,
    ensure_output_directory,
    validate_file_exists,
    validate_pdf_path,
    FileOperationError,
)


class ImageOperations:
    """Handles image to PDF and PDF to image conversions."""

    def image_to_pdf(
        self,
        image_paths: list[str],
        output_path: str,
    ) -> str:
        """
        Convert one or more images into a single PDF.

        Args:
            image_paths: List of image file paths.
            output_path: Destination PDF path.

        Returns:
            Output PDF path.
        """
        try:
            if not image_paths:
                raise ValueError("At least one image is required.")

            for image_path in image_paths:
                validate_file_exists(image_path)

            ensure_output_directory(output_path)

            pdf_document = pymupdf.open()

            for image_path in image_paths:
                image = Image.open(image_path)

                # Convert images with transparency or other color modes
                # into RGB for reliable PDF conversion.
                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")

                image_width, image_height = image.size

                # Convert pixels to PDF points.
                # 72 DPI is used as the baseline.
                page_width = image_width * 72 / 96
                page_height = image_height * 72 / 96

                page = pdf_document.new_page(
                    width=page_width,
                    height=page_height,
                )

                page.insert_image(
                    page.rect,
                    filename=str(image_path),
                )

                image.close()

            pdf_document.save(output_path)
            pdf_document.close()

            logger.info(
                "Converted %d image(s) to PDF: %s",
                len(image_paths),
                output_path,
            )

            return output_path

        except Exception as exc:
            logger.exception("Image to PDF conversion failed.")
            raise FileOperationError(
                f"Failed to convert image(s) to PDF: {exc}"
            ) from exc

    def pdf_to_images(
        self,
        pdf_path: str,
        output_directory: str,
        image_format: str = "png",
        dpi: int = 150,
    ) -> list[str]:
        """
        Convert every PDF page into an image.

        Args:
            pdf_path: Source PDF.
            output_directory: Destination directory.
            image_format: png or jpg.
            dpi: Rendering resolution.

        Returns:
            List of generated image paths.
        """
        try:
            validate_pdf_path(pdf_path)

            image_format = image_format.lower()

            if image_format not in ("png", "jpg", "jpeg"):
                raise ValueError(
                    "Image format must be png, jpg, or jpeg."
                )

            if dpi <= 0:
                raise ValueError("DPI must be greater than zero.")

            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)

            document = pymupdf.open(pdf_path)

            pdf_name = Path(pdf_path).stem
            generated_files = []

            zoom = dpi / 72
            matrix = pymupdf.Matrix(zoom, zoom)

            for page_number, page in enumerate(document, start=1):
                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False,
                )

                extension = "jpg" if image_format == "jpeg" else image_format

                output_path = (
                    output_dir
                    / f"{pdf_name}_page_{page_number}.{extension}"
                )

                pixmap.save(str(output_path))

                generated_files.append(str(output_path))

            document.close()

            logger.info(
                "Converted PDF to %d image(s): %s",
                len(generated_files),
                output_directory,
            )

            return generated_files

        except Exception as exc:
            logger.exception("PDF to image conversion failed.")
            raise FileOperationError(
                f"Failed to convert PDF to image(s): {exc}"
            ) from exc