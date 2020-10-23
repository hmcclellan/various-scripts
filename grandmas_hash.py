def main():

    import csv
    import hashlib
    import os
    import time
    import binascii

    t0 = time.time()

    salt = open('../../../Desktop/dataviz/project_sandbox/salt.txt', 'r').read()
    years = [1977 + x for x in range(11)]
    for year in years:
        newFile = open('../../../Desktop/dataviz/project_sandbox/' +
                       'grandmas_marathon/anonymized' +
                       '_grandmas_'+str(year)+'.csv', "w")
        writer = csv.writer(newFile)

        with open('../../../Desktop/dataviz/project_sandbox/grandmas_marathon/' +
                  'grandmas_'+str(year)+'.csv') as oldFile:
            readCSV = csv.reader(oldFile, delimiter=',')
            headers = next(readCSV, None)
            writer.writerow(headers)

            for row in readCSV:
                row_copy = row

                hashed = hashlib.pbkdf2_hmac('sha256', row[1], salt, 4)
                row_copy[1] = binascii.hexlify(hashed)
                writer.writerow(row_copy)
        oldFile.close()
        newFile.close()

    t1 = time.time()
    total = t1-t0
    print(total)


if __name__ == "__main__":
    main()
