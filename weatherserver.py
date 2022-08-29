import http.server
import socketserver
import json

port=10001
class Handler(http.server.BaseHTTPRequestHandler):
    print('inside handler')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        with open("data.json", "r") as f:
            self.send_response(200)
            self.end_headers()
            path = self.translate_path(self.path)
            path_split = [p for p in self.path.split('/')]
            params = path_split[1]
            city_name = params.lstrip('?city_name=')
            data = json.loads(f.read())
            self.wfile.write(str((data[city_name])).encode('utf-8'))

    def do_POST(self):
        path = self.translate_path(self.path)
        path_split = [p for p in self.path.split('/')]
        params = path_split[1]
        params = params.split('&')
        city_name = params[0].lstrip('?city_name=')
        temp = params[1].lstrip('temp=')
        lat = params[2].lstrip('lat=')
        long = params[3].lstrip('long=')
        new_data = {"coord": {"lon": long, "lat": lat}, "temp": temp}
        # try:
        #     with open('data.json') as file:
        #         data = json.loads(file.read())
        #     data[city_name] = new_data
        # except Exception:
        #     print("json.loads")
        # try:
        #     with open('data.json', 'w') as file:
        #         data = json.dumps(data, file)
        #         print(data)
        #         print(type(data))
        #         self.wfile.write(data.encode('utf-8'))
        # except Exception:
        #     print('json.dumps')

        # with open('data.json', 'r+') as file:
        #     # First we load existing data into a dict.
        #     # file_data = json.load(file)
        #     file_data[city_name] = new_data
        #     json.dump(file_data, file)
        data = None
        try:

            with open("data.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data[city_name] = new_data

            with open("data.json", "w") as jsonFile:
                json.dump(data, jsonFile)

            with open("data.json", "r") as jsonFile:
                self.wfile(str(data).encode('utf-8'))

            # with open('data.json', "r+") as file:
            #     data = json.load(file)
            #     print(type(data))
            #     print(data, "before")
            #     # data[city_name] = new_data
            #     # print(data, 'before dumping')
            #     # data = json.dumps(data)
            #     # print(data, 'after dumping')
            #     # print(type(data))
            #     # data.update({city_name:new_data})
            #     # json.dump(data, file)
            #     # file.truncate()


            print('post wfile')
        except Exception as e:
            print(e)
            print("inside exception")
        # 2. Update json object


        # 3. Write json file

        #try:
            #with open('data.json', "w") as file:
                #json.dump(data, file)
            #self.wfile.write(data.encode('utf-8'))
        #except Exception as e:
            #print(e)
            #print("dump")
            #print(data)
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)

    def translate_path(self, path):
        pass

with socketserver.TCPServer(("", port), Handler) as httpd:
    print("serving at port", port)
    httpd.serve_forever()