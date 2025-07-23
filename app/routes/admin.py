from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import User, QueueTicket
from extensions import db
from datetime import datetime

bp = Blueprint('admin', __name__)

# Admin Login
@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin_login.html')

# Admin Logout
@bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.admin_login'))

# Admin Dashboard
@bp.route('/admin/dashboard')
@login_required
def dashboard():
    status_filter = request.args.get('status', 'all')

    if status_filter == 'all':
        tickets = QueueTicket.query.order_by(QueueTicket.created_at).all()
    else:
        tickets = QueueTicket.query.filter_by(status=status_filter).order_by(QueueTicket.created_at).all()

    total_count = QueueTicket.query.count()
    waiting_count = QueueTicket.query.filter_by(status='waiting').count()
    skipped_count = QueueTicket.query.filter_by(status='skipped').count()
    served_count = QueueTicket.query.filter_by(status='served').count()

    return render_template('admin_dashboard.html',
                           tickets=tickets,
                           status_filter=status_filter,
                           total_count=total_count,
                           waiting_count=waiting_count,
                           skipped_count=skipped_count,
                           served_count=served_count)

# Call Ticket (POST only)
@bp.route('/admin/call/<int:ticket_id>', methods=['POST'])
@login_required
def call_ticket(ticket_id):
    ticket = QueueTicket.query.get_or_404(ticket_id)

    if ticket.status == 'waiting':
        # Mark previous called tickets as served
        called_tickets = QueueTicket.query.filter_by(status='called').all()
        for t in called_tickets:
            t.status = 'served'
            t.called_at = datetime.utcnow()

        ticket.status = 'called'
        ticket.called_at = datetime.utcnow()

        # Optionally count it as served for filters
        db.session.commit()

        return jsonify({'success': True, 'status': 'called'})
    else:
        return jsonify({'success': False, 'message': 'Only waiting tickets can be called.'})

# Skip Ticket (POST only)
@bp.route('/admin/skip/<int:ticket_id>', methods=['POST'])
@login_required
def skip_ticket(ticket_id):
    ticket = QueueTicket.query.get_or_404(ticket_id)

    if ticket.status in ['waiting', 'called']:
        ticket.status = 'skipped'
        db.session.commit()
        return jsonify({'success': True, 'status': 'skipped'})
    else:
        return jsonify({'success': False, 'message': 'Ticket cannot be skipped.'})

# Reset Queue (POST only)
@bp.route('/admin/reset', methods=['POST'])
@login_required
def reset_queue():
    try:
        QueueTicket.query.delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
