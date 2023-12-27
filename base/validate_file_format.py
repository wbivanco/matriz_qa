ALLOWED_EXTENSIONS = {"pptx", "py", "js"}

def allowed_file(filename):    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


