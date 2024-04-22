import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FinMind 設定
SHIOAJI_API_Key = os.environ.get("FINMIND_API_KEY")