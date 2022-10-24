import mysql.connector
import urllib.request
# URL segement to fetch data from
url_base = "https://serval.uvm.edu/~rgweb/batch/enrollment/curr_enroll_"

def main():
    scrape_data()
    db_connect()


def scrape_data():
    for i in range(1995, 2021):
       for j in [1, 6, 9]:
           url_end = str(i) + "0" + str(j) + ".txt"
           url = url_base + url_end
           f = open("../data/" + url_end, 'w')
           response = urllib.request.urlopen(url)
           for line in response:
               f.write(line.decode('utf-8'))
           f.close()


def db_connect():
    mydb = mysql.connector.connect(
    	host="webdb.uvm.edu",
    	user="oreckord_reader",
    	password="hfDC3mIJGXkG"
    )
    print(mydb)
    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    for x in cursor:
    	print(x)


if __name__== "__main__":
  main()
