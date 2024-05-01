import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

def generate_qr_codes_to_pdf(file_path, qr_data_list, qr_size_list):
    c = canvas.Canvas(file_path, pagesize=letter)
    page_width, page_height = letter

    # Set margins and gap
    x_margin = 10 * mm  # Left margin
    y_margin = 10 * mm  # Top margin
    qr_gap = 5 * mm  # Gap between QR codes

    qr_size = 10  # Fixed size for QR codes

    x_start = x_margin  # Start from left margin
    y_start = page_height - y_margin  # Start from top margin

    for qr_data in qr_data_list:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_size,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="orange")  # Change background color to orange
        img_path = f"temp_qr_{qr_size}.png"
        img.save(img_path)

        # Draw QR code
        c.drawImage(img_path, x_start, y_start - qr_size * mm, width=qr_size * mm, height=qr_size * mm)

        # Add size text under each QR code
        size_text = f"{qr_size}X{qr_size}"
        # Adjust the font size
        font_size = 8
        text_width = c.stringWidth(size_text, "Helvetica", font_size)
        # Adjust the x-coordinate for the second text
        text_x = x_start + (qr_size * mm - text_width) / 2
        # Add an offset to the y-coordinate for the first text
        text_y = y_start - qr_size * mm - 5  # 10mm gap below QR code
        c.setFont("Helvetica", font_size)
        c.drawString(text_x, text_y, size_text)

        # Update x position for next QR code
        x_start += qr_size * mm + qr_gap

    c.save()

if __name__ == "__main__":
    qr_data_list = ["https://example.com"] * 14  # Only one URL repeated for demonstration
    generate_qr_codes_to_pdf("qr_codes.pdf", qr_data_list, [10] * len(qr_data_list))  # QR size is 10mm
