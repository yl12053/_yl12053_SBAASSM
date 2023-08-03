from striprtf.striprtf import rtf_to_text
def process(dirname):
    try:
        encoded = open(dirname).read()
        return (0, rtf_to_text(encoded).strip().replace("\0", ""))
    except UnicodeDecodeError:
        return (1, "File using unknown encoding.")
    except Exception as e:
        return (1, str(e))