from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sys, os

project_name = "Go Work At"
net_id = "Ji Hwan Seung: js2687; Ju Un Park: jp848; Yong Jin Cho: yc628; Sang Won Yoon: sy623"

@irsystem.route('/', methods=['GET'])
def search():
	skillset_query = request.args.get('skillset')
	company_quality_query = request.args.get('company_quality')
	# print("b", file=sys.stderr)
	# print(os.path.dirname(os.path.abspath(__file__)), file=sys.stderr)
	if not skillset_query:
		results = []
	else:
		results = engine.fetch_postings(skillset_query, company_quality_query)
		output_message = "Companies"
		print (results, file=sys.stderr)
		
	return render_template('search.html', results=results)



