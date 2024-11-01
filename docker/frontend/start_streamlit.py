import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

port = os.getenv("STREAMLIT_PORT", "80")

subprocess.run(["streamlit", "run", "app.py", "--server.port", port, "--server.address=0.0.0.0"])
