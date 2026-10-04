from .pdf_operations import PDFOperations
from .image_operations import ImageOperations
from .preview import PDFPreview


class PDFManager:
    """Coordinates all PDF editor operations."""

    def __init__(self):
        self.pdf_operations = PDFOperations()
        self.image_operations = ImageOperations()
        self.preview = PDFPreview()

    # -------------------------
    # PDF operations
    # -------------------------

    def merge_pdfs(self, input_paths, output_path):
        return self.pdf_operations.merge_pdfs(
            input_paths,
            output_path,
        )

    def split_pdf(self, input_path, output_directory):
        return self.pdf_operations.split_pdf(
            input_path,
            output_directory,
        )

    def rotate_pages(
        self,
        input_path,
        output_path,
        pages,
        angle,
    ):
        return self.pdf_operations.rotate_pages(
            input_path,
            output_path,
            pages,
            angle,
        )

    def delete_pages(
        self,
        input_path,
        output_path,
        pages,
    ):
        return self.pdf_operations.delete_pages(
            input_path,
            output_path,
            pages,
        )

    def reorder_pages(
        self,
        input_path,
        output_path,
        page_order,
    ):
        return self.pdf_operations.reorder_pages(
            input_path,
            output_path,
            page_order,
        )

    def extract_text(
        self,
        input_path,
        output_path,
    ):
        return self.pdf_operations.extract_text(
            input_path,
            output_path,
        )

    def add_watermark(
        self,
        input_path,
        output_path,
        watermark_text,
    ):
        return self.pdf_operations.add_watermark(
            input_path,
            output_path,
            watermark_text,
        )

    def password_protect(
        self,
        input_path,
        output_path,
        password,
    ):
        return self.pdf_operations.password_protect(
            input_path,
            output_path,
            password,
        )

    # -------------------------
    # Image operations
    # -------------------------

    def image_to_pdf(
        self,
        image_paths,
        output_path,
    ):
        return self.image_operations.image_to_pdf(
            image_paths,
            output_path,
        )

    def pdf_to_images(
        self,
        pdf_path,
        output_directory,
        image_format="png",
        dpi=150,
    ):
        return self.image_operations.pdf_to_images(
            pdf_path,
            output_directory,
            image_format,
            dpi,
        )

    # -------------------------
    # Preview
    # -------------------------

    def render_page(
        self,
        pdf_path,
        page_number=1,
        dpi=100,
    ):
        return self.preview.render_page(
            pdf_path,
            page_number,
            dpi,
        )

    def get_page_count(self, pdf_path):
        return self.preview.get_page_count(pdf_path)