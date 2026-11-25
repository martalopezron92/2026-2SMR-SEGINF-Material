#!/usr/bin/env python3
"""Servidor de login de prueba para la demo de sniffer (UD02).

Uso:
  python3 servidor_login.py            -> HTTP  en http://127.0.0.1:8080
  python3 servidor_login.py --https    -> HTTPS en https://127.0.0.1:8443
                                          (necesita cert.pem y key.pem en la misma carpeta)
Solo escucha en 127.0.0.1: no es accesible desde otros equipos.
"""
import html
import ssl
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

FORM = """<!doctype html><html lang="es"><meta charset="utf-8">
<title>Intranet Talleres Ribera</title>
<body style="font-family:sans-serif;max-width:360px;margin:60px auto">
<h2>Intranet Talleres Ribera</h2>
<form method="post" action="/login">
<p>Usuario<br><input name="usuario"></p>
<p>Contrase&ntilde;a<br><input name="password" type="password"></p>
<p><button>Entrar</button></p>
</form></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, html):
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(FORM)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        campos = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"))
        usuario = html.escape(campos.get("usuario", [""])[0])
        self._send(f"<!doctype html><meta charset='utf-8'><body style='font-family:sans-serif'>"
                   f"<h2>Bienvenido/a, {usuario}</h2><p>(Login de demostración: no se guarda nada.)</p>")


if __name__ == "__main__":
    https = "--https" in sys.argv
    port = 8443 if https else 8080
    srv = HTTPServer(("127.0.0.1", port), Handler)
    if https:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain("cert.pem", "key.pem")
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f"Escuchando en {'https' if https else 'http'}://127.0.0.1:{port}  (Ctrl+C para parar)")
    srv.serve_forever()
