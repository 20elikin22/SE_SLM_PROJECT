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