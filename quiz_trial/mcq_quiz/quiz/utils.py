import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import white

def generate_filled_certificate(name, score, date, image_path):
    output = io.BytesIO()

    
    page_size = landscape(A4)
    can = canvas.Canvas(output, pagesize=page_size)


    bg_image = ImageReader(image_path)
    can.drawImage(bg_image, 0, 0, width=page_size[0], height=page_size[1])

    can.setFont("Helvetica-Bold", 24)
    can.setFillColor(white)

    
    can.drawCentredString(page_size[0] / 2, 240, name)
    can.setFont("Helvetica-Bold", 13)
    can.drawCentredString( 338.5, 174.65, f"{score} points")
    can.setFont("Helvetica", 15)
    can.drawCentredString(680, 200, f" {date}")

    can.showPage()
    can.save()
    output.seek(0)

    return output
