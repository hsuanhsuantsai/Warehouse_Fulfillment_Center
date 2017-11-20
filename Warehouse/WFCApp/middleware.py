class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path
        # print(path)
        res = path.split('/')
        # print(res)
        if len(res) >= 4 and res[2] == 'inventory' and request.method == 'GET':
        	response["Access-Control-Allow-Origin"] = "*"
        return response