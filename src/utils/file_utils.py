from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}

def allowed_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)
