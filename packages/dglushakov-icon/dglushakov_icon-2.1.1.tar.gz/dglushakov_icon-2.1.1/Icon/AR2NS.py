import requests
import datetime
import xml.etree.ElementTree as ET


class AR2NS:
    def __init__(self, ip='127.0.0.1', login='admin', password='admin'):
        self.ip = ip
        self.login = login
        self.password = password

    def make_request(self, url):
        url = 'http://' + self.ip + '/' + url
        r = requests.get(url, auth=(self.login, self.password))
        return r

    def get_records_list(self, date_from=None, date_to=None):
        today = datetime.date.today()
        yesterday = (datetime.date.today() + datetime.timedelta(days=-1))
        if date_from is None:
            date_from = today
        if date_to is None:
            date_to = yesterday

        # http://10.77.197.207/records.xml?save=0&from=20200727&to=20200729
        url = 'records.xml?save=0&from=' + date_from.strftime('%Y%m%d') + '&to=' + date_to.strftime('%Y%m%d')
        records_request = self.make_request(url)

        records_list = []
        root = ET.fromstring(records_request.content)
        for child in root:
            record = {'ul': int(child.attrib['ul']), 'file': child.text}
            records_list.append(record)
        return records_list

    def get_settings(self):
        settings_request = self.make_request('settings.xml')

        settings = []
        root = ET.fromstring(settings_request.content)
        for child in root:
            setting = {child.tag: child.text}
            settings.append(setting)
        return settings


if __name__ == "__main__":
    device = AR2NS('192.168.0.100')
    settings = device.get_settings()
    for setting in settings:
        print(setting)
    # date_from = datetime.datetime.strptime('Jul 28 2020', '%b %d %Y')
    # date_to = datetime.datetime.strptime('Jul 29 2020', '%b %d %Y')
    # records = device.get_records_list(date_from, date_to)
    #
    # for record in records:
    #     print(record)
    #     if record['ul'] == 0:
    #         print('alert')
    #