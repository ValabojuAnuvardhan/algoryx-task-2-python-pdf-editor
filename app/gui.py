import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

from .pdf_manager import PDFManager


class PDFEditorGUI(ctk.CTk):
    """Main GUI application for the ALGORYX PDF Editor."""

    def __init__(self):
        super().__init__()

        self.title("ALGORYX PDF Editor")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.manager = PDFManager()

        self.current_pdf = None
        self.current_page = 1
        self.total_pages = 0
        self.preview_image = None

        self._build_layout()

    def _build_layout(self):
        # Main window grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------------------------------------------------------
        # HEADER
        # ---------------------------------------------------------
        self.header = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0
        )
        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="ALGORYX PDF Editor",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=18,
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            self.header,
            text="● Ready",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.grid(
            row=0,
            column=1,
            padx=25,
            pady=18
        )

        # ---------------------------------------------------------
        # SIDEBAR
        # ---------------------------------------------------------
        self.sidebar = ctk.CTkScrollableFrame(
            self,
            width=230,
            corner_radius=0
        )
        self.sidebar.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 2)
        )

        # Sidebar heading
        self.tools_label = ctk.CTkLabel(
            self.sidebar,
            text="PDF Tools",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )
        self.tools_label.pack(
            padx=15,
            pady=(20, 15)
        )

        # Open PDF button
        self.open_button = ctk.CTkButton(
            self.sidebar,
            text="📂  Open PDF",
            height=40,
            command=self.open_pdf
        )
        self.open_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )
                # Merge PDFs
        self.merge_button = ctk.CTkButton(
            self.sidebar,
            text="🔗  Merge PDFs",
            height=40,
            command=self.merge_pdfs,
        )
        self.merge_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )

        # Split PDF
        self.split_button = ctk.CTkButton(
            self.sidebar,
            text="✂️  Split PDF",
            height=40,
            command=self.split_pdf,
        )
        self.split_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )
                # Rotate Pages
        self.rotate_button = ctk.CTkButton(
            self.sidebar,
            text="🔄  Rotate Pages",
            height=40,
            command=self.rotate_pages,
        )
        self.rotate_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )

        # Delete Pages
        self.delete_button = ctk.CTkButton(
            self.sidebar,
            text="🗑️  Delete Pages",
            height=40,
            command=self.delete_pages,
        )
        self.delete_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )
        # Reorder Pages
        self.reorder_button = ctk.CTkButton(
            self.sidebar,
            text="↕️  Reorder Pages",
            height=40,
            command=self.reorder_pages,
        )
        self.reorder_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )

        # Extract Text
        self.extract_button = ctk.CTkButton(
            self.sidebar,
            text="📝  Extract Text",
            height=40,
            command=self.extract_text,
        )
        self.extract_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )
        # Watermark
        self.watermark_button = ctk.CTkButton(
            self.sidebar,
            text="💧  Add Watermark",
            height=40,
            command=self.add_watermark,
        )
        self.watermark_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )

        # Password Protection
        self.password_button = ctk.CTkButton(
            self.sidebar,
            text="🔐  Password Protect",
            height=40,
            command=self.password_protect,
        )
        self.password_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )
        # Image to PDF
        self.image_to_pdf_button = ctk.CTkButton(
            self.sidebar,
            text="🖼️  Images → PDF",
            height=40,
            command=self.image_to_pdf,
        )
        self.image_to_pdf_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )

        # PDF to Images
        self.pdf_to_images_button = ctk.CTkButton(
            self.sidebar,
            text="🖼️  PDF → Images",
            height=40,
            command=self.pdf_to_images,
        )
        self.pdf_to_images_button.pack(
            padx=15,
            pady=8,
            fill="x",
        )
        # Preview navigation section
        self.navigation_label = ctk.CTkLabel(
            self.sidebar,
            text="Preview Navigation",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )
        self.navigation_label.pack(
            padx=15,
            pady=(25, 8),
            anchor="w"
        )

        self.previous_button = ctk.CTkButton(
            self.sidebar,
            text="◀ Previous Page",
            height=38,
            command=self.previous_page,
            state="disabled"
        )
        self.previous_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.next_button = ctk.CTkButton(
            self.sidebar,
            text="Next Page ▶",
            height=38,
            command=self.next_page,
            state="disabled"
        )
        self.next_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        # ---------------------------------------------------------
        # CONTENT AREA
        # ---------------------------------------------------------
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.content.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=(0, 10)
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Current file
        self.file_label = ctk.CTkLabel(
            self.content,
            text="No PDF selected",
            font=ctk.CTkFont(size=16)
        )
        self.file_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        # Preview frame
        self.preview_frame = ctk.CTkFrame(
            self.content,
            corner_radius=10
        )
        self.preview_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 10)
        )

        # Preview label
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="PDF Preview",
            font=ctk.CTkFont(size=20)
        )
        self.preview_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Page information
        self.page_label = ctk.CTkLabel(
            self.content,
            text="Page 0 of 0",
            font=ctk.CTkFont(size=14)
        )
        self.page_label.grid(
            row=2,
            column=0,
            padx=20,
            pady=10
        )

    # =============================================================
    # PDF OPENING
    # =============================================================

    def open_pdf(self):
        """Open a PDF selected by the user."""

        file_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            self.status_label.configure(text="● Opening...")

            # Validate PDF and get page count
            page_count = self.manager.get_page_count(file_path)

            self.current_pdf = file_path
            self.current_page = 1
            self.total_pages = page_count

            # Update filename
            self.file_label.configure(
                text=f"📄 {Path(file_path).name}"
            )

            # Enable navigation
            self.update_navigation_buttons()

            # Render first page
            self.show_current_page()

            self.status_label.configure(
                text="● PDF Loaded"
            )

        except Exception as exc:
            self.current_pdf = None
            self.current_page = 1
            self.total_pages = 0

            self.update_navigation_buttons()

            self.status_label.configure(
                text="● Error"
            )

            messagebox.showerror(
                "Unable to Open PDF",
                f"The PDF could not be opened.\n\n{exc}"
            )
    # =============================================================
    # REORDER PAGES
    # =============================================================

    def reorder_pages(self):
        """Reorder all pages according to a user-defined sequence."""

        input_file = filedialog.askopenfilename(
            title="Select PDF to Reorder",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        try:
            page_count = self.manager.get_page_count(
                input_file
            )
        except Exception as exc:
            messagebox.showerror(
                "PDF Error",
                f"Could not read the PDF.\n\n{exc}",
            )
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Reorder Pages")
        dialog.geometry("500x350")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Reorder PDF Pages",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 15),
        )

        ctk.CTkLabel(
            dialog,
            text=(
                f"This PDF contains {page_count} pages.\n\n"
                "Enter the complete page order.\n"
                "Example: 3,1,4,2"
            ),
            justify="center",
        ).pack(
            pady=10,
        )

        order_entry = ctk.CTkEntry(
            dialog,
            width=350,
            placeholder_text="3,1,4,2",
        )
        order_entry.pack(
            pady=15,
        )

        ctk.CTkLabel(
            dialog,
            text=(
                f"Every page from 1 to {page_count} "
                "must appear exactly once."
            ),
            font=ctk.CTkFont(size=12),
        ).pack(
            pady=5,
        )

        def perform_reorder():
            page_order = order_entry.get().strip()

            if not page_order:
                messagebox.showwarning(
                    "Missing Page Order",
                    "Enter the page order.",
                    parent=dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save Reordered PDF",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF files", "*.pdf"),
                ],
                initialfile="reordered.pdf",
                parent=dialog,
            )

            if not output_path:
                return

            try:
                self.status_label.configure(
                    text="● Reordering..."
                )

                result = self.manager.reorder_pages(
                    input_file,
                    output_path,
                    page_order,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● Reorder Complete"
                )

                messagebox.showinfo(
                    "Reorder Complete",
                    f"New page order:\n{page_order}\n\n"
                    f"Saved to:\n{result}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Reorder Error",
                    f"Could not reorder the pages.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Reorder & Save",
            command=perform_reorder,
        ).pack(
            pady=15,
        )

    # =============================================================
    # EXTRACT TEXT
    # =============================================================

    def extract_text(self):
        """Extract text from a PDF and save it as a TXT file."""

        input_file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Extracted Text",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
            ],
            initialfile="extracted_text.txt",
        )

        if not output_path:
            return

        try:
            self.status_label.configure(
                text="● Extracting..."
            )

            result = self.manager.extract_text(
                input_file,
                output_path,
            )

            self.status_label.configure(
                text="● Text Extracted"
            )

            messagebox.showinfo(
                "Extraction Complete",
                f"Text successfully extracted.\n\n"
                f"Saved to:\n{result}",
            )

        except Exception as exc:
            self.status_label.configure(
                text="● Error"
            )

            messagebox.showerror(
                "Extraction Error",
                f"Could not extract text.\n\n{exc}",
            )
    # =============================================================
    # WATERMARK
    # =============================================================

    def add_watermark(self):
        """Add a watermark to every page of a PDF."""

        input_file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Watermark")
        dialog.geometry("450x280")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Add Watermark",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 20),
        )

        ctk.CTkLabel(
            dialog,
            text="Watermark text",
        ).pack(
            pady=5,
        )

        watermark_entry = ctk.CTkEntry(
            dialog,
            width=320,
            placeholder_text="CONFIDENTIAL",
        )
        watermark_entry.pack(
            pady=8,
        )

        def perform_watermark():
            watermark_text = watermark_entry.get().strip()

            if not watermark_text:
                messagebox.showwarning(
                    "Missing Watermark",
                    "Enter watermark text.",
                    parent=dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save Watermarked PDF",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF files", "*.pdf"),
                ],
                initialfile="watermarked.pdf",
                parent=dialog,
            )

            if not output_path:
                return

            try:
                self.status_label.configure(
                    text="● Adding Watermark..."
                )

                result = self.manager.add_watermark(
                    input_file,
                    output_path,
                    watermark_text,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● Watermark Added"
                )

                messagebox.showinfo(
                    "Watermark Complete",
                    f"Watermark added successfully.\n\n"
                    f"Text: {watermark_text}\n\n"
                    f"Saved to:\n{result}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Watermark Error",
                    f"Could not add watermark.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Add & Save",
            command=perform_watermark,
        ).pack(
            pady=20,
        )
    # =============================================================
    # PASSWORD PROTECTION
    # =============================================================

    def password_protect(self):
        """Protect a PDF with a password."""

        input_file = filedialog.askopenfilename(
            title="Select PDF to Protect",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Password Protection")
        dialog.geometry("450x330")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Password Protect PDF",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 20),
        )

        ctk.CTkLabel(
            dialog,
            text="Enter password",
        ).pack(
            pady=5,
        )

        password_entry = ctk.CTkEntry(
            dialog,
            width=320,
            show="*",
            placeholder_text="Enter password",
        )
        password_entry.pack(
            pady=8,
        )

        ctk.CTkLabel(
            dialog,
            text="Confirm password",
        ).pack(
            pady=(10, 5),
        )

        confirm_entry = ctk.CTkEntry(
            dialog,
            width=320,
            show="*",
            placeholder_text="Confirm password",
        )
        confirm_entry.pack(
            pady=8,
        )

        def perform_protection():
            password = password_entry.get()
            confirmation = confirm_entry.get()

            if not password:
                messagebox.showwarning(
                    "Missing Password",
                    "Enter a password.",
                    parent=dialog,
                )
                return

            if password != confirmation:
                messagebox.showwarning(
                    "Password Mismatch",
                    "The passwords do not match.",
                    parent=dialog,
                )
                return

            if len(password) < 4:
                messagebox.showwarning(
                    "Weak Password",
                    "Please use at least 4 characters.",
                    parent=dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save Protected PDF",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF files", "*.pdf"),
                ],
                initialfile="protected.pdf",
                parent=dialog,
            )

            if not output_path:
                return

            try:
                self.status_label.configure(
                    text="● Protecting..."
                )

                result = self.manager.password_protect(
                    input_file,
                    output_path,
                    password,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● PDF Protected"
                )

                messagebox.showinfo(
                    "Protection Complete",
                    "PDF password protection enabled.\n\n"
                    f"Saved to:\n{result}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Protection Error",
                    f"Could not protect the PDF.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Protect & Save",
            command=perform_protection,
        ).pack(
            pady=20,
        )
    # =============================================================
    # IMAGE → PDF
    # =============================================================

    def image_to_pdf(self):
        """Convert one or more images into a PDF."""

        image_files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
            ],
        )

        if not image_files:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
            initialfile="images_converted.pdf",
        )

        if not output_path:
            return

        try:
            self.status_label.configure(
                text="● Converting Images..."
            )

            result = self.manager.image_to_pdf(
                list(image_files),
                output_path,
            )

            self.status_label.configure(
                text="● Image Conversion Complete"
            )

            messagebox.showinfo(
                "Image → PDF Complete",
                f"Successfully converted "
                f"{len(image_files)} image(s) to PDF.\n\n"
                f"Saved to:\n{result}",
            )

        except Exception as exc:
            self.status_label.configure(
                text="● Error"
            )

            messagebox.showerror(
                "Image Conversion Error",
                f"Could not convert the images.\n\n{exc}",
            )
    # =============================================================
    # PDF → IMAGES
    # =============================================================

    def pdf_to_images(self):
        """Convert every PDF page into an image."""

        input_file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        output_directory = filedialog.askdirectory(
            title="Select Output Folder",
        )

        if not output_directory:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("PDF → Images")
        dialog.geometry("420x300")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="PDF → Images",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 20),
        )

        ctk.CTkLabel(
            dialog,
            text="Image format",
        ).pack(
            pady=5,
        )

        format_menu = ctk.CTkOptionMenu(
            dialog,
            values=["PNG", "JPG"],
        )
        format_menu.set("PNG")
        format_menu.pack(
            pady=8,
        )

        ctk.CTkLabel(
            dialog,
            text="Resolution (DPI)",
        ).pack(
            pady=(10, 5),
        )

        dpi_entry = ctk.CTkEntry(
            dialog,
            width=200,
            placeholder_text="150",
        )
        dpi_entry.insert(0, "150")
        dpi_entry.pack(
            pady=5,
        )

        def perform_conversion():
            try:
                dpi = int(dpi_entry.get())

                if dpi <= 0:
                    raise ValueError(
                        "DPI must be greater than zero."
                    )

                image_format = format_menu.get().lower()

                self.status_label.configure(
                    text="● Converting PDF..."
                )

                generated_files = self.manager.pdf_to_images(
                    input_file,
                    output_directory,
                    image_format,
                    dpi,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● Conversion Complete"
                )

                messagebox.showinfo(
                    "PDF → Images Complete",
                    f"Successfully converted "
                    f"{len(generated_files)} PDF page(s).\n\n"
                    f"Output folder:\n{output_directory}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Conversion Error",
                    f"Could not convert the PDF.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Convert",
            command=perform_conversion,
        ).pack(
            pady=20,
        )
    # =============================================================
    # PAGE PREVIEW
    # =============================================================

    def show_current_page(self):
        """Render and display the current PDF page."""

        if not self.current_pdf:
            return

        try:
            image = self.manager.render_page(
                self.current_pdf,
                self.current_page,
                dpi=100
            )

            # Calculate a display size that fits the preview area.
            max_width = 650
            max_height = 650

            image.thumbnail(
                (max_width, max_height)
            )

            self.preview_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.preview_label.configure(
                image=self.preview_image,
                text=""
            )

            self.page_label.configure(
                text=f"Page {self.current_page} of {self.total_pages}"
            )

            self.update_navigation_buttons()

        except Exception as exc:
            messagebox.showerror(
                "Preview Error",
                f"Could not render the page.\n\n{exc}"
            )
    # =============================================================
    # ROTATE PAGES
    # =============================================================

    def rotate_pages(self):
        """Rotate selected PDF pages by 90, 180, or 270 degrees."""

        input_file = filedialog.askopenfilename(
            title="Select PDF to Rotate",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Rotate Pages")
        dialog.geometry("420x300")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Rotate PDF Pages",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 20),
        )

        ctk.CTkLabel(
            dialog,
            text="Pages\nExample: 1,3-5",
        ).pack(
            pady=(5, 5),
        )

        pages_entry = ctk.CTkEntry(
            dialog,
            width=280,
            placeholder_text="1,3-5",
        )
        pages_entry.pack(
            pady=5,
        )

        ctk.CTkLabel(
            dialog,
            text="Rotation angle",
        ).pack(
            pady=(10, 5),
        )

        angle_menu = ctk.CTkOptionMenu(
            dialog,
            values=["90", "180", "270"],
        )
        angle_menu.set("90")
        angle_menu.pack(
            pady=5,
        )

        def perform_rotation():
            pages = pages_entry.get().strip()

            if not pages:
                messagebox.showwarning(
                    "Missing Pages",
                    "Enter the pages to rotate.",
                    parent=dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save Rotated PDF",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF files", "*.pdf"),
                ],
                initialfile="rotated.pdf",
                parent=dialog,
            )

            if not output_path:
                return

            try:
                angle = int(angle_menu.get())

                self.status_label.configure(
                    text="● Rotating..."
                )

                result = self.manager.rotate_pages(
                    input_file,
                    output_path,
                    pages,
                    angle,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● Rotation Complete"
                )

                messagebox.showinfo(
                    "Rotation Complete",
                    f"Pages {pages} rotated by {angle}°.\n\n"
                    f"Saved to:\n{result}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Rotation Error",
                    f"Could not rotate the PDF.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Rotate & Save",
            command=perform_rotation,
        ).pack(
            pady=(20, 10),
        )

    # =============================================================
    # DELETE PAGES
    # =============================================================

    def delete_pages(self):
        """Delete selected pages from a PDF."""

        input_file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Delete Pages")
        dialog.geometry("420x250")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Delete PDF Pages",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(
            pady=(25, 20),
        )

        ctk.CTkLabel(
            dialog,
            text="Pages to delete\nExample: 2,4-5",
        ).pack(
            pady=5,
        )

        pages_entry = ctk.CTkEntry(
            dialog,
            width=280,
            placeholder_text="2,4-5",
        )
        pages_entry.pack(
            pady=8,
        )

        def perform_delete():
            pages = pages_entry.get().strip()

            if not pages:
                messagebox.showwarning(
                    "Missing Pages",
                    "Enter the pages to delete.",
                    parent=dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save PDF Without Selected Pages",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF files", "*.pdf"),
                ],
                initialfile="deleted_pages.pdf",
                parent=dialog,
            )

            if not output_path:
                return

            try:
                self.status_label.configure(
                    text="● Deleting..."
                )

                result = self.manager.delete_pages(
                    input_file,
                    output_path,
                    pages,
                )

                dialog.destroy()

                self.status_label.configure(
                    text="● Pages Deleted"
                )

                messagebox.showinfo(
                    "Delete Complete",
                    f"Deleted pages: {pages}\n\n"
                    f"Saved to:\n{result}",
                )

            except Exception as exc:
                self.status_label.configure(
                    text="● Error"
                )

                messagebox.showerror(
                    "Delete Error",
                    f"Could not delete the selected pages.\n\n{exc}",
                    parent=dialog,
                )

        ctk.CTkButton(
            dialog,
            text="Delete & Save",
            command=perform_delete,
        ).pack(
            pady=15,
        )
    # =============================================================
    # MERGE PDFs
    # =============================================================

    def merge_pdfs(self):
        """Select multiple PDFs and merge them into one PDF."""

        input_files = filedialog.askopenfilenames(
            title="Select PDFs to Merge",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_files:
            return

        if len(input_files) < 2:
            messagebox.showwarning(
                "Merge PDFs",
                "Please select at least two PDF files.",
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
            initialfile="merged.pdf",
        )

        if not output_path:
            return

        try:
            self.status_label.configure(
                text="● Merging..."
            )

            result = self.manager.merge_pdfs(
                list(input_files),
                output_path,
            )

            self.status_label.configure(
                text="● Merge Complete"
            )

            messagebox.showinfo(
                "Merge Complete",
                f"Successfully merged {len(input_files)} PDFs.\n\n"
                f"Saved to:\n{result}",
            )

        except Exception as exc:
            self.status_label.configure(
                text="● Error"
            )

            messagebox.showerror(
                "Merge Error",
                f"Could not merge the PDF files.\n\n{exc}",
            )

    # =============================================================
    # SPLIT PDF
    # =============================================================

    def split_pdf(self):
        """Split a PDF into individual one-page PDF files."""

        input_file = filedialog.askopenfilename(
            title="Select PDF to Split",
            filetypes=[
                ("PDF files", "*.pdf"),
            ],
        )

        if not input_file:
            return

        output_directory = filedialog.askdirectory(
            title="Select Output Folder",
        )

        if not output_directory:
            return

        try:
            self.status_label.configure(
                text="● Splitting..."
            )

            generated_files = self.manager.split_pdf(
                input_file,
                output_directory,
            )

            self.status_label.configure(
                text="● Split Complete"
            )

            messagebox.showinfo(
                "Split Complete",
                f"Successfully split the PDF into "
                f"{len(generated_files)} pages.\n\n"
                f"Output folder:\n{output_directory}",
            )

        except Exception as exc:
            self.status_label.configure(
                text="● Error"
            )

            messagebox.showerror(
                "Split Error",
                f"Could not split the PDF.\n\n{exc}",
            )
    # =============================================================
    # PAGE NAVIGATION
    # =============================================================

    def previous_page(self):
        """Display the previous page."""

        if not self.current_pdf:
            return

        if self.current_page > 1:
            self.current_page -= 1
            self.show_current_page()

    def next_page(self):
        """Display the next page."""

        if not self.current_pdf:
            return

        if self.current_page < self.total_pages:
            self.current_page += 1
            self.show_current_page()

    def update_navigation_buttons(self):
        """Enable or disable page navigation buttons."""

        if not self.current_pdf:
            self.previous_button.configure(
                state="disabled"
            )
            self.next_button.configure(
                state="disabled"
            )
            return

        if self.current_page > 1:
            self.previous_button.configure(
                state="normal"
            )
        else:
            self.previous_button.configure(
                state="disabled"
            )

        if self.current_page < self.total_pages:
            self.next_button.configure(
                state="normal"
            )
        else:
            self.next_button.configure(
                state="disabled"
            )

    # =============================================================
    # APPLICATION
    # =============================================================

    def run(self):
        """Start the GUI event loop."""

        self.mainloop()