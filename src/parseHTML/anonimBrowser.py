import mechanize, http.cookiejar, random, time


class anonimBrowser(mechanize.Browser):
    def __init__(self, proxies=[], useragents=[]):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.proxies = proxies
        self.user_agents = useragents+['Mozilla/4.0', 'FireFox/6.01', 'ExactSearch', 'Nokia7110/1.0']
        self.change_user_agent()
        self.set_cookiejar(http.cookiejar.LWPCookieJar())
        self.change_proxy()

    def clear_cookies(self):
        self.set_cookiejar(http.cookiejar.LWPCookieJar())

    def change_user_agent(self):
        index = random.randrange(0, len(self.user_agents))
        self.addheaders = [('User-agent', self.user_agents[index])]

    def change_proxy(self):
        if self.proxies:
            index = random.randrange(0, len(self.proxies))
            self.set_proxies(self.proxies[index])

    def anonymize(self, sleep=False):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()
        if sleep:
            time.sleep(60);
