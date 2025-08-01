from flask import Blueprint, Response, render_template, make_response
from app.models import QueueTicket
from io import BytesIO
import csv
from xhtml2pdf import pisa

bp = Blueprint('export', __name__)

# Export CSV
@bp.route('/export/csv')
def export_csv():
    tickets = QueueTicket.query.all()

    def generate():
        data = BytesIO()
        writer = csv.writer(data)
        writer.writerow(["Queue Number", "Service Type", "Status", "Created At"])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for ticket in tickets:
            status = "served" if ticket.status == "called" else ticket.status
            writer.writerow([ticket.queue_number, ticket.service_type, status, ticket.created_at])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=tickets.csv"}
    )


# Export PDF using xhtml2pdf
@bp.route('/export/pdf')
def export_pdf():
    tickets = QueueTicket.query.all()

    # Render the template into HTML
    html = render_template("export_pdf.html", tickets=tickets)

    # Generate PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    if pisa_status.err:
        return "Error generating PDF", 500

    pdf.seek(0)
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=tickets.pdf'
    return response