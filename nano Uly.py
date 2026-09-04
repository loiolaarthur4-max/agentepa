import sys
import os

# Força a codificação do sistema para UTF-8 no Python
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st
from google import genai
from google.genai import types
# ... resto do seu código
