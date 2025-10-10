# src/tests/conftest.py
import sys
import os

# Додаємо кореневу директорію проєкту в шлях імпорту
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
