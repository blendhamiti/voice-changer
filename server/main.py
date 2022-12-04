from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
from requests_toolbelt.multipart import decoder
import os

hostName = "localhost"
serverPort = 8081


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>Voice Changer Backend</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This means the server is working.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content_type = self.headers.get('Content-Type')
        content_len = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_len)
        data = decoder.MultipartDecoder(body, content_type).parts

        voice = None
        env = None

        for field in data:
            headers = str(field.headers)
            if "name=\"voice\"" in headers:
                voice = field.content
            if "name=\"env\"" in headers:
                env = field.content.decode("utf-8")

        dir = os.path.dirname(__file__)
        input = "input.wav"
        output = 'output.wav'

        with open(os.path.join(dir, input), 'wb') as file:
            file.write(voice)

        cmd = f"octave convolution.m {input} sounds/{env}.wav"
        subprocess.run(cmd, shell=True)

        self.send_response(200)
        self.send_header("Content-type", "audio/wav")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        with open(os.path.join(dir, output), 'rb') as file:
            self.wfile.write(file.read())

        os.remove(input)
        os.remove(output)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
