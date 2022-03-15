import http.server
import socketserver
from http import HTTPStatus
import json
import xmltodict
from urllib.parse import urlparse


def parse_xml():
    with open("resources.xml") as file:
        data = file.read()
    return xmltodict.parse(data)


class HttpServer(http.server.SimpleHTTPRequestHandler):

    # q = parse_qs(parsed_url.query)

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path, allow_fragments=True)
        json_data = parse_xml()
        print(json_data)
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(parse_xml(), indent=4, sort_keys=True).encode())
        else:
            response, result = self.get_collection()
            if response != "":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=4, sort_keys=True).encode())
            else:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

    def do_POST(self):
        return None

    def do_DELETE(self):
        return None

    def do_PUT(self):
        return None

    def do_PATCH(self):
        return None

    def get_collection(self):
        json_data = parse_xml()
        path_split = self.path.split('/')
        path_split.remove('')

        data = json_data
        result = ""
        for index in range(0, len(path_split)): #[employees, employee]
            if path_split[index] in data.keys():
                result = data[path_split[index]]
                data = data[path_split[index]]
            else:
                return ""
        return result


if __name__ == '__main__':
    handler = HttpServer
    server = socketserver.TCPServer(("127.0.0.1", 3000), handler)
    print("Running at: 127.0.0.1:3000")
    server.serve_forever()