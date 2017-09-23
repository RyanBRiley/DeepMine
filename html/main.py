import tornado.ioloop
import tornado.web
import sys 
sys.path.append('../')
from StatusEnum import Status

data = [
    "01-Jan-15 00:00:00",
    {
        "status":Status.Good,
        "pressure": [Status.Good, 3071],
        "feed": [Status.Good, 280],
        "level": [Status.Good, 69],
        "vent value position": [Status.Good, 66]
    }, 
    {
        "status":Status.Good,
        "pressure": [Status.Fail, 10],
        "feed": [Status.Good, 280],
        "level": [Status.Good, 69],
        "vent value position": [Status.Good, 66]
    }, 
    {
        "status":Status.Caution,
        "pressure": [Status.Caution, 2000],
        "feed": [Status.Good, 100],
        "level": [Status.Caution, 2],
        "vent value position": [Status.Good, 66]
    }, 
    {
        "status":Status.Fail,
        "pressure": [Status.Fail, 0],
        "feed": [Status.Fail,0],
        "level": [Status.Fail, 0],
        "vent value position": [Status.Good, 66]
    }
]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/sensors.html", Status=Status, date=data[0], autoclaves=data[1:])

class AutoclaveHandler(tornado.web.RequestHandler):
    def get(self, id):
        idx = int(id)
        self.render("templates/single.html", Status=Status, id=idx, ac=data[idx + 1]) # first index is date of update

def make_app(): 
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/autoclave/(\d{1})", AutoclaveHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {
            "path": "css"
        }),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
