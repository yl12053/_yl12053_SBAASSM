def process(dirname):
    try:
        return (0, open(dirname).read().strip())
    except UnicodeDecodeError:
        return (1, "File using unknown encoding.")
    except Exception as e:
        return (1, str(e))