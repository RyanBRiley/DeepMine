import tornado.ioloop
import tornado.web
import sys 
sys.path.append('../')
import StatusEnum
from threading import Lock 
from MineMonitor import MineMonitor


class MyDataStore:

    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = MyDataStore()
            return cls._instance

    def store_data(self, update_row, monitor):
        self.update_row = update_row
        self.monitor = monitor

    def get_data(self):
        return {'row':self.update_row, 'monitor':self.monitor}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        d = MyDataStore.instance().get_data()
        row_index = d['row']
        monitor = d['monitor']
        mydata = monitor.get_update(row_index)
        MyDataStore.instance().store_data(row_index + 1, monitor)
        self.render("templates/sensors.html", Status=StatusEnum.Status, show_other=False, date=mydata[0], autoclaves=mydata[1:])

class AutoclaveHandler(tornado.web.RequestHandler):
    def get(self, id):
        idx = int(id)
        d = MyDataStore.instance().get_data()
        row_index = d['row']
        monitor = d['monitor']
        mydata = monitor.get_update(row_index)
        self.render("templates/single.html", Status=StatusEnum.Status, show_other=True, id=idx, ac=mydata[idx + 1]) # first index is date of update

class AgitatorHandler(tornado.web.RequestHandler):
    def get(self, auto_id, agi_id):
        auto_idx = int(auto_id)
        d = MyDataStore.instance().get_data()
        row_index = d['row']
        monitor = d['monitor']
        mydata = monitor.get_update(row_index)
        self.render("templates/single_agi.html", Status=StatusEnum.Status, id=agi_id, agi=mydata[auto_idx + 1][agi_id]) # first index is date of update

def make_app(): 
    monitor = MineMonitor('../data')
    monitor.learn_stats()
    MyDataStore.instance().store_data(1, monitor)
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/autoclave/(\d{1})", AutoclaveHandler),
        (r"/autoclave/(\d{1})/agitator/([A-G])", AgitatorHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {
            "path": "css"
        }),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
