from firewithinfilms import *
from firewithinfilms.models import *

app = create_app()
app.app_context().push()


hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
admin = User(username='admin', email='admin@admin.com', password=hashed_password, user_role='admin')
db.session.add(admin)
db.session.commit()