#!/usr/bin/python
import os
import sys

def get_rows_num(file_name):
    """Get number of rows in table.

    return number of rows
    """
    # By default add the first datetime
    row_num = 1
    with open(file_name, "r") as file:
        for line in file:
            if line == "\n":
                break
            else:
                row_num += 1

    return row_num


def init_table(row_num):
    """Initialize the table.

    return the init table in the form of array
    """
    # Initialize the number of rows in table
    table = []
    for i in range(row_num):
        row = []
        table.append(row)

    # Append the default first cell to the table
    table[0].append("Curreny Type")

    return table


def get_data(file_name):
    """Get the parsed data.

    return the data saved in array.
    """
    data = []
    with open(file_name, "r") as file:
        for line in file:
            if (line != "\n"):
                data.append(line.rstrip("\n"))

    return data


def main():
    # Check number of argv
    if len(sys.argv) != 2:
        print "Oops, you might forget add the output file as arg"
        sys.exit(0)

    # Get the file name
    file_name = sys.argv[1]

    # Get number of rows in table
    row_num = get_rows_num(file_name)

    # Generate init table
    table = init_table(row_num)

    # Get the parsed data saved in array
    data = get_data(file_name)
    print(data)
    print(table)


if __name__ == '__main__':
    main()
