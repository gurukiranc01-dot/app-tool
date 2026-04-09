from app import app
from models import db

with app.app_context():
    db.create_all()
    print('✓ Database created successfully with all columns including:')
    print('  - scratches_image')
    print('  - dents_image')
    print('  - glass_damage_image')
    print('  - lights_image')
