
# Pandas Campaign Finance

Python wrapper to generate pandas DataFrames from the New York Times'
Campaign Finance API.

Information about the API, including how to obtain a key is available
here - http://developer.nytimes.com/docs/campaign\_finance\_api/


### Usage
The wrapper provides methods to match most of the endpoints in the Candidates, Committees and Presidential Campaigns categories. Take a look at the code to see the exact methods, the function level documentation should be clear about the necessary parameters. For example, to search for candidates named Jones in the 2016 cycle you would use the following:

	from PandasCampaignFinance import PandasCampaignFinance as PCF
	api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	
	api_wrapper = PCF(api_key)
	
	candidates = api_wrapper.candidate_search("Jones", 2016)
	

This would return a DataFrame containing basic information about each candidate in Congressional or presidential races in 2016 named Jones.

### Implemented Endpoints
The following have been implemented so far:

-	Candidates
	-	Candidate Search
	-	Candidate Details (With support for multiple candidates)
-	Committees
	-	Committee Search
	-	Committee Details (With support for multiple committees)
	-	New Committees
	-	Committee Contributions
	-	Committee Contributions to a Candidate
-	Presidential Campaigns
	-	Presidential Candidate Totals
	-	Presidential Candidate Details (With support for multiple candidates)
	-	Presidential State/ZIP Totals