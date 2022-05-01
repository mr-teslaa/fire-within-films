from firewithinfilms import *
from firewithinfilms.models import *

app = create_app()
app.app_context().push()

db.create_all()