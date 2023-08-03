import Base, Background

def main():
    from Modules import ModuleSpelling
    import webview
    webview.create_window('Hello world', 'https://www.google.com')
    webview.start(gui='qt')

Background.run(main)