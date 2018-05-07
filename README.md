# Project: Logs Analysis

This program is a reporting tool that prints out reports (in plain text) based on the data in the database.  This program is a Python program using the psycopg2 module to connect to the database.

## Requirements

- This program requires python 2.7.
- This program requires psycopg2 Python module.
- This program requires PostgreSQL 9.5.
- Database data file can be downloaded from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. To load the data into your local database, use the following command:
```
$ psql -d news -f newsdata.sql
```

## Usage

Run the following command:

```
$ python logs_analysis.py
```

## License

This project has no license.
