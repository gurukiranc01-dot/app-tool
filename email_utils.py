"""Email utility functions for sending notifications"""

import os
from flask import render_template_string
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_email(app):
    """Initialize Flask-Mail with app configuration"""
    # Email configuration already set in app config
    mail.init_app(app)


def send_email(subject, recipients, template=None, data=None, body_text=None):
    """
    Send an email notification
    
    Args:
        subject (str): Email subject
        recipients (list): List of email addresses
        template (str): Template name (without .html extension)
        data (dict): Context data for the template
        body_text (str): Plain text body (used if no template)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # If no recipients provided, use default admin email
        if not recipients:
            recipients = [os.getenv('MAIL_DEFAULT_SENDER', 'admin@bikevault.com')]
        
        # Prepare message body
        if template:
            # Render HTML template if provided
            html_body = render_template_string(
                get_email_template(template),
                **data
            )
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=html_body,
                sender=os.getenv('MAIL_DEFAULT_SENDER', 'noreply@bikevault.com')
            )
        else:
            # Use plain text body
            msg = Message(
                subject=subject,
                recipients=recipients,
                body=body_text or "",
                sender=os.getenv('MAIL_DEFAULT_SENDER', 'noreply@bikevault.com')
            )
        
        # Send the email
        mail.send(msg)
        print(f"✓ Email sent to {recipients}: {subject}")
        return True
    except Exception as e:
        print(f"✗ Error sending email: {str(e)}")
        return False


def get_email_template(template_name):
    """
    Get HTML template for email
    
    Args:
        template_name (str): Name of the template
    
    Returns:
        str: HTML template string
    """
    templates = {
        'new_vehicle': '''
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
                    .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px 5px 0 0; }
                    .content { background-color: white; padding: 20px; border-radius: 0 0 5px 5px; }
                    .field { margin: 10px 0; }
                    .label { font-weight: bold; color: #2c3e50; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>✓ New Vehicle Received</h2>
                    </div>
                    <div class="content">
                        <p>A new vehicle has been added to the system.</p>
                        
                        <div class="field">
                            <span class="label">Vehicle Name:</span> {{ vehicle_name }}
                        </div>
                        <div class="field">
                            <span class="label">RC Number:</span> {{ rc_number }}
                        </div>
                        <div class="field">
                            <span class="label">Owner:</span> {{ owner }}
                        </div>
                        <div class="field">
                            <span class="label">Received On:</span> {{ received_on }}
                        </div>
                        <div class="field">
                            <span class="label">Received By:</span> {{ received_by }}
                        </div>
                        
                        <p style="margin-top: 20px; color: #666; font-size: 12px;">
                            This is an automated notification from Bike Vault System.
                        </p>
                    </div>
                </div>
            </body>
            </html>
        ''',
        
        'test_completed': '''
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
                    .header { background-color: #27ae60; color: white; padding: 20px; border-radius: 5px 5px 0 0; }
                    .content { background-color: white; padding: 20px; border-radius: 0 0 5px 5px; }
                    .field { margin: 10px 0; }
                    .label { font-weight: bold; color: #27ae60; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>✓ Test Completed</h2>
                    </div>
                    <div class="content">
                        <p>Vehicle testing has been marked as completed.</p>
                        
                        <div class="field">
                            <span class="label">Vehicle Name:</span> {{ vehicle_name }}
                        </div>
                        <div class="field">
                            <span class="label">RC Number:</span> {{ rc_number }}
                        </div>
                        <div class="field">
                            <span class="label">Owner:</span> {{ owner }}
                        </div>
                        <div class="field">
                            <span class="label">Completion Date:</span> {{ completion_date }}
                        </div>
                        <div class="field">
                            <span class="label">Completed By:</span> {{ completed_by }}
                        </div>
                        
                        <p style="margin-top: 20px; color: #666; font-size: 12px;">
                            This is an automated notification from Bike Vault System.
                        </p>
                    </div>
                </div>
            </body>
            </html>
        ''',
        
        'vehicle_returned': '''
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
                    .header { background-color: #e74c3c; color: white; padding: 20px; border-radius: 5px 5px 0 0; }
                    .content { background-color: white; padding: 20px; border-radius: 0 0 5px 5px; }
                    .field { margin: 10px 0; }
                    .label { font-weight: bold; color: #e74c3c; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>✓ Vehicle Returned</h2>
                    </div>
                    <div class="content">
                        <p>Vehicle has been marked as returned.</p>
                        
                        <div class="field">
                            <span class="label">Vehicle Name:</span> {{ vehicle_name }}
                        </div>
                        <div class="field">
                            <span class="label">RC Number:</span> {{ rc_number }}
                        </div>
                        <div class="field">
                            <span class="label">Owner:</span> {{ owner }}
                        </div>
                        <div class="field">
                            <span class="label">Return Date:</span> {{ return_date }}
                        </div>
                        <div class="field">
                            <span class="label">Returned By:</span> {{ returned_by }}
                        </div>
                        
                        <p style="margin-top: 20px; color: #666; font-size: 12px;">
                            This is an automated notification from Bike Vault System.
                        </p>
                    </div>
                </div>
            </body>
            </html>
        '''
    }
    
    return templates.get(template_name, '')
