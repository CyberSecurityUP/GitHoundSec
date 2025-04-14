# main.py

import sys
import os

# Adiciona o caminho do frontend e backend ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "frontend"))
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# Importa e executa a interface principal
from main_gui import GitHoundSecApp

if __name__ == "__main__":
    app = GitHoundSecApp()
    app.mainloop()
