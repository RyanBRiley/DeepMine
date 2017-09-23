import tornado.ioloop
import tornado.web
import enum

class Status(enum.Enum):
    Good = 1
    Error = 2
    Fail = 3

data = [
    {
        "status":Status.Good,
        "pressure_status": Status.Good,
        "pressure": 3071,
        "feed_status": Status.Good,
        "feed": 280,
        "level_status": Status.Good,
        "level": 69
    }, 
    {
        "status":Status.Good,
        "pressure_status": Status.Fail,
        "pressure": 10,
        "feed_status": Status.Good,
        "feed": 280,
        "level_status": Status.Good,
        "level": 69
    }, 
    {
        "status":Status.Error,
        "pressure_status": Status.Error,
        "pressure": 2000,
        "feed_status": Status.Good,
        "feed": 100,
        "level_status": Status.Error,
        "level": 2
    }, 
    {
        "status":Status.Fail,
        "pressure_status": Status.Fail,
        "pressure": 0,
        "feed_status": Status.Fail,
        "feed": 0,
        "level_status": Status.Fail,
        "level": 0
    }
]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/sensors.html", Status=Status, autoclaves=data)

class AutoclaveHandler(tornado.web.RequestHandler):
    def get(self, id):
        idx = int(id)
        self.render("templates/single.html", Status=Status, autoclaves=data, id=idx, ac=data[idx])

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
