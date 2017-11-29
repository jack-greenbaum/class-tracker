import time
import subprocess
import argparse
import urllib.request
from bs4 import BeautifulSoup

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

parser = argparse.ArgumentParser(description=('Track open spots remaining from LSA Course Guide.'))
parser.add_argument('initial', metavar='initial', type=int,
                   help = 'an integer for the starting open slots.')
parser.add_argument('class_num', metavar='class_num', type=str, help='class number')

def main(previous, class_num):
    url = 'https://www.lsa.umich.edu/cg/cg_detail.aspx?content=2170EECS' + class_num + '001&termArray=w_18_2170'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    html_items = soup.find_all('div', attrs={'class': 'col-md-1'})

    remaining = int(html_items[10].text.strip().replace(' ',  '').split('\n')[1])

    if remaining < previous:
        applescript = """
        display dialog "EECS %s: %s" ¬
        with title "Class Tracker" ¬
        buttons {"OK"}
        """ % (class_num, str(remaining))
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
        time.sleep(5)
        main(remaining, class_num)
    else:
        time.sleep(5)
        main(previous, class_num)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.initial, args.class_num)
