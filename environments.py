import json
import os

from dotenv import load_dotenv

load_dotenv()

model_key_json = os.getenv("MODEL_KEY")
MODEL_KEY = json.loads(model_key_json)
assert MODEL_KEY is not None, "MODEL_KEY not initialized"
