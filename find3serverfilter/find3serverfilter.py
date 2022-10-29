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
    filtered = dict(input_json)
    filtered_total = 0
    for source in dict(filtered['s']).keys():
      original_count = len(input_json['s'][source])
      filtered_count = 0
      for key, value in dict(filtered['s'][source]).items():
        if source in self.settings['allowlist']:
          if key not in self.settings['allowlist'][source]:
            del filtered['s'][source][key]
      filtered_count = len(filtered['s'][source])
      filtered_total += len(filtered['s'][source])
      removed_count = original_count - filtered_count
      print(
        "Filtering: {}: Starting entries: {}, Removed: {}, Forwarded: {}"
        .format(
          source,
          original_count,
          removed_count,
          filtered_count
        )
      )
    if filtered_total > 0:
      response = requests.post(self.settings['upstream_server']+'/passive', json=filtered)
      print(response.json())
