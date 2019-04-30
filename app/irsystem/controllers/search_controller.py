from . import *
from app import app
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sys, os, json

project_name = "Go Work At"
net_id = "Ji Hwan Seung: js2687; Ju Un Park: jp848; Yong Jin Cho: yc628; Sang Won Yoon: sy623"

@irsystem.route('/', methods=['GET'])
def search():
	skillset_query = request.args.get('skillset')
	company_quality_query = request.args.get('company_quality')

	with open(os.path.join(app.root_path, "./backend/scraper/url_dict.json")) as f:
		company_to_review_url = json.load(f)

	with open(os.path.join(app.root_path, "./backend/keywords.json")) as f:
		company_to_keyword = json.load(f)

	print ("skillset query is: {}".format(skillset_query))
	print ("company_quality is: {}".format(company_quality_query))
	# print (request.args, file=sys.stderr)
	if not skillset_query:
		results = []
	else:
		results = engine.fetch_postings(skillset_query, company_quality_query, request.args.get('city'))

	for result in results:
		print (result['company_name'])
		if result['company_name'] == 'accenture':
			print ("PRINTING")
	print (company_to_review_url, file=sys.stderr)
	print (company_to_keyword, file=sys.stderr)

	return render_template('search.html', 
						   results=results, 
						   company_to_review_url=company_to_review_url,
						   company_to_keyword=company_to_keyword
						   )



