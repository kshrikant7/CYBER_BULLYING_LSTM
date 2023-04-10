from tempfile import mkdtemp

DEBUG = True
TEMPLATES_AUTO_RELOAD = True
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"