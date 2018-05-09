import re
import logging
import sys
from exercise.price_update import update_price
from exercise.graph_generate_search import generate_graph, find_exchange_path

"""
author: Chen Yang
email: garychenyang@gmail.com
"""

logging.basicConfig(
    format="%(asctime)s [%(name)s] [%(levelname)s]  %(message)s",
    level = "DEBUG",
    handlers=[
        logging.FileHandler(".//exercise.log"),
        logging.StreamHandler(sys.stdout)
    ])

if __name__ == "__main__":
    # variable to save graph
    exchange_graph = None
    # regular expression for price string
    price_re = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*?)\s(.*?)\s(.*?)\s(.*?)\s(.*?)\s(.*)'
    # regular expression for exchange request string
    exchange_request_re = r'EXCHANGE_RATE_REQUEST\s(.*?)\s(.*?)\s(.*?)\s(.*)'
    
    # loop to process each standard input until entering "exit"
    while True:
        # accept standard input
        stin=input("please pass your standard input:")
        
        if(stin == "exit"):
            logging.info("exit processor now!") 
            break
        
        # check if standard input is price update 
        price_check = re.search(price_re, stin)
        if price_check is not None:
            # get all content from the price update string
            timestamp = price_check.group(1)
            exchange = price_check.group(2)
            source_currency = price_check.group(3)
            dest_currency = price_check.group(4)
            forward_factor = price_check.group(5)
            backward_factor = price_check.group(6)
            logging.info("get price updating request: " + stin)
            update_price(timestamp, exchange, source_currency, dest_currency, forward_factor, backward_factor)
            
            # generate rate graph when price is updated
            vertex_list, exchange_graph = generate_graph()
            logging.info("price was updated and the latest exchange rate graph is:\n" + str(exchange_graph))
        else:
            # check if standard input is exchange path request
            request_check = re.search(exchange_request_re, stin)
            if request_check is not None:
                # get all content from the exchange path request
                source_exchange = request_check.group(1)
                source_currency = request_check.group(2)
                dest_exchange = request_check.group(3)
                dest_currency = request_check.group(4)
                logging.info("get exchange rate request: " + stin)
                # generate graph if it was not created before 
                if exchange_graph is None:
                    try:
                        vertex_list, exchange_graph = generate_graph()
                    except ValueError as err:
                        logging.error(err)
                        continue
                    logging.info("the latest exchange rate graph is:\n" + str(exchange_graph))
                
                # check if source and destination are valid
                source_vertex = source_exchange+"_"+source_currency
                dest_vertex = dest_exchange+"_"+dest_currency
                if (source_vertex not in vertex_list) or (dest_vertex not in vertex_list): 
                    logging.info("The source or destination exchange&currency is invalid, please check to update and re-run again.")
                    continue
                
                # call method to find exchange path
                path, rate = find_exchange_path(vertex_list, exchange_graph, source_exchange, source_currency, dest_exchange, dest_currency)
                
                # construct the exchange path output
                if len(path) > 0:
                    # get exchange rate result from rate matrix by vertex indexes
                    final_rate = str(rate[vertex_list.index(source_exchange+"_"+source_currency)][vertex_list.index(dest_exchange+"_"+dest_currency)])
                    result = "\n" \
                            "BEST_RATES_BEGIN\n" \
                            +source_exchange + " " + source_currency + " " + dest_exchange + " " + dest_currency + " " + final_rate +"\n"
                    for index in path:
                        # split the vertex <exchange>_<currency> to exchange and currency 
                        exchange_currency = vertex_list[index].split("_")
                        result +=  exchange_currency[0] + "," + exchange_currency[1] + "\n"
                        
                    result += "BEST_RATES_END"    
                    logging.info("The exchange result is: " + result)
                else:
                    logging.info("Some price was set unreasonably, please check to update and re-run again.")
            else:    
                logging.info("Input is not a price update string nor exchange rate request string, please pass correct format string.")
