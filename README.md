# **Project: Logs Analysis**
This project is a simple script that analyzes mock news data, including Articles, Authors, and Logs, in a PostgreSQL database.

## **Getting Started**

### **How to use?**
The following functions will write data to a file titled `log_results.txt`. If the file already exists, the results will be appended to the end of the file.
* `pop_authors()` - returns the top 3 most popular articles of all time (by page views)
* `pop_articles()` - returns the most popular articles authors of all time (by page views)
* `req_errors()` - returns the day(s) on which more than 1% of requests lead to errors

Running the script directly will call all three functions above. You can use `from newsdata import *` to run the functions individually.

**Database Views:**
No views were created for this project.