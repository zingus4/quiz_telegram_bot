import os
from pathlib import Path
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()
from django.conf import settings
# load_dotenv()

BOT_TOKEN = settings.BOT_TOKEN
admin_id = int(settings.ADMIN_ID)
#lp_token = os.getenv("LIQPAY_TOKEN")
host = "localhost"

I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
