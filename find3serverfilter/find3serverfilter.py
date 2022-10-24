import cherrypy
import os
import yaml
import json
import requests

class Find3ServerFilter():
  def __init__(self, config):
    self.settings = {}
    self.config = config

    if os.path.isfile(config):
      settingsFile = open(config)
      self.settings = yaml.safe_load(settingsFile)
      settingsFile.close()
    else:
      print("Couldn't open configuration file '{0}'".format(config))
      os.sys.exit()

  @cherrypy.expose
  def index(self):
    return "Hello world!"

  @cherrypy.expose
  @cherrypy.tools.json_in()
  def passive(self):
    input_json = cherrypy.request.json
    original_count = len(input_json['s']['wifi'])
    filtered = dict(input_json)
    for key, value in dict(filtered['s']['wifi']).items():
      if key not in self.settings['allowlist']:
        del filtered['s']['wifi'][key]
    filtered_count = len(filtered['s']['wifi'])
    removed_count = original_count - filtered_count
    print("Starting entries: {}, Removed: {}, Forwarded: {}".format(original_count, removed_count, filtered_count))
    if filtered_count > 0:
      response = requests.post(self.settings['upstream_server']+'/passive', json=filtered)
      print(response.json())

