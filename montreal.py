#!/usr/bin/env python2

import requests

class Destination:
    def __init__(self, html_line):
        #print html_line+'\n\n\n'
        self.city_from = ""
        self.city_to = ""
        self.price = ""
        self.link = ""

        self.parse(html_line)
        #print self.city_from
        #print self.city_to+' : '+self.price
        #print self.month

    def parse(self, html_line):

        # Airport of departure
        from_beg = html_line.find("class=\"dealtag\">")+len("class=\"dealtag\">")
        from_end = html_line[from_beg:].find("</div><div")+from_beg
        self.city_from = html_line[from_beg:from_end]
        if self.city_from[:3] == "de ":
            self.city_from = self.city_from[3:]
        #else:
        #    print list(self.city_to[:3])

        # Airport of destination
        dest_beg = html_line.find("class=\"deal_dest\"><h2>")+len("class=\"deal_dest\"><h2>")
        dest_end = html_line[dest_beg:].find("</h2></div>")+dest_beg
        city_month = html_line[dest_beg:dest_end]
        self.city_to = city_month.split('/')[0][:-1]

        # Month
        self.month = city_month.split('/')[1][1:]

        # Price of flight
        price_beg = html_line.find("class=\"deal_price\"><h2>")+len("class=\"deal_price\"><h2>")
        price_end = html_line.find("$</h2></div>")+1
        self.price = html_line[price_beg:price_end]

        # Link to possible dates
        link_beg = html_line.find("<a href=")+len("<a href=\"")
        link_end = html_line.find(".html")+len(".html")
        self.link = "https://flytrippers.com/"+html_line[link_beg:link_end]

def main():
    destinations = []
    r = requests.get('https://flytrippers.com/blocks/mtl_deals.html')
    if r.status_code == 200:
        for line in r.text.split('\n'):
            if "class=\"expired\"" not in line:
                destinations.append(Destination(line))
    else:
        print "Can't reach website"

    max_size_city = 0
    for x in destinations:
        if len(x.city_to) > max_size_city:
            max_size_city = len(x.city_to)
    destinations = sorted(destinations, key=lambda Destination: Destination.price)
    for dst in destinations:
        price_color = "\x1B[31m"
        price_int = int(dst.price[:-1])
        if price_int <= 100:
            price_color = "\x1B[32m"
        elif price_int <= 200:
            price_color = "\x1B[33m"
        print price_color+dst.price+" \x1B[0m"+dst.city_to+"\x1B[31m"+'\x20'*(max_size_city - len(dst.city_to))+" <--> \x1B[0m"+dst.city_from+"\x1B[0m"

if __name__ == "__main__":
    main()
