"""Email utility module for sending notifications"""
from flask_mail import Mail, Message
from flask import current_app
from datetime import datetime

mail = Mail()

def send_admin_notification(subject, vehicle_name, action, details=""):
    """
    Send email notification to admin about vehicle updates
    
    Args:
        subject: Email subject
        vehicle_name: Name of the vehicle
        action: Action performed (e.g., "Vehicle Added", "Status Changed")
        details: Additional details about the action
    """
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL')
        
        # Build email body
        body = f"""
BikeVault System Notification

Action: {action}
Vehicle: {vehicle_name}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Details:
{details}

---
This is an automated notification from BikeVault System.
Please do not reply to this email.
        """
        
        msg = Message(
            subject=f"[BikeVault] {subject}",
            recipients=[admin_email],
            body=body,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_vehicle_added_notification(vehicle_name, rc_number, owner, received_date):
    """Send notification when new vehicle is added"""
    details = f"""
Vehicle Name: {vehicle_name}
RC Number: {rc_number}
Owner: {owner}
Received Date: {received_date}
Status: In Testing
    """
    return send_admin_notification(
        "New Vehicle Added",
        vehicle_name,
        "Vehicle Received",
        details
    )


def send_status_changed_notification(vehicle_name, old_status, new_status):
    """Send notification when vehicle status changes"""
    details = f"""
Vehicle Name: {vehicle_name}
Previous Status: {old_status}
New Status: {new_status}
Changed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    return send_admin_notification(
        f"Status Changed: {old_status} → {new_status}",
        vehicle_name,
        "Status Changed",
        details
    )


def send_user_added_notification(username, role):
    """Send notification when new user is added"""
    details = f"""
Username: {username}
Role: {role}
Added At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    return send_admin_notification(
        "New User Added",
        "N/A",
        "User Created",
        details
    )


def send_vehicle_returned_notification(vehicle_name, return_date, end_date):
    """Send notification when vehicle is returned"""
    details = f"""
Vehicle Name: {vehicle_name}
Return Date: {return_date}
End Date: {end_date}
Returned At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    return send_admin_notification(
        "Vehicle Returned",
        vehicle_name,
        "Vehicle Returned",
        details
    )


def send_test_email(recipient_email):
    """Send test email to verify configuration"""
    try:
        msg = Message(
            subject="[BikeVault] Test Email",
            recipients=[recipient_email],
            body="This is a test email from BikeVault System.\n\nIf you received this, email configuration is working correctly!",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending test email: {str(e)}")
        return False
