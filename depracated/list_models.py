from google.generativeai.models import list_models
from google.generativeai.client import configure
import os

configure(api_key=os.environ.get("GOOGLE_API_KEY"))
for m in list_models():
    print(m.name)
