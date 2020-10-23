def main():

    import csv
    import json
    import time

    t0 = time.time()
    super_keys = {}

    with open('./attribs.csv') as oldFile:
        readCSV = csv.reader(oldFile, delimiter=',')
        next(readCSV, None)

        for row in readCSV:
            if len(row) == 0:
                continue
            updated = row[0]
            updated = updated.replace("\"u'", "\"'")
            updated = updated.replace("'", "\"")
            updated = updated.replace("False", "\"False\"")
            updated = updated.replace("True", "\"True\"")
            updated = updated.replace("\"\"", "\"")
            updated = updated.replace("\"{", "{")
            updated = updated.replace("}\"", "}")

            as_json = json.loads(updated)
            for key in as_json.keys():
                if key not in super_keys:
                    super_keys[key] = []
                value = as_json[key]
                value_list = super_keys[key]
                if type(value) is dict:
                    for baby_key in value.keys():
                        if(baby_key not in value_list):
                            super_keys[key].append(baby_key)

    oldFile.close()

    with open('./attribs.csv') as oldFile:
        readCSV = csv.reader(oldFile, delimiter=',')
        next(readCSV, None)

        newFile = open('./attr_hash.csv', "w")
        writer = csv.writer(newFile)

        readCSV = csv.reader(oldFile, delimiter=',')
        headers = convert_to_header_format(super_keys)
        writer.writerow(headers)

        for row in readCSV:
            if len(row) == 0:
                continue
            updated = row[0]
            updated = updated.replace("\"u'", "\"'")
            updated = updated.replace("'", "\"")
            updated = updated.replace("False", "\"False\"")
            updated = updated.replace("True", "\"True\"")
            updated = updated.replace("\"\"", "\"")
            updated = updated.replace("\"{", "{")
            updated = updated.replace("}\"", "}")
            as_json = json.loads(updated)

            all_vals = []

            for key in headers:

                this_val = ""
                val_to_check_for = ""
                if ">>" in key:
                    val_to_check_for = key.split(">>")
                else:
                    val_to_check_for = key
                if type(val_to_check_for) is list:
                    if(val_to_check_for[0] in as_json and (val_to_check_for[1] in as_json[val_to_check_for[0]])):
                        this_val = as_json[val_to_check_for[0]
                                           ][val_to_check_for[1]]
                else:
                    if(val_to_check_for in as_json):
                        this_val = as_json[val_to_check_for]
                print(this_val)
                all_vals.append(this_val)

            writer.writerow(all_vals)

        newFile.close()

    oldFile.close()

    t1 = time.time()
    total = t1-t0
    print(total)


def convert_to_header_format(key_hash):
    """key_hash is a dictionary with strings as keys and lists of strings as values

    Converts to a list to be used as headers for a csv
    """
    list_of_headers = []

    for key in key_hash.keys():

        if(len(key_hash[key]) > 0):
            for value in key_hash[key]:
                list_of_headers.append(
                    convert_to_value_header_format(key, value))
        else:
            list_of_headers.append(key)

    print(list_of_headers)

    return list_of_headers


def convert_to_value_header_format(key, value):
    return key+">>"+value


if __name__ == "__main__":
    main()
