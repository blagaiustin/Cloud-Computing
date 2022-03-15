import http.server
import socketserver
from bson import json_util
from database import db_client


class HttpServer(http.server.SimpleHTTPRequestHandler):

    def get_query_components(self):
        query_components = self.path.split("/")
        while '' in query_components:
            query_components.remove('')
        return query_components

    def do_GET(self):
        query_components = self.get_query_components()
        print(query_components)
        if query_components[0] not in db_client.list_collection_names():
            self.send_response(404, "Collection not found")
            self.end_headers()
        else:
            collection = db_client.get_collection(query_components[0])
            if len(query_components) % 2 == 0:
                query = {'id': int(query_components[1])}
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.end_headers()
                json_data = str([json_util.dumps(res) for res in collection.find(query)])
                self.wfile.write(json_data.encode())
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.end_headers()
                json_data = str([json_util.dumps(res) for res in collection.find()])
                self.wfile.write(json_data.encode())

    def do_POST(self):
        query_components = self.get_query_components()
        if len(query_components) == 1:
            self.send_response(201, "Collection created")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            collection = db_client.create_collection(query_components[0])
            query = {'id': len(collection.count_documents() + 1)}
            collection.insert_one(query)
            json_data = str([json_util.dumps(res) for res in collection.find(query)])
            self.wfile.write(json_data.encode())
        else:
            collection = db_client.get_collection(query_components[0])
            query = {'id': int(query_components[1]), query_components[2]: query_components[3]}
            if collection.find_one(query):
                self.send_response(409, "Resource already exists")
                self.end_headers()
            else:
                collection.insert_one(query)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                json_data = str([json_util.dumps(res) for res in collection.find(query)])
                self.wfile.write(json_data.encode())

    def do_DELETE(self):
        query_components = self.get_query_components()
        if len(query_components) == 1:
            self.send_response(405, "Method not allowed")
            self.end_headers()
        else:
            collection = db_client.get_collection(query_components[0])
            query = {"id": int(query_components[1])}
            if not collection.find_one(query):
                self.send_response(404, "Resource not found")
                self.end_headers()
            else:
                self.send_response(200,"Resource found")
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                collection.delete_one(query)
                json_data = str([json_util.dumps(res) for res in collection.find()])
                self.wfile.write(json_data.encode())

    def do_PUT(self):
        query_components = self.get_query_components()
        if len(query_components) == 1:
            self.send_response(405, "Method not allowed")
            self.end_headers()
        else:
            collection = db_client.get_collection(query_components[0])
            query = {'id': int(query_components[1])}
            print(query)
            if collection.find_one(query):
                if len(query_components) == 4:
                    query_update = {query_components[2]: query_components[3]}
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    collection.update_many(query, {"$set": query_update})
                    json_data = str([json_util.dumps(res) for res in collection.find()])
                    self.wfile.write(json_data.encode())
                else:
                    self.send_response(204)
                    self.end_headers()
                    query = {query_components[2]: None}
                    collection.update(query)
                    json_data = str([json_util.dumps(res) for res in collection.find()])
                    self.wfile.write(json_data.encode())
            else:
                self.send_response(404, "Resource not found")
                self.end_headers()


if __name__ == '__main__':
    handler = HttpServer
    server = socketserver.TCPServer(("127.0.0.1", 3000), handler)
    print("Running at: 127.0.0.1/3000")
    server.serve_forever()