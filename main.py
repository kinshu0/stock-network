import json

from core_modules.mongo_driver import mongo_connection as mongo_connection
'''
Establish connection with url and database name of mongoDB server
'''
with open('appconfig.json', 'r') as f:
    configuration = json.load(f)

mongo_connection(configuration['serverUrl'], configuration['dbName'])

import webapp.front_end.web_application

webapp.front_end.web_application.app.run_server(debug=bool(configuration['debug']), host='127.0.0.1', port=8080) # Keep the debug variable empty for false and anything else for true