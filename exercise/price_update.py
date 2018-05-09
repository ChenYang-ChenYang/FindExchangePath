import fileinput
from datetime import datetime
import sys, os
import re

"""
author: Chen Yang
email: garychenyang@gmail.com
"""

price_file_path = "./latest_price.txt"

def update_price(timestamp, exchange, source_currency, dest_currency, forward_factor, backward_factor):
    """update latest price to a file
    
    Arguments:
    timestamp -- timestamp of the price
    exchange -- exchange name
    source_currency -- source currency
    dest_currency -- destination currency
    forword_factor -- forward factor
    backward_factor -- backward factor
    """
    # flag if exchange with currency exists or not in system
    is_exchange_currency_found = False
    # new price info
    new_line = timestamp+" "+exchange+" "+source_currency+" "+dest_currency+" "+forward_factor+" "+backward_factor
    
    # create a new file and add price info if file doesn't exist
    if not os.path.exists(price_file_path):
        with open(price_file_path, "a") as file:
            file.write(new_line+"\n")
            
    else:
        # loop exist price list in files
        for line in fileinput.input(price_file_path, inplace=True):
            # check if the same exchange, source currency, destination currency exist 
            price_str = re.search(r'(\d{4}-\d{2}-\d{2}.*?)\s'+exchange+'\s'+source_currency+'\s'+dest_currency+'\s(.*?)\s(.*)', line)
            # exist
            if price_str is not None:
                is_exchange_currency_found = True
                timestamp_old = price_str.group(1)
                # timestamp is newer than existing one, update the price, or keep the existing one
                if(is_newer_time(timestamp_old, timestamp)):
                    sys.stdout.write(new_line+"\n")
                else:
                    sys.stdout.write(line)
            else:
                # keep existing price if current line doesn't match
                sys.stdout.write(line)
        fileinput.close()
        
        # append price info if it is new exchange, source currency, destination currency         
        if not is_exchange_currency_found:
            with open(price_file_path, "a") as file:
                file.write(new_line+"\n")

# compare if a timestamp is newer than another one. It is used when updating price info.                    
def is_newer_time(exist_time_str, new_time_str):
    exist_till_seconds = exist_time_str.split("+")[0]
    new_till_seconds = new_time_str.split("+")[0]
    exist_time = datetime.strptime(exist_till_seconds, "%Y-%m-%dT%H:%M:%S")
    new_time = datetime.strptime(new_till_seconds, "%Y-%m-%dT%H:%M:%S")
    if(new_time > exist_time):
        return True
    else:
        return False