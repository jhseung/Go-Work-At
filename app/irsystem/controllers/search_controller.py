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

	if not skillset_query and not company_quality_query:
		return render_template('search.html', 
							results="home", 
							company_to_review_url=company_to_review_url,
							company_to_keyword=company_to_keyword
							)

	city_query = request.args.get('city') if request.args.get('city') else "sanfrancisco"

	results = engine.fetch_postings(skillset_query, company_quality_query, city_query)

	# print("skillset_query: {}".format(skillset_query), file=sys.stderr)

	skillset_lst = postings.skill_tokens(min_df=3)

	skillset_dict = dict(enumerate(skillset_lst))
	print(request.form, file=sys.stderr)
	print(request.data, file=sys.stderr)
	print(request.values, file=sys.stderr)
	# print(request.form, file=sys.stderr)

	return render_template('search.html', 
						   results=results, 
						   company_to_review_url=company_to_review_url,
						   company_to_keyword=company_to_keyword
						   )



