import tkinter as tk
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")

        self.mode = tk.StringVar(value="single")
        self.qr_size = tk.StringVar(value="10")
        self.saved_location = tk.StringVar(value="")

        self.single_entry_frame = tk.Frame(master)
        self.bulk_entry_frame = tk.Frame(master)
        self.random_entry_frame = tk.Frame(master)

        self.create_widgets()
        self.show_frame()

    def create_widgets(self):
        # Radio buttons to select entry mode
        tk.Radiobutton(self.master, text="Single Entry", variable=self.mode, value="single",
                       command=self.show_frame).grid(row=0, column=0, padx=10, pady=5)
        tk.Radiobutton(self.master, text="Bulk Entry", variable=self.mode, value="bulk",
                       command=self.show_frame).grid(row=0, column=1, padx=10, pady=5)
        tk.Radiobutton(self.master, text="Random Entry", variable=self.mode, value="random",
                       command=self.show_frame).grid(row=0, column=2, padx=10, pady=5)

        # QR Size options
        qr_sizes = [("10x10", "10"), ("20x20", "20"), ("30x30", "30")]
        for size, value in qr_sizes:
            tk.Radiobutton(self.master, text=size, variable=self.qr_size, value=value).grid(row=1, column=qr_sizes.index((size, value)), padx=10, pady=5)

        # Label to show saved location
        self.saved_location_label = tk.Label(self.master, textvariable=self.saved_location)

        # Single Entry Frame
        tk.Label(self.single_entry_frame, text="Enter TEXT:").pack()
        self.single_entry_url = tk.Entry(self.single_entry_frame)
        self.single_entry_url.pack()
        self.single_entry_generate_btn = tk.Button(self.single_entry_frame, text="Generate QR",
                                                   command=self.generate_single_qr)
        self.single_entry_generate_btn.pack()

        # Bulk Entry Frame
        tk.Label(self.bulk_entry_frame, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.bulk_entry_text = tk.Entry(self.bulk_entry_frame)
        self.bulk_entry_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.bulk_entry_frame, text="From:").grid(row=1, column=0, padx=5, pady=5)
        self.bulk_entry_from = tk.Entry(self.bulk_entry_frame)
        self.bulk_entry_from.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.bulk_entry_frame, text="To:").grid(row=2, column=0, padx=5, pady=5)
        self.bulk_entry_to = tk.Entry(self.bulk_entry_frame)
        self.bulk_entry_to.grid(row=2, column=1, padx=5, pady=5)
        self.bulk_entry_generate_btn = tk.Button(self.bulk_entry_frame, text="Generate QR",
                                                 command=self.generate_bulk_qr)
        self.bulk_entry_generate_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # Random Entry Frame
        tk.Label(self.random_entry_frame, text="Enter QR Code Text:").grid(row=0, column=0, padx=5, pady=5)
        self.random_entry_text = tk.Text(self.random_entry_frame, height=5, width=50)
        self.random_entry_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.random_entry_frame, text="Enter QR Code Labeling:").grid(row=1, column=0, padx=5, pady=5)
        self.random_entry_labeling = tk.Text(self.random_entry_frame, height=5, width=50)
        self.random_entry_labeling.grid(row=1, column=1, padx=5, pady=5)
        self.random_entry_generate_btn = tk.Button(self.random_entry_frame, text="Generate QR",
                                                   command=self.generate_random_qr)
        self.random_entry_generate_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Place frames
        self.single_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.bulk_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.random_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.saved_location_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def show_frame(self):
        mode = self.mode.get()
        if mode == "single":
            self.single_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
            self.bulk_entry_frame.grid_forget()
            self.random_entry_frame.grid_forget()
        elif mode == "bulk":
            self.single_entry_frame.grid_forget()
            self.bulk_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
            self.random_entry_frame.grid_forget()
        elif mode == "random":
            self.single_entry_frame.grid_forget()
            self.bulk_entry_frame.grid_forget()
            self.random_entry_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def generate_single_qr(self):
        text = self.single_entry_url.get().upper()
        if text:
            file_path = f"{text.replace('/', '-')}.pdf"
            self.generate_qr_to_pdf(file_path, [text])
            self.saved_location.set(f"PDF saved at: {file_path}")

    def generate_bulk_qr(self):
        text = self.bulk_entry_text.get().upper()
        frm = int(self.bulk_entry_from.get())
        to = int(self.bulk_entry_to.get())
        qr_data_list = [f"{text}{str(i).zfill(3)}" for i in range(frm, to + 1)]
        file_path = f"{text.replace('/', '-')} ({frm}-{to}).pdf"
        self.generate_qr_to_pdf(file_path, qr_data_list)
        self.saved_location.set(f"PDF saved at: {file_path}")

    def generate_random_qr(self):
        qr_data = self.random_entry_text.get("1.0", "end-1c").upper().split("\n")
        qr_labeling = self.random_entry_labeling.get("1.0", "end-1c").split("\n")
        qr_data_list = [data.strip() for data in qr_data if data.strip()]
        qr_labeling_list = [label.strip() for label in qr_labeling if label.strip()]
        if qr_data_list:
            file_path = f"random_qr.pdf"
            self.generate_qr_to_pdf(file_path, qr_data_list, qr_labeling_list)
            self.saved_location.set(f"PDF saved at: {file_path}")

    def generate_qr_to_pdf(self, file_path, qr_data_list, qr_labeling_list=None):
        qr_size = int(self.qr_size.get())
        qr_per_row = 13 if qr_size == 10 else (8 if qr_size == 20 else 5)

        c = canvas.Canvas(file_path, pagesize=letter)
        page_width, page_height = letter

        x_start = 10 * mm
        y_start = page_height - 10 * mm

        qr_gap = 5 * mm
        qr_row_gap = 5 * mm

        qr_counter = 0
        num_rows = 1

        for qr_data, qr_labeling in zip(qr_data_list, qr_labeling_list or [""] * len(qr_data_list)):
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=qr_size,
                border=2,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="orange")
            img_path = f"temp_qr_{qr_size}.png"
            img.save(img_path)

            size_text = qr_labeling if qr_labeling else qr_data
            font_size = 8

            text_x = x_start + (qr_size * mm - c.stringWidth(size_text, "Helvetica", font_size)) / 2
            text_y = y_start - qr_size * mm - 5
            c.setFont("Helvetica", font_size)

            c.drawImage(img_path, x_start, y_start - qr_size * mm, width=qr_size * mm, height=qr_size * mm)
            c.drawString(text_x, text_y, size_text)

            qr_row_end_x = x_start + qr_size * mm
            x_start += qr_size * mm + qr_gap
            qr_counter += 1

            if qr_counter >= qr_per_row:
                qr_counter = 0
                x_start = 10 * mm
                y_start -= qr_size * mm + qr_row_gap
                qr_row_start_x = x_start
                qr_row_end_x = x_start
                num_rows += 1

                if y_start < 10 * mm:
                    c.showPage()  # Add a new page if the images exceed the page
                    y_start = page_height - 10 * mm

        bottom_left_y = (y_start - qr_row_gap - qr_size * mm) - 5 * mm
        bottom_right_y = bottom_left_y

        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.5)

        x_margin = 5 * mm
        y_margin = 5 * mm

        c.line(x_margin, page_height - y_margin, x_margin + 5 * mm, page_height - y_margin)
        c.line(x_margin, page_height - y_margin, x_margin, page_height - y_margin - 5 * mm)

        c.line(page_width - x_margin, page_height - y_margin, page_width - x_margin - 5 * mm, page_height - y_margin)
        c.line(page_width - x_margin, page_height - y_margin, page_width - x_margin, page_height - y_margin - 5 * mm)

        c.line(x_margin, bottom_left_y, x_margin + 5 * mm, bottom_left_y)
        c.line(x_margin, bottom_left_y, x_margin, bottom_left_y + 5 * mm)

        c.line(page_width - x_margin, bottom_right_y, page_width - x_margin - 5 * mm, bottom_right_y)
        c.line(page_width - x_margin, bottom_right_y, page_width - x_margin, bottom_right_y + 5 * mm)
        
        c.save()


def main():
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
