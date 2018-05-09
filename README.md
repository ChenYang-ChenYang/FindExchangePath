# Description
Update exchange price and find best exchange rate path by request.

# Prerequisites
1. Install Python 3.5 or above
2. Make sure numpy is installed in the Python environment. 

# Verified Platforms
All the test cases in test report were verified on both Linux and Windows platforms.

# How to use
1. Copy the whole exercise folder to your machine where you intend to run.
2. Locate to the folder where the exercise folder is saved.
3. Run "python -m exercise.processor"
4. Pass all your price updating strings as standard input. The program will save all latest price to a file and generate a rate graph in memory.
5. Pass exchange rate request string as standard input. The program will output the best rate following the required format.
6. You can repeat step 4 or 5 continuously.

# Highlights 
1. One interface to process both price updating and exchange rate request. The program can distinguish by request format. 
2. Save price in text file and update with the latest price. This will avoid data lost when system crashes or restart. The price will be updated only when the timestamp is newer.
3. Generate new graph if price is updated. The graph will be saved in memory and no need to regenerated when processing exchange request, which will have better performance.
4. Create "price updating", "graph generation and search", "main processor" in 3 scripts separately, to keep a very clear structure.
5. Use logging module to save logs in both files and stdout. It is easy to track in production environment. 
6. Very details comments for code. 

# Negative test cases:
1. Timestamp format in price update request is invalid. The program can detect and log.  
2. The whole price update request format is invalid. The program can detect and log. 
3. Request exchange rate path but there is no any price information. The program can detect and log.
4. The exchange rate request format is invalid. The program can detect and log. 
5. The source or destination exchange or currency doesn't exist. The program can detect and log. 
6. Some price value is set unreasonably so the exchange rate path will loop infinitely. The program can detect and log. 

# Test report
Please refer to Test_Report.docx for all positive and negative test cases and result.
