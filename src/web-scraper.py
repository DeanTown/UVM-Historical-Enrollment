import argparse
from urllib.error import HTTPError
import urllib.request
import os
import ssl
import pandas as pd
import yaml

ssl._create_default_https_context = ssl._create_unverified_context


def parse_args():
    """
    Parse CLI options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="../config/default.json")
    parser.add_argument(
        "-y",
        "--years",
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
        self.raw_data_path = "../raw-data/"
        self.clean_data_path = "../clean-data/"
        self.url_base = "https://serval.uvm.edu/~rgweb/batch/enrollment/curr_enroll_"
        self.cfg = self.read_config(args)

        self.check_directory(self.raw_data_path)
        self.check_directory(self.clean_data_path)

    def run(self):
        self.scrape_data()
        self.clean_data()

    def scrape_data(self):
        years = [*range(self.year_start, self.year_end + 1)]
        dates = [
            str(year) + session for year in years for session in ["01", "06", "09"]
        ]
        for date in dates:
            url = f"{self.url_base}{date}.csv"
            try:
                response = urllib.request.urlopen(url)
                f = open(self.raw_data_path + date + ".csv", "w")
                for line in response:
                    line = line.decode("utf-8")
                    # check the line for fixes and apply if needed
                    for fix in self.cfg["fixes"]:
                        if fix in line:
                            line = line.replace(fix, self.cfg["fixes"][fix])
                    f.write(line)
                f.close()
                self.sessions.append(date)
            except HTTPError as e:
                print(f"While trying to scrape {url}, an error occured: {e}")

    def clean_data(self):
        # for each file in the sessions list, discard unwanted columns, and rename headers
        for session in self.sessions:
            self.clean_file(session)

    def clean_file(self, session):
        df = pd.read_csv(self.raw_data_path + session + ".csv")
        # strip column names of leading and trailing whitespace
        df = df.rename(columns={col: col.strip() for col in df.columns})
        # check if df contains `Instructor First` or `Instructor Last` for fixing
        if "Instructor First" in df.columns or "Instructor Last" in df.columns:
            df["Instructor"] = (
                df["Instructor First"].astype(str)
                + " "
                + df["Instructor Last"].astype(str)
            )
            df = df.drop(["Instructor First", "Instructor Last"], axis=1)
            # Reorder columns so that `Instructor` is the second to last column
            cols = df.columns.tolist()
            cols = cols[:-2] + [cols[-1]] + [cols[-2]]
            df = df[cols]
        # map column names
        mapped_columns = {
            col: self.cfg["col_mapping"].get(col, False) for col in df.columns
        }
        # rename headers
        df = df.rename(columns=mapped_columns)
        # determine which columns are being discarded
        for col in df.columns:
            if not self.cfg["cols"].get(col, False):
                df = df.drop(col, axis=1)
        # write to new file
        df.to_csv(self.clean_data_path + session + ".csv")

    def check_directory(self, path):
        does_exist = os.path.exists(path)
        if not does_exist:
            os.makedirs(path)

    @staticmethod
    def read_config(args):
        with open(args.config) as config_file:
            return yaml.safe_load(config_file)


if __name__ == "__main__":
    EnrollmentData(parse_args()).run()
