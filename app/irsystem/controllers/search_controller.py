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

	print ("skillset query is: {}".format(skillset_query))
	print ("company_quality is: {}".format(company_quality_query))
	# print (request.args, file=sys.stderr)
	results = engine.fetch_postings(skillset_query, company_quality_query, request.args.get('city'))

	for result in results:
		print (result['company_name'])
		if result['company_name'] == 'accenture':
			print ("PRINTING")
	# print (results, file=sys.stderr)
	skillset_lst = postings.skill_tokens(min_df=3)

	skillset_dict = dict(enumerate(skillset_lst))
	print(skillset_dict)

	return render_template('search.html', results=results, skillset_dict=skillset_dict)



