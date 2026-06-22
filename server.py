"""
橘猫女孩 AR 测试服务器
用法: python server.py
"""
import http.server
import ssl
import socket
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(DIR, 'server.pem')
PORT = 8080


def get_lan_ip():
    """获取真实局域网 IPv4"""
    # 192.168.3.9 是这台机器以太网的固定IP
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip.startswith(('192.168.', '10.', '172.16.')):
            return ip
    except:
        pass
    return '192.168.3.9'


def ensure_cert():
    if os.path.exists(CERT):
        return
    print('生成自签名证书...')
    from OpenSSL import crypto
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().CN = get_lan_ip()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    with open(CERT, 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    print('[OK] 证书已生成')


class Handler(http.server.SimpleHTTPRequestHandler):
    # MIME 类型扩展（MindAR 需要）
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.glb': 'model/gltf-binary',
        '.gltf': 'model/gltf+json',
        '.mind': 'application/octet-stream',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cross-Origin-Opener-Policy', 'unsafe-none')
        self.send_header('Cross-Origin-Embedder-Policy', 'unsafe-none')
        super().end_headers()

    def log_message(self, fmt, *args):
        if '/favicon' not in args[0]:
            print(f'  ← {args[0]}')


if __name__ == '__main__':
    os.chdir(DIR)
    ensure_cert()

    ip = get_lan_ip()

    # 启动服务器
    httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    print()
    print('=' * 60)
    print('  三潭印月 AR - MindAR 测试服务器')
    print('=' * 60)
    print()
    print('  AR 页面:')
    print(f'     https://{ip}:{PORT}')
    print()
    print('  使用说明:')
    print(f'     https://{ip}:{PORT}/README.txt')
    print()
    print('  浏览器提示不安全 -> 点[高级] -> [继续访问]')
    print('  Ctrl+C 停止')
    print('=' * 60)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
