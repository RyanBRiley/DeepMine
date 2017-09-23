import tornado.ioloop
import tornado.web
import enum

class Status(enum.Enum):
    Good = 1
    Error = 2
    Fail = 3


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/sensors.html", Status=Status,
            autoclaves=[
                {
                    "status":Status.Good,
                    "pressure_status": Status.Good,
                    "pressure": 3071,
                    "feed_status": Status.Good,
                    "feed": 280 
                }, 
                {
                    "status":Status.Good,
                    "pressure_status": Status.Fail,
                    "pressure": 10,
                    "feed_status": Status.Good,
                    "feed": 280 
                }, 
                {
                    "status":Status.Error,
                    "pressure_status": Status.Error,
                    "pressure": 2000,
                    "feed_status": Status.Good,
                    "feed": 100 
                }, 
                {
                    "status":Status.Fail,
                    "pressure_status": Status.Fail,
                    "pressure": 0,
                    "feed_status": Status.Fail,
                    "feed": 0 
                }
            ])

def make_app(): 
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {
            "path": "css"
        }),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
