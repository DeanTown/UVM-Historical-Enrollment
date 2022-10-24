import sys
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def parse_args():
    """
    Parse CLI options
    """
    return {
        'start': int(sys.argv[1]),
        'end': int(sys.argv[2]),
    }


def main():
    args = parse_args()
    scrape_data(args)


def scrape_data(args):
    # URL segment to fetch data from
    url_base = 'https://serval.uvm.edu/~rgweb/batch/enrollment/curr_enroll_'
    for year in range(args['start'], args['end'] + 1):
       for session in ['01', '06', '09']:
           url_end = str(year) + session + '.txt'
           url = url_base + url_end
           f = open('../data/' + url_end, 'w')
           response = urllib.request.urlopen(url)
           for line in response:
               f.write(line.decode('utf-8'))
           f.close()


if __name__ == '__main__':
  main()
