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
	print("b", file=sys.stderr)
	print(os.path.dirname(os.path.abspath(__file__)), file=sys.stderr)
	# sf, chicago, nyc, seattle, dc, denver, detroit = ('sanfrancisco' in request.args,
	# 										 'chicago' in request.args,
	# 										 'newyork' in request.args,
	# 										 'seattle' in request.args,
	# 										 'washingtondc' in request.args,
	# 										 'denver' in request.args,
	# 										 'detroit' in request.args)

	# cities = [sf, chicago, nyc, seattle, dc, denver, detroit]
	# city_names = ["sanfrancisco", "chicago", "newyork", 
	# 			  "seattle", "washingtondc", "denver",
	# 			  "detroit"]


	print(request.args.get('city'), file=sys.stderr)
	# available_cities = list(map(lambda x: x[1], filter(lambda x: x[0], zip(cities, city_names))))
	# print(available_cities, file=sys.stderr)

	# print (request.args, file=sys.stderr)
	if not skillset_query:
		results = []
	else:
		results = engine.fetch_postings(skillset_query, company_quality_query, request.args.get('city'))

	print (results, file=sys.stderr)
	return render_template('search.html', results=results)



