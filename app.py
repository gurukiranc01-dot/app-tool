from flask import Flask, request, jsonify, render_template, send_file, redirect, flash
from flask_login import LoginManager, login_required, current_user
from models import db, User, Vehicle
from routes import routes
from config import config
from email_service import mail
from io import BytesIO
from datetime import datetime, timedelta
from sqlalchemy import func
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors

app = Flask(__name__)

# Load configuration based on FLASK_ENV
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

db.init_app(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(routes)

# CREATE DB + DEFAULT USERS
with app.app_context():
    db.create_all()

    # Create default users if they don't exist
    if not User.query.first():
        try:
            db.session.add(User(username="admin", password="admin123", role="Admin"))
            db.session.add(User(username="user", password="user123", role="User"))
            db.session.add(User(username="eng", password="eng123", role="Engineer"))
            db.session.commit()
            print("✓ Default users created successfully")
        except Exception as e:
            print(f"ℹ️ Users already exist: {str(e)}")
            db.session.rollback()

    # Create demo vehicles ONLY if no vehicles exist
    if Vehicle.query.count() == 0:
        try:
            db.session.add(Vehicle(
                name="Pulsar NS200",
                rc="KA-01-AB-1234",
                chassis="MBLHA10EJ8M123456",
                owner="Bajaj",
                received_on="2026-02-26",
                status="In Testing"
            ))
            db.session.add(Vehicle(
                name="Classic 350",
                rc="MH-12-CD-5678",
                chassis="MBLHA10EJ8M789012",
                owner="Royal Enfield",
                received_on="2026-01-15",
                status="Returned"
            ))
            db.session.commit()
            print("✓ Demo vehicles created successfully")
        except Exception as e:
            print(f"ℹ️ Demo vehicles initialization info: {str(e)}")
            db.session.rollback()

# ===== ADMIN PANEL =====
# (Admin route now handled by routes.py blueprint for consistency)


# ===== ADMIN API ROUTES =====

@app.route('/api/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != "Admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json() or request.form
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'User').strip()
    
    # Validation
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if role not in ['Admin', 'User', 'Engineer']:
        return jsonify({'error': 'Invalid role'}), 400
    
    try:
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User "{username}" created successfully',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'role': new_user.role
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != "Admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Prevent deleting self
    if current_user.id == user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User "{username}" deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/edit_user/<int:user_id>', methods=['PUT'])
@login_required
def edit_user(user_id):
    if current_user.role != "Admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '').strip()
        
        # Validate inputs
        if not username or not role:
            return jsonify({'error': 'Username and role are required'}), 400
        
        if role not in ['Admin', 'User', 'Engineer']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Check if username is taken (by another user)
        existing_user = User.query.filter(User.username == username, User.id != user_id).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Update fields
        user.username = username
        user.role = role
        
        # Update password if provided
        if password:
            if len(password) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            user.password = password
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User "{username}" updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_report', methods=['GET'])
@login_required
def generate_report():
    if current_user.role != "Admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Create PDF with proper margins for centered header
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        bikevault_style = ParagraphStyle(
            'BikeVault',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.white,
            spaceAfter=0,
            alignment=1,  # Center
            leading=24,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#DC2626'),
            spaceAfter=0,
            alignment=1,  # Center
            leading=12,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Professional centered header with Logo on top
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'bosch.png')
        logo = Image(logo_path, width=1.2*inch, height=1.0*inch)
        bikevault_text = Paragraph("BikeVault", bikevault_style)
        subtitle_text = Paragraph("TWO WHEELER & POWERSPORTS TESTING CENTRE", subtitle_style)
        
        # Create centered header table - single column, full width
        header_table = Table([
            [logo],
            [bikevault_text],
            [subtitle_text]
        ], colWidths=[5.5*inch])
        
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 2), 'CENTER'),
            ('VALIGN', (0, 0), (0, 2), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 2), 0),
            ('RIGHTPADDING', (0, 0), (0, 2), 0),
            ('TOPPADDING', (0, 0), (0, 2), 0),
            ('BOTTOMPADDING', (0, 0), (0, 2), 0)
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Generated date
        date_text = Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Section
        elements.append(Paragraph("📊 SUMMARY", heading_style))
        
        total_users = User.query.count()
        total_vehicles = Vehicle.query.count()
        testing = Vehicle.query.filter_by(status='In Testing').count()
        returned = Vehicle.query.filter_by(status='Returned').count()
        success_rate = (returned/total_vehicles*100) if total_vehicles > 0 else 0
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Users', str(total_users)],
            ['Total Vehicles', str(total_vehicles)],
            ['In Testing', str(testing)],
            ['Returned', str(returned)],
            ['Success Rate', f"{success_rate:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F4F6')])
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Vehicles Section
        elements.append(Paragraph("🚙 VEHICLES", heading_style))
        
        vehicles = Vehicle.query.all()
        vehicle_data = [['ID', 'Vehicle Name', 'Plate', 'Status', 'Received', 'Returned']]
        for v in vehicles:
            # Safe date formatting
            received_date = 'N/A'
            if v.received_on:
                if isinstance(v.received_on, str):
                    received_date = v.received_on
                else:
                    received_date = v.received_on.strftime('%Y-%m-%d')
            
            returned_date = 'Pending'
            if v.end_date:  # Changed from returned_on to end_date
                if isinstance(v.end_date, str):
                    returned_date = v.end_date
                else:
                    returned_date = v.end_date.strftime('%Y-%m-%d')
            
            vehicle_data.append([
                str(v.id),
                v.name[:15],  # Truncate for table
                v.number_plate or 'N/A',
                v.status,
                received_date,
                returned_date
            ])
        
        vehicles_table = Table(vehicle_data, colWidths=[0.6*inch, 1.4*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        vehicles_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F4F6')])
        ]))
        elements.append(vehicles_table)
        
        # Build PDF
        doc.build(elements)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'BikeVault_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        print(f"Report generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ===== QR CODE ROUTES (Using Online API - No Pillow Needed) =====
@app.route('/vehicle_qr/<int:vehicle_id>')
def vehicle_qr(vehicle_id):
    """Generate QR code using online API and redirect to it"""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    qr_data = f"{request.host_url.rstrip('/')}vehicle/{vehicle_id}"
    
    # Use QR Server API (free, no dependencies needed)
    import urllib.parse
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(qr_data)}"
    
    return redirect(qr_url)

@app.route('/download_qr/<int:vehicle_id>')
def download_qr(vehicle_id):
    """Download QR code using online API"""
    import urllib.request
    import urllib.parse
    
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    qr_data = f"{request.host_url.rstrip('/')}vehicle/{vehicle_id}"
    
    # Use QR Server API
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(qr_data)}"
    
    try:
        # Download QR code image
        response = urllib.request.urlopen(qr_url)
        img_io = BytesIO(response.read())
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'QR_Vehicle_{vehicle.name}_{vehicle_id}.png'
        )
    except Exception as e:
        return jsonify({'error': 'Failed to generate QR code'}), 500

@app.route('/api/vehicle/<int:vehicle_id>')
def get_vehicle_json(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        'id': vehicle.id,
        'name': vehicle.name,
        'rc': vehicle.rc,
        'chassis': vehicle.chassis,
        'engine': vehicle.engine or 'N/A',
        'owner': vehicle.owner or 'N/A',
        'status': vehicle.status,
        'received_on': str(vehicle.received_on),
        'cc': vehicle.cc or 'N/A',
        'gears': vehicle.gears or 'N/A',
        'fuel': vehicle.fuel or 'N/A',
        'oil': vehicle.oil or 'N/A',
    })

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    # For production, don't use debug mode
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)