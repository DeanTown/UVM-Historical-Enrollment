import argparse
from urllib.error import HTTPError
import urllib.request
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
        nargs='+',
        required=True,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    scrape_data(args)


def scrape_data(args):
    # URL segment to fetch data from
    url_base = 'https://serval.uvm.edu/~rgweb/batch/enrollment/curr_enroll_'
    for year in range(args.years[0], args.years[1] + 1):
        for session in ['01', '06', '09']:
            date = str(year) + session + '.csv'
            url = url_base + date
            try:
                response = urllib.request.urlopen(url)
                f = open('../data/' + date, 'w')
                for line in response:
                    f.write(line.decode('utf-8'))
                f.close()
            except HTTPError as e:
                print(f"While trying to scrape {url}, an error occured:")
                print(e)


if __name__ == '__main__':
  main()
