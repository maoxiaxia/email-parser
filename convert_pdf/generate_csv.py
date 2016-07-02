#!/usr/bin/python
import sys
import csv

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


def get_cols_num(file_name, data, num):
    """Get number of cols.

    return number of cols.
    """
    count = 0
    for item in data:
        if item.find("%") > 0:
            count += 1
    return count / num


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


def get_header(data):
    """Get the header of the table.

    return header.
    """
    header = ""
    for item in data:
        if len(item) > 10:
            header = item
            break
    return header


def fill_table(info):
    """Fill the rest of cells in table.

    modified the table
    """
    # extrac attributes from info struct
    data = info["data"]
    table = info["table"]
    header = info["header"]
    row_num = info["row_num"]

    currency_type_num = row_num - 1
    row_index = 0
    col_index = 0
    i = 0
    while i < len(data):
        if data[i].find("%") > 0:
            # stat data
            while i < len(data) and row_index < currency_type_num:
                table[row_index+1].append(data[i])
                row_index += 1
                i += 1
            # Reset row_index
            row_index = 0
        else:
            if i < row_num - 1:
                # currency Type
                table[i+1].append(data[i])
            else:
                # time marker
                if data[i] != header:
                    table[0].append(data[i])
            i += 1

    # End loop
    return None


def print_table(table):
    """Print table.

    simple print.
    """
    for i in range(len(table)):
        print "Row ", i, "\t",
        for j in range(len(table[i])):
            print table[i][j],
        print "\n"


def generate_csv(table):
    """Generate csv file.

    generate the file.
    """
    with open("result.csv", "w") as csvfile:
        for i in range(len(table)):
            for j in range(len(table[i])):
                if j != len(table[i])-1:
                    tmp = table[i][j] + ","
                else:
                    tmp = table[i][j] + "\n"
                csvfile.write(tmp)


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

    # Get number of cols in table
    col_num = get_cols_num(file_name, data, row_num - 1)

    # Get header of table
    header = get_header(data)
    trimmed_header = header.replace("\t \xc2\xa0", " ")

    info = {
        "data": data,
        "row_num": row_num,
        "table": table,
        "header": header
    }

    # Fill the rest of cells in table
    fill_table(info)
    print_table(table)

    generate_csv(table)


if __name__ == '__main__':
    main()
