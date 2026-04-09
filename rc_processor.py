"""RC Card OCR Processing Module"""

import re
import os
from io import BytesIO

# These are optional - only imported when RC extraction is needed
reader = None

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        dict: Extracted text from PDF
    """
    try:
        import PyPDF2
        
        extracted_text = ""
        with open(pdf_path, 'rb') as file:
            reader_pdf = PyPDF2.PdfReader(file)
            for page in reader_pdf.pages:
                extracted_text += page.extract_text() + "\n"
        
        return {
            'success': True,
            'text': extracted_text,
            'confidence': 0.9,  # PDFs are generally more reliable
            'source': 'pdf'
        }
    except Exception as e:
        return {'success': False, 'error': str(e), 'text': '', 'source': 'pdf'}


def _initialize_ocr():
    """Initialize OCR reader (lazy loading)"""
    global reader
    if reader is None:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
    return reader


def extract_text_from_rc_image(image_path):
    """
    Extract all text from RC card image using OCR or PDF extraction
    
    Args:
        image_path (str): Path to the RC card image or PDF file
    
    Returns:
        dict: Extracted text and confidence scores
    """
    # Check if file is PDF
    if image_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(image_path)
    try:
        import cv2
        import numpy as np
        
        # Initialize OCR (lazy load)
        ocr = _initialize_ocr()
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return {'error': 'Could not read image', 'text': ''}
        
        # Extract text using EasyOCR
        results = ocr.readtext(image)
        
        # Format results
        extracted_text = '\n'.join([text[1] for text in results])
        
        return {
            'success': True,
            'text': extracted_text,
            'confidence': np.mean([text[2] for text in results]),
            'raw_results': results
        }
    except Exception as e:
        return {'success': False, 'error': str(e), 'text': ''}


def parse_rc_details(extracted_text):
    """
    Parse RC card extracted text and identify key details
    
    Args:
        extracted_text (str): Raw text extracted from RC card
    
    Returns:
        dict: Parsed RC details (rc_number, owner, vehicle_model, etc.)
    """
    text = extracted_text.upper()
    details = {
        'rc_number': None,
        'owner': None,
        'vehicle_model': None,
        'chassis_number': None,
        'engine_number': None,
        'registration_date': None,
        'fuel_type': None,
        'class': None,
        'confidence': 0
    }
    
    try:
        # Extract RC Number (format: XX-XX-XX-XXXX)
        rc_match = re.search(r'([A-Z]{2}[-]?[0-9]{2}[-]?[A-Z]{2}[-]?[0-9]{4})', text)
        if rc_match:
            details['rc_number'] = rc_match.group(1).replace(' ', '')
        
        # Extract Owner name (usually after "Owner" keyword)
        owner_match = re.search(r'(?:OWNER|ओनर)[:\s]+([A-Z\s\.]+)', text)
        if owner_match:
            owner = owner_match.group(1).strip()
            # Clean up owner name
            owner = re.sub(r'[0-9]', '', owner)  # Remove numbers
            details['owner'] = owner[:50]  # Limit to 50 chars
        
        # Extract Vehicle Model/Name
        model_keywords = ['MODEL', 'MAKE', 'व्हीकल', 'VEHICLE']
        for keyword in model_keywords:
            pattern = rf'{keyword}[:\s]+([A-Z\s\d\-\.]+)'
            model_match = re.search(pattern, text)
            if model_match:
                details['vehicle_model'] = model_match.group(1).strip()[:50]
                break
        
        # Extract Chassis Number (usually 17 chars)
        chassis_match = re.search(r'(?:CHASSIS|चेसिस)[:\s]+([A-Z0-9]{17,})', text)
        if chassis_match:
            details['chassis_number'] = chassis_match.group(1).strip()
        
        # Extract Engine Number
        engine_match = re.search(r'(?:ENGINE|इंजन)[:\s]+([A-Z0-9]+)', text)
        if engine_match:
            details['engine_number'] = engine_match.group(1).strip()
        
        # Extract Fuel Type (PETROL, DIESEL, etc.)
        fuel_match = re.search(r'(?:FUEL|ईंधन)[:\s]+([A-Z\s]+)', text)
        if fuel_match:
            details['fuel_type'] = fuel_match.group(1).strip()
        
        # Extract Class (Two Wheeler, Four Wheeler, etc.)
        class_match = re.search(r'(?:CLASS|वर्ग)[:\s]+([A-Z\s\d]+)', text)
        if class_match:
            details['class'] = class_match.group(1).strip()
        
        # Extract Registration Date (DD/MM/YYYY or YYYY-MM-DD)
        date_match = re.search(r'(?:DATE|दिनांक)[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{4})', text)
        if date_match:
            details['registration_date'] = date_match.group(1).strip()
        
        return details
    
    except Exception as e:
        print(f"Error parsing RC details: {str(e)}")
        return details


def process_rc_card(image_path):
    """
    Complete RC card processing pipeline
    
    Args:
        image_path (str): Path to RC card image
    
    Returns:
        dict: Processed RC details ready to fill form
    """
    try:
        # Step 1: Extract text from image
        extraction = extract_text_from_rc_image(image_path)
        
        if not extraction.get('success'):
            return {
                'success': False,
                'error': extraction.get('error', 'OCR failed'),
                'data': {}
            }
        
        # Step 2: Parse extracted text
        parsed_details = parse_rc_details(extraction['text'])
        
        return {
            'success': True,
            'confidence': extraction.get('confidence', 0),
            'data': parsed_details,
            'raw_text': extraction['text']
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': {}
        }
