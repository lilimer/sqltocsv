# SQL to CSV Exporter

## Overview
This Python application provides a graphical user interface (GUI) to connect to a MariaDB or MySQL database, list its tables, and export selected tables to CSV files. It uses wxPython for the GUI and mysql-connector-python for database interaction.

## Features
- Connect to a MariaDB or MySQL database
- List all tables in the database with checkboxes
- Export one or more selected tables to CSV files

## Requirements
- Python
- wxPython
- mysql-connector-python
- pandas

## Usage
1. Install `requirements.txt`
2. Specify the details of your connection in `config.ini`
3. Run `converter.py`