import time
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from gpiozero import LED, Button

led = LED(15)
button = Button(16)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        led_state = "LED is OFF" if led.value == 0 else "LED is ON"
        button_state = "Button is NOT pressed" if button.is_active else "Button is pressed"

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico W</title>
        </head>
        <body>
            <h1>Pico W HTTP Server</h1>
            <p>Hello, World!</p>
            <p>{}</p>
            <p>{}</p>
        </body>
        </html>
        """.format(led_state, button_state)

        self.wfile.write(html.encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
