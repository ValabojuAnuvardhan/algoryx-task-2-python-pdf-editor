@'
# ALGORYX PDF Editor

A Python-based desktop PDF editor developed as part of the ALGORYX Python Internship.

The application provides a clean graphical interface for common PDF editing, conversion, preview, and security operations.

## Features

### PDF Editing
- Merge multiple PDF files
- Split a PDF into individual pages
- Rotate selected pages
- Delete selected pages
- Reorder PDF pages
- Extract text from PDF files
- Add watermarks
- Password-protect PDF files

### Conversion
- Convert images to PDF
- Convert PDF pages to PNG/JPG images

### Preview
- Open PDF files
- Display page previews
- Navigate between pages
- Display current page number and total pages

### Reliability
- PDF validation
- Graceful handling of invalid/corrupted PDFs
- User-friendly error messages
- Application logging
- Exception handling

## Technology Stack

- Python 3.11+
- PyMuPDF
- Pillow
- CustomTkinter
- Object-Oriented Programming
- Modular architecture

## Project Structure

```text
task-2-pdf-editor/
│
├── app/
│   ├── __init__.py
│   ├── gui.py
│   ├── pdf_manager.py
│   ├── pdf_operations.py
│   ├── image_operations.py
│   ├── preview.py
│   └── utils.py
│
├── assets/
├── docs/
├── logs/
├── output/
│   └── .gitkeep
│
├── tests/
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
Architecture
The project follows a modular, object-oriented architecture.
                    ┌─────────────────────┐
                    │       main.py       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      gui.py         │
                    │   CustomTkinter     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   pdf_manager.py    │
                    │   Service Facade    │
                    └──────┬───────┬──────┘
                           │       │
                ┌──────────┘       └──────────┐
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │pdf_operations.py│          │image_operations │
       │                 │          │      .py        │
       └────────┬────────┘          └────────┬────────┘
                │                            │
                └────────────┬───────────────┘
                             ▼
                    ┌─────────────────────┐
                    │      utils.py       │
                    │ Logging & Validation│
                    └─────────────────────┘

## Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd task-2-pdf-editor

2. Create a virtual environment
python -m venv .venv

3. Activate the virtual environment
Windows PowerShell:
.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

**Run the Application**
python main.py

The ALGORYX PDF Editor window will open.
## Usage
Open PDF
Click Open PDF, select a PDF file, and the first page will be displayed in the preview area.
Use Previous Page and Next Page to navigate through the document.
Merge PDFs
Click Merge PDFs, select two or more PDF files, and choose the output location.
Split PDF
Click Split PDF, select a PDF, and choose an output directory. Each page will be saved as an individual PDF.
Rotate Pages
Click Rotate Pages, select the PDF, enter page numbers such as:
1,3-5

Then select a rotation angle:
90
180
270

Delete Pages
Select the PDF and enter the pages to delete.
Example:
2,4-5

Reorder Pages
Enter the complete page order.
Example:
3,1,4,2

Each page must appear exactly once.
Extract Text
Select a PDF and choose a .txt output file. Extracted text is organized by page.
Add Watermark
Select a PDF, enter watermark text, and save the resulting PDF.
Password Protect
Select a PDF and provide a password and confirmation password. The resulting PDF is encrypted.
Images → PDF
Select one or more PNG/JPG images and save them as a PDF.
PDF → Images
Select a PDF, choose PNG or JPG, select the resolution, and choose an output folder.
# Error Handling
The application handles invalid and corrupted PDF files without terminating the application.
Errors are:
- Logged to logs/pdf_editor.log
- Displayed to the user through GUI error dialogs
- Converted into application-level exceptions where appropriate
**Logging**
Application logs are stored in:
logs/pdf_editor.log

Logs include successful operations and exceptions.
# Requirements
The project requires:
- Python 3.11 or later
- PyMuPDF
- Pillow
- CustomTkinter
Install all dependencies using:
pip install -r requirements.txt

# Testing
The project was tested for:
- PDF opening
- Page preview
- Page navigation
- PDF merging
- PDF splitting
- Page rotation
- Page deletion
- Page reordering
- Text extraction
- Watermarking
- Password protection
- Image-to-PDF conversion
- PDF-to-image conversion
- Invalid/corrupted PDF handling
# Security
Password-protected PDFs use PDF encryption through PyMuPDF.
Passwords should be handled securely and should not be stored in source code or logs.
# Internship Task
This project was developed for the ALGORYX Python Internship, Task 2: Python PDF Editor.
## Author
    Anuvardhan Chary
    B.Tech Computer Science & Engineering
## License
This project was developed for educational and internship purposes.
'@ | Set-Content README.md -Encoding UTF8