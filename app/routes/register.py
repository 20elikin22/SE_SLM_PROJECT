from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import QueueTicket
from extensions import db

bp = Blueprint('register', __name__)

SERVICE_TYPES = ['Bank', 'Cafe', 'Clinic', 'Tech Support']

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        service_type = request.form.get('service_type')

        if service_type not in SERVICE_TYPES:
            flash('Invalid service type selected.', 'danger')
            return redirect(url_for('register.register'))

        # Step 1: Create ticket (without queue_number)
        ticket = QueueTicket(service_type=service_type)
        db.session.add(ticket)
        db.session.commit()

        # Step 2: Set queue_number after we get the ID
        ticket.queue_number = ticket.id
        db.session.commit()

        # Step 3: Count how many are ahead
        ahead_count = QueueTicket.query.filter(
            QueueTicket.id < ticket.id,
            QueueTicket.service_type == service_type,
            QueueTicket.status == 'waiting'
        ).count()

        estimated_wait = (ahead_count + 1) * 3  # 3 mins per person

        return render_template('ticket_info.html',
                               ticket=ticket,
                               position=ahead_count,
                               estimated_wait=estimated_wait)

    return render_template('register.html', service_types=SERVICE_TYPES)
