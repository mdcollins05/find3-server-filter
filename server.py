import os
import cherrypy

from find3serverfilter.find3serverfilter import Find3ServerFilter

base_dir = os.path.dirname(os.path.realpath(__file__))

cherrypy.config.update(base_dir + '/server.conf')
cherrypy.config.update({
    'log.screen': True,
    })

cherrypy.tree.mount(Find3ServerFilter(base_dir + "/config/config.yml"), '/', base_dir + "/app.conf")
cherrypy.engine.autoreload.files.add('config/config.yml')

cherrypy.engine.start()
cherrypy.engine.block()
