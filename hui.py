import datetime
from src.database.models import Contact

today = datetime.date.today()
contact = Contact(birthday=datetime.date(2000, 4, 23))

print(contact.birthday, type(contact.birthday))

