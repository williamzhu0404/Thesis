import requests

# converting year in Republican Calendar to that in Gregorian Calendar
def roc_greg(year, roc = True):
	ROC_0 = 1911
	return year + ROC_0 if roc else year - ROC_0

ENDPOINT = "https://www.ly.gov.tw/WebAPI/{}.aspx"
dept_dict = {
	"budget": "BudgetCenterResearch",
	"legal": "LawBureauResearch",
	"bill": "LegislativeBill",
	"speech": "LegislativeSpeech"
}

def dept_endpoint(dept):
	return ENDPOINT.format(dept_dict[dept])


def payload(begin, end, mode, **kwargs):
	req_params = {
	"from": begin,
	"to": end,
	"mode": mode
	}
	for key, val in kwargs.items():
		req_params[key] = val
	return req_params

r = requests.get( dept_endpoint("bill") , params=payload("0811219", "1111231", "csv" ) )
#r = requests.get( dept_endpoint("bill") , params=payload("0811219", "1111231", "json" ) )

f = open("bill_proposal.json", "w")
f.write(r.text)
f.close()
