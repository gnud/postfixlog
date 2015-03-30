#!/usr/bin/python2

__author__ = "Damjan Dimitrioski"
__version__ = "0.1"

import re

import argparse

argparser = argparse.ArgumentParser(description="Parse some postfix mail log to csv")
argparser.add_argument("filename")

args = argparser.parse_args()
filename = args.filename

DEBUG = False

# Change or add values to the header
CSV_HEADER_LINE = "Hour of submission, Nr of submission, Who Country code, email adresses to:"

# CSV Template layout, change it if needed
ExportTemplate = "%s,%s,%s,%s,%s"


class Report():
    """

    """

    def __init__(self, csv_out_file="report.csv"):
        """
        """

        self.csv_out_file = csv_out_file
        # Format is key = linenumber, value is { dictionary with: key: msg_type, value: msg_content }
        self.items = {

        }

        self.csv_lines = []

    def add(self, line):
        """
        :param line: String CSV line
        """

        self.csv_lines.append(line)

    def export_csv(self):
        """
        """

        from os import linesep

        csv_file = open(self.csv_out_file, "w")

        csv_file.write(CSV_HEADER_LINE + linesep)

        for l in self.csv_lines:
            csv_file.write(l + linesep)
        csv_file.close()


class LogParser(object):
    """
    Parses given mail postfix log list
    """

    @staticmethod
    def find_value(test_str, column_name):
        """
        Find a value of some attribute
        :return: String value of the attribute
        """

        value = ""
        p = re.compile(r"%s=<([^<>]*?)>" % column_name)

        try:
            value = re.search(p, test_str.strip("\n")).group(1)
        except AttributeError:
            pass

        return value

    @staticmethod
    def extract_message_date(test_str):
        """
        Extract the date value
        :param test_str: String line content
        :return String value of the message date
        """

        value = ""

        p = re.compile(r"(^\w{3,4}[^a-zA-Z]+)")

        try:
            value = re.search(p, test_str.strip("\n")).group(1)
        except AttributeError:
            pass

        return value

    def extract_message_from(self, test_str):
        """
        :param test_str:
        :return String value of the message from
        """

        return self.find_value(test_str, "from")

    def extract_message_to(self, test_str):
        """
        :param test_str:
        :return String value of the message to
        """

        return self.find_value(test_str, "to")

    def __init__(self, log_data, report):
        """
        Parser constructor
        """

        self.report = report
        self.log_data = log_data

        for line in log_data[10:-1]:
            if "from=" in line or "to=" in line:
                message_date = self.extract_message_date(line)
                message_from = self.extract_message_from(line)
                message_to = self.extract_message_to(line)

                data_line = ExportTemplate % (message_date, "", message_from, "", message_to)  # + line

                # don't print if line is empty
                if len(data_line.replace(",", "")) > 0:
                    report.add(data_line)

                if DEBUG:
                    print "**************************************"

        if DEBUG:
            print "\nI am done!"


def file_log2_list(my_log):
    """

    :param my_log: String file path
    :return: List of the file lines
    """

    my_list = []

    for line in open(my_log, "r"):
        my_list.append(line.strip("\n"))

    return my_list


def main():
    log_data = file_log2_list(filename)
    report = Report(filename + ".csv")

    LogParser(log_data, report)

    report.export_csv()


if __name__ == "__main__":
    main()
