import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

class WebViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Package Manager")  # Change the title here
        self.set_default_size(800, 600)

        # Create a WebKitWebView
        webview = WebKit2.WebView()

        # Load a webpage (change the URL as needed)
        webview.load_uri("http://127.0.0.1:5000")

        # Create a scrolled window and add the WebView to it
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(webview)

        # Add the scrolled window to the main window
        self.add(scrolled_window)

        # Handle the destroy event
        self.connect("destroy", Gtk.main_quit)

        # Show all elements
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
