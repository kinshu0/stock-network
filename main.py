from core_modules.mongo_driver import mongo_connection as mongo_connection
'''
Establish connection with url and database name of mongoDB server
'''
mongo_connection('mongodb://localhost:27017/', 'dev3')

import webapp.front_end.web_application

webapp.front_end.web_application.app.run_server(debug=True)