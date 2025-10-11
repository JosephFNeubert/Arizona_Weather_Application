import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
print("hi")
print(os.getenv("KEY"))
