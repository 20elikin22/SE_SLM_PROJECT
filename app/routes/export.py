<<<<<<< HEAD
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
            writer.writerow([ticket.queue_number, ticket.service_type, ticket.status, ticket.created_at])
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
=======
from flask import Blueprint, Response
from app.models import QueueTicket
import csv
from io import StringIO
from datetime import datetime

bp = Blueprint('export', __name__)


@bp.route('/export/csv')
def export_csv():
    """Export tickets as CSV (called tickets will be marked as served)."""
    output = StringIO()
    writer = csv.writer(output)

    # Write CSV headers
    writer.writerow(["Queue Number", "Service Type", "Status", "Created At", "Called At"])

    tickets = QueueTicket.query.order_by(QueueTicket.queue_number).all()

    for ticket in tickets:
        # Change 'called' to 'served' just for the export
        status = ticket.status
        if status == "called":
            status = "served"

        writer.writerow([
            ticket.queue_number,
            ticket.service_type,
            status,
            ticket.created_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.created_at else '',
            ticket.called_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.called_at else ''
        ])

    output.seek(0)

    # Return CSV as a downloadable response
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=tickets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    return response
>>>>>>> 51f376742c835a233ee914ec905b78dabc47c0e3
