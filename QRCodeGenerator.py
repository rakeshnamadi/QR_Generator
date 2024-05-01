import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

def generate_qr_codes_to_pdf(file_path, qr_data_list, qr_size_list):
    c = canvas.Canvas(file_path, pagesize=letter)
    page_width, page_height = letter

    # Set margins and gap
    x_margin = 10 * mm  # Left and right margin
    y_margin = 10 * mm  # Top and bottom margin
    qr_gap = 5 * mm  # Gap between QR codes
    qr_row_gap = 5 * mm  # Gap between rows of QR codes

    qr_size = 10  # Fixed size for QR codes

    x_start = x_margin  # Start from left margin
    y_start = page_height - y_margin  # Start from top margin
    qr_counter = 0
    qr_row_start_x = x_start  # Store the starting x-coordinate of the current row
    qr_row_end_x = x_start  # Store the ending x-coordinate of the current row
    num_rows = 1  # Counter for number of rows

    for qr_data in qr_data_list:
        # Draw QR code
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

        # Add size text under each QR code
        size_text = f"{qr_size}X{qr_size}"
        # Adjust the font size
        font_size = 8
        text_width = c.stringWidth(size_text, "Helvetica", font_size)
        # Adjust the x-coordinate for the second text
        text_x = x_start + (qr_size * mm - text_width) / 2
        # Add an offset to the y-coordinate for the first text
        text_y = y_start - qr_size * mm - 5  # 5mm gap below QR code
        c.setFont("Helvetica", font_size)

        c.drawImage(img_path, x_start, y_start - qr_size * mm, width=qr_size * mm, height=qr_size * mm)
        c.drawString(text_x, text_y, size_text)

        # Update x position for next QR code
        qr_row_end_x = x_start + qr_size * mm  # Update the ending x-coordinate of the current row
        x_start += qr_size * mm + qr_gap
        qr_counter += 1

        if qr_counter >= 13:
            qr_counter = 0  # Reset QR counter
            x_start = 10 * mm  # Start new row from 10mm on X axis
            y_start -= qr_size * mm + qr_row_gap  # Move to the next row
            qr_row_start_x = x_start  # Update the starting x-coordinate of the new row
            qr_row_end_x = x_start  # Update the ending x-coordinate of the new row
            last_row_y = y_start + qr_size * mm  # Store the y-coordinate of the last row
            num_rows += 1
    print(num_rows, page_height*mm)
    # Adding cutting marks
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.5)
    x_margin = 5 * mm  # Left and right margin
    y_margin = 5 * mm

    # Top left corner
    c.line(x_margin, page_height - y_margin, x_margin + 5 * mm, page_height - y_margin)
    #print(x_margin, page_height - y_margin, x_margin + 5 * mm, page_height - y_margin)
    c.line(x_margin, page_height - y_margin, x_margin, page_height - y_margin - 5 * mm)

    # Top right corner
    c.line(page_width - x_margin, page_height - y_margin, page_width - x_margin - 5 * mm, page_height - y_margin)
    c.line(page_width - x_margin, page_height - y_margin, page_width - x_margin, page_height - y_margin - 5 * mm)

    # Bottom left corner
    bottom_left_y = (last_row_y + qr_size * num_rows)
    print(bottom_left_y, last_row_y, qr_size, num_rows)
    print(bottom_left_y*mm)
    bottom_left_y = page_height - bottom_left_y
    # Calculate the y-coordinate of the bottom left marker
    bottom_left_y = (y_start - qr_row_gap - qr_size * mm)- 5*mm

    # Draw the bottom left marker
    c.line(x_margin, bottom_left_y, x_margin + 5 * mm, bottom_left_y)
    c.line(x_margin, bottom_left_y, x_margin, bottom_left_y + 5 * mm)

    # Bottom right corner
    bottom_right_y = (y_start - qr_row_gap - qr_size * mm)- 5*mm
    print(bottom_right_y)
    c.line(page_width - x_margin, bottom_right_y, page_width - x_margin - 5 * mm, bottom_right_y)
    c.line(page_width - x_margin, bottom_right_y, page_width - x_margin, bottom_right_y + 5 * mm)

    c.save()

if __name__ == "__main__":
    qr_data_list = ["https://example.com"] * 30  # Only one URL repeated for demonstration
    generate_qr_codes_to_pdf("qr_codes1.pdf", qr_data_list, [10] * len(qr_data_list))  # QR size is 10mm