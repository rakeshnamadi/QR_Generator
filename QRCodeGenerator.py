from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

def generate_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    print(width, height)
    print("in mm: ", width * mm, height * mm)

    # Define dimensions of the grid
    border_size = 10 * mm
    usable_width = width - (2 * border_size)
    usable_height = height - (2 * border_size)
    box_size = 20 * mm
    print("1mm=", 1 * mm)
    # Calculate the number of rows and columns
    rows = int(usable_height / box_size)
    cols = int(usable_width / box_size)
    print("rows: ", rows, "cols: ", cols, "usable_height: ", usable_height, "usable_width: ", usable_width)
    # Calculate the starting point for the grid
    start_x = border_size
    print("start_x: ", start_x)
    start_y = height - border_size - usable_height
    print("start_y: ", start_y)

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * box_size
            print(x)
            y = start_y + (row * box_size)
            print(y)
            c.rect(x, y, box_size, box_size)

    # Draw "L" shapes at each corner with a 5mm distance from the grid
    l_shape_size = 5 * mm
    l_shape_distance = 5 * mm
    
    # Top left corner
    c.setStrokeColorRGB(0, 0, 0)
    c.line(start_x - l_shape_distance, start_y - l_shape_distance,
           start_x - l_shape_distance, start_y - l_shape_distance - l_shape_size)
    c.line(start_x - l_shape_distance, start_y - l_shape_distance,
           start_x - l_shape_distance - l_shape_size, start_y - l_shape_distance)

    # Top right corner
    c.line(width - start_x + l_shape_distance, start_y - l_shape_distance,
           width - start_x + l_shape_distance + l_shape_size, start_y - l_shape_distance)
    c.line(width - start_x + l_shape_distance, start_y - l_shape_distance,
           width - start_x + l_shape_distance, start_y - l_shape_distance - l_shape_size)

    # Bottom left corner
    c.line(start_x - l_shape_distance, height - start_y + l_shape_distance,
           start_x - l_shape_distance, height - start_y + l_shape_distance + l_shape_size)
    c.line(start_x - l_shape_distance, height - start_y + l_shape_distance,
           start_x - l_shape_distance - l_shape_size, height - start_y + l_shape_distance)

    # Bottom right corner
    c.line(width - start_x + l_shape_distance, height - start_y + l_shape_distance,
           width - start_x + l_shape_distance + l_shape_size, height - start_y + l_shape_distance)
    c.line(width - start_x + l_shape_distance, height - start_y + l_shape_distance,
           width - start_x + l_shape_distance, height - start_y + l_shape_distance + l_shape_size)

    c.save()

if __name__ == "__main__":
    generate_pdf("grid_with_border_and_L_shapes.pdf")
