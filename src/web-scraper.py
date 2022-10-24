import argparse
from urllib.error import HTTPError
import urllib.request
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def parse_args():
    """
    Parse CLI options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-y',
        '--years',
        type=int,
        nargs=2,
        required=True,
    )
    return parser.parse_args()


class EnrollmentData:
    def __init__(self, args):
        self.sessions = []
        self.year_start = args.years[0]
        self.year_end = args.years[1]
        self.data_path = '../data/'
        self.url_base = 'https://serval.uvm.edu/~rgweb/batch/enrollment/curr_enroll_'

        does_exist = os.path.exists(self.data_path)
        if not does_exist:
            os.makedirs(self.data_path)

    def run(self):
        self.scrape_data()
        print(self.sessions)

    def scrape_data(self):
        for year in range(self.year_start, self.year_end + 1):
            for session in ['01', '06', '09']:
                date = str(year) + session
                url = self.url_base + date  + '.csv'
                try:
                    response = urllib.request.urlopen(url)
                    f = open('../data/' + date + '.csv', 'w')
                    for line in response:
                        f.write(line.decode('utf-8'))
                    f.close()
                    self.sessions.append(date)
                except HTTPError as e:
                    print(f"While trying to scrape {url}, an error occured:")
                    print(e)


if __name__ == '__main__':
    EnrollmentData(parse_args()).run()
