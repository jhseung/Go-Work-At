from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sys, os

project_name = "Go Work At"
net_id = "Ji Hwan Seung: js2687; Ju Un Park: jp848; Yong Jin Cho: yc628; Sang Won Yoon: sy623"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	# print("b", file=sys.stderr)
	# print(os.path.dirname(os.path.abspath(__file__)), file=sys.stderr)
	if not query:
		data = []
		output_message = ''
	else:
		engine.fetch_postings(query)
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



