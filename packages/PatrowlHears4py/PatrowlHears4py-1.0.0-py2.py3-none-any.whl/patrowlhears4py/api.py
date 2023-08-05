import requests

from patrowlhears4py.exceptions import PatrowlHearsException


class PatrowlHearsApi:
    """Python API for PatrowlHears."""

    def __init__(self, url, auth_token, proxies={}, ssl_verify=False, timeout=10):
        """
        Initialize a PatrowlHearsApi object.

        :param url: PatrowlHears URL
        :param auth_token: The API key
        :param proxies: The HTTP/HTTPS proxy endpoints
        :param ssl_verify: SSL/TLS certificate verification
        :param timeout: Request timeout (in sec)
        """
        self.url = url
        self.rs = requests.Session()
        self.rs.headers['Authorization'] = 'Token {}'.format(auth_token)
        self.rs.proxies = proxies
        self.rs.verify = ssl_verify
        self.rs.timeout = timeout

    # Vulnerabilities
    def get_latest_vulns(self):
        """
        Get latest vulnerabilities.

        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/latest").json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve vuln: {}".format(e))

    def get_vulns_stats(self):
        """
        Get vulnerability statistics.

        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/stats").json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve vuln stats: {}".format(e))

    def get_vuln(self, vuln_id):
        """
        Get vulnerability info by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve vuln: {}".format(e))

    def get_vuln_exploits(self, vuln_id):
        """
        Get exploits related to a vulnerability by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}/exploits".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve vuln exploits: {}".format(e))

    def get_vuln_threats(self, vuln_id):
        """
        Get threats related to a vulnerability by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}/threats".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve vuln threats: {}".format(e))

    def get_vuln_history(self, vuln_id):
        """
        Get vulnerability changes history by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}/history".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to get vuln history: {}".format(e))

    def toggle_vuln_monitoring(self, vuln_id):
        """
        Toggle monitoring status of a vulnerability by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}/toggle".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to toggle vuln monitoring status: {}".format(e))

    def refresh_vuln_score(self, vuln_id):
        """
        Refresh vulnerability score by his ID.

        :param vuln_id: Vulnerability ID
        :rtype: json
        """
        try:
            return self.rs.get(self.url+"/api/vulns/{}/refresh_score".format(vuln_id)).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to refresh vuln score: {}".format(e))

    def get_data_info(self, since=None, to=None):
        """
        Get static data info.

        :param since: Search data from date (format: YYYY-MM-DD). Optional.
        :param to: Search data to date (format: YYYY-MM-DD). Optional.
        :rtype: json
        """

        url = self.url+"/api/data/export/info?"
        if since is not None:
            url = "{}&since={}".format(url, since)
        if to is not None:
            url = "{}&to={}".format(url, to)
        try:
            return self.rs.get(url).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve data info: {}".format(e))

    def export_data(self, since=None, to=None, limit=None):
        """
        Export static data.

        :param since: Search data from date (format: YYYY-MM-DD). Optional.
        :param to: Search data to date (format: YYYY-MM-DD). Optional.
        :param limit: Limit rows per table. Optional.
        :rtype: json
        """

        url = self.url+"/api/data/export/full?"
        if since is not None:
            url = "{}&since={}".format(url, since)
        if to is not None:
            url = "{}&to={}".format(url, to)
        if limit is not None:
            url = "{}&limit={}".format(url, limit)
        print(url)
        try:
            return self.rs.get(url).json()
        except requests.exceptions.RequestException as e:
            raise PatrowlHearsException("Unable to retrieve data: {}".format(e))
