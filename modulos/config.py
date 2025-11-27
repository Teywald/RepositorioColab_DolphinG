import os

# Path absoluto a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # modulos/
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "dolphin_green.db"))