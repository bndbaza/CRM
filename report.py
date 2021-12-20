from reportlab.pdfgen import canvas

def Pdf():
    pdf = canvas.Canvas('My.pdf')
    pdf.setTitle('Title')
    pdf.setStrokeColorRGB(0,0,0)
    pdf.setFillColorRGB(0,0,255)
    pdf.rect(300,790,50,30,fill=1)
    pdf.setFillColorRGB(0,0,0)
    pdf.drawString(300,800,'1234567890')
    
    
    
    
    
    
    
    
    
    
    
    pdf.save()
