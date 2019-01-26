# **Project: Logs Analysis**
This project is a simple script that analyzes mock news data, including Articles, Authors, and Logs, in a PostgreSQL database.

## **Getting Started**

### **Requirements**
* [Python 2.7.15](https://www.python.org/downloads/release/python-2715/ "Python 2 Download")
* [PostgreSQL](https://www.postgresql.org/download/ "PostgreSQL Download")
* [psycopg2](http://initd.org/psycopg/download/ "psycopg2 Download")
* [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 "VirtualBox Download")
* [Vagrant](https://www.vagrantup.com/downloads.html "Vagrant Download")

### **Installing**
This project utilizes a virtual machine (VM) to run the SQL database server. To get setup:

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 "VirtualBox Download").

2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html "Vagrant Download").

3. Download the VM Configuration by using one of the following methods:
    * Download and unzip the [VM Configuration File](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip "VM Configuration Download") to create a directory titled FSND-Virtual-Machine
    * Use GitHub to fork and clone this repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm "GitHub Repository")

To begin working with this project, fork and clone this repository in the _vagrant_ subdirectory of the VM Configuration directory, and download the [newsdata.sql file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip "newsdata.sql Download")

In your terminal, change to the _vagrant_ subdirectory
```
cd /FSND-Virtual-Machine/vagrant/
  -- OR --
cd /fullstack-nanodegree-vm/vagrant/
```

While inside the vagrant subdirectory, run the command `vagrant up` to initialize the virtual machine, and run the command `vagrant ssh` to log in

Import the newsdata.sql data and schema to a database labeled _news_ by running the command `psql -d news -f newsdata.sql`

### **How to use?**
The newsdata.py script provides a function `log_results()` that writes the results of a SQL query to a .txt file labeled `log_results.txt`

The `log_results()` function has two parameters:

* `query` -- the SQL query to be executed
* `mode` -- optional argument to specify the file mode (default "w+")


There are three SQL queries provided in the newsdata.py script:

* `pop_authors` -- returns the top 3 most popular articles of all time (by page views)
* `pop_articles` -- returns the most popular article authors of all time (by page views)
* `req_errors` -- returns the day(s) on which more than 1% of requests led to errors

Running the newsdata.py script included in this repository will write the results of all three of the built-in SQL queries to the `log_results.txt` file.

**Database Views:**
No views were created for this project.

## **License**
This project is licensed under the MIT License - see the LICENSE.md file for details.