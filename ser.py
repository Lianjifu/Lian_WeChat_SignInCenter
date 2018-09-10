#!/usr/bin/python
# encoding=utf-8

from urls import urlpatterns
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import config


class Application(tornado.web.Application):
    def __init__(self,*args, **kwargs):
        base_dir = os.path.dirname(__file__)
        settings = dict(
            template_path=os.path.join(base_dir, "template"),
            static_path=os.path.join(base_dir, "static"),
            # cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
            # xsrf_cookies=True,
            debug=True
        )
        super(Application, self).__init__(urlpatterns, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port=config.ser_port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()