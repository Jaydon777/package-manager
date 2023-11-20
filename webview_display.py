import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

class WebViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Package Manager")
        self.set_default_size(800, 600)

        webview = WebKit2.WebView()

        webview.load_uri("http://127.0.0.1:5000")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(webview)

        self.add(scrolled_window)

        # Handle the destroy event
        self.connect("destroy", Gtk.main_quit)

        self.show_all()

    def run(self):
        # Run the Gtk main loop
        Gtk.main()

# If this script is run directly, create the WebViewWindow and run the application
if __name__ == "__main__":
    # Initialize Gtk
    Gtk.init()

    # Create the WebViewWindow
    win = WebViewWindow()

    # Run the Gtk main loop
    win.run()
