"""
Python wrapper to generate pandas DataFrames from the New York Times'
Campaign Finance API.

Information about the API, including how to obtain a key is available
here - http://developer.nytimes.com/docs/campaign_finance_api/

Written by Connor Laird
Released under the MIT license - http://opensource.org/licenses/MIT
"""

# Imports
import datetime
import urllib
import pandas as pd
try:
    import json
except ImportError:
    import simplejson as json


class PandasCampaignFinance():

    def __init__(self, api_key, version="v3"):
        self.api_key = api_key
        self.version = version

    # ----------------------------------------------------------------------
    # Candidate Queries
    # ----------------------------------------------------------------------

    """
    Performs a Candidate Search request. Searches for Congressional and
    presidential candidates by last name.
    @param last_name - Last name or partial last name for search
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def candidate_search(self, last_name, campaign_cycle):
        #  Build query parameters
        endpoint = "candidates/search.json"
        parameters = {"query": last_name, "api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        #  Extract needed information
        candidates = []
        for candidate in data['results']:
            meta_info = {"committee": candidate["committee"],
                         "state": candidate["state"],
                         "district": candidate["district"]}

            candidates.append(dict(meta_info.items()
                                   + candidate['candidate'].items()))

        return pd.DataFrame(candidates)

    """
    Retrieves the campaign finance details for a particular presidential
    or Congressional candidate
    @param fec_id - String: (P | H | S) + 9 digits
                    (P = President; H = House; S = Senate)
                    The FEC assigns a unique ID to each candidate
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def candidate_details(self, fec_id, campaign_cycle):
        #  Build query parameters
        endpoint = "candidates/" + str(fec_id) + ".json"
        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    """
    Retrieves the campaign finance details for a multiple presidential
    or Congressional candidate
    @param fec_ids - And array of fec_ids
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def multiple_candidate_details(self, fec_ids, campaign_cycle):
        #  Make multiple calls to candidate_details
        details = pd.DataFrame()

        for fec_id in fec_ids:
            #  Append the results
            details = details.append(self.candidate_details(fec_id,
                                                            campaign_cycle))
        return details

    # ----------------------------------------------------------------------
    # Presidential Campaigns Queries
    # ----------------------------------------------------------------------

    """
    Retrieve totals (receipts and disbursements) for all presidential
    candidates for a particular campaign cycle
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def presidential_totals(self, campaign_cycle):
        endpoint = "president/totals.json"
        parameters = {"api-key": self.api_key}

        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    """
    Retrieves campaign finance details for a particular presidential candidate
    @param candidate - Last name or FEC committee ID
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def presidential_details(self, candidate, campaign_cycle):
        #  Build query parameters
        endpoint = "president/candidates/" + str(candidate) + ".json"
        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    """
    Retrieves campaign finance details for a multiple presidential candidates
    @param candidates - array of candidate names or ids
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def multiple_presidential_details(self, candidates, campaign_cycle):
        #  Make multiple calls to presidential_details
        details = pd.DataFrame()

        for candidate in candidates:
            #  Append the results
            details = details.append(self.presidential_details(candidate,
                                                               campaign_cycle))
        return details

    """
    To retrieve totals (donations to all presidential candidates)
    for a particular location
    @param location - Two-letter state abbreviation (for the states
                      resource type) or five-digit ZIP code (for the zips
                      resource type)
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def presidential_location_totals(self, location, campaign_cycle):
        #  Build query parameters
        if len(location) == 2:
            endpoint = "president/states/" + str(location) + ".json"
        else:
            endpoint = "president/zips/" + str(location) + ".json"

        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    # ----------------------------------------------------------------------
    # Committee Queries
    # ----------------------------------------------------------------------

    """
    Search for a political committee by full or partial name
    @param name - The committee name or partial name
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def committee_search(self, name, campaign_cycle):
        #  Build query parameters
        endpoint = "committees/search.json"
        parameters = {"query": name, "api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        #  Extract needed information
        return pd.DataFrame(data['results'])

    """
    Get details about a committee by FEC ID
    @param fec-id - String: C + 9 digits
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def committee_details(self, fec_id, campaign_cycle):
        #  Build query parameters
        endpoint = "committees/" + str(fec_id) + ".json"
        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results']).drop('other_cycles', 1)

    """
    Get details about multiple committees by FEC IDs
    @param fec-ids - Array of Strings: C + 9 digits
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def multiple_committee_details(self, fec_ids, campaign_cycle):
        #  Make multiple calls to committee_details
        details = pd.DataFrame()

        for committee in fec_ids:
            #  Append the results
            details = details.append(self.committee_details(committee,
                                                            campaign_cycle))
        return details

    """
    Retrieve the 20 most recently added committees
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def new_committees(self, campaign_cycle):
        #  Build query parameters
        endpoint = "committees/new.json"
        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    """
    Retrieve all available data about a particular committee's
    contributions to candidates.
    @param fec_id - FEC id of committee
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    @param offset - [Optional] Sets the starting point of the result set
                    Integer, multiple of 20. Used in paging
    """
    def committee_contributions(self, fec_id, campaign_cycle, offset=0):
        #  Build query parameters
        endpoint = "committees/" + str(fec_id) + "/contributions.json"
        parameters = {"offset": offset, "api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    """
    Retrieve committee contributions to a particular candidate
    @param committee_id - FEC id of the committee
    @param candidate_id - FEC id of the candidate
    @param campaign_cycle - Even-numbered year or election
                            Presidential Data: 2008-present
                            Congressional data: 2000-present
    """
    def contributions_to_candidate(self,
                                   committee_id,
                                   candidate_id,
                                   campaign_cycle):
        #  Build query parameters
        endpoint = "committees/" + str(committee_id) + "/contributions/"
        endpoint += "candidates/" + str(candidate_id) + ".json"

        parameters = {"api-key": self.api_key}

        #  Make API Call
        data = self.api_request(campaign_cycle, endpoint, parameters)
        if data is False:
            print "Bad response: Returning empty DataFrame"
            return pd.DataFrame()

        return pd.DataFrame(data['results'])

    # ----------------------------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------------------------

    """
    Builds a request URI, makes the request and returns as JSON load
    """
    def api_request(self, campaign_cycle, endpoint, parameters):
        #  Biuld the request URI
        request_uri = "http://api.nytimes.com/svc/elections/us/"
        request_uri += self.version + "/finances/"
        request_uri += str(campaign_cycle) + "/" + endpoint + "?"
        for key, value in parameters.iteritems():
            request_uri += "&" + str(key) + "=" + str(value)

        #  Make the request, return in a JSON object
        request = urllib.urlopen(request_uri)
        response = request.read()

        #  Check for errors in the response
        try:
            self.check_api_error(response)
        except ValueError as e:
            print e
            return False

        return json.loads(response)

    """
    Checks the response for errors, raising exceptions as needed.
    """
    def check_api_error(self, response):
        #  Check for a bad API key
        if response == "<h1>Developer Inactive</h1>":
            raise ValueError('Bad API key')

        #  Check for other errors
        response = json.loads(response)
        if response['status'] == "ERROR":
            raise ValueError('API Error Response: %s' % (response['errors']))
