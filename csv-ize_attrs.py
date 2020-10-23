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
                if not key in super_keys:
                    super_keys[key] = {}

            break

    oldFile.close()

    # newFile = open('./separated_attribs.csv', "w")
    # writer = csv.writer(newFile)

    # with open('./attribs.csv') as oldFile:
    #     readCSV = csv.reader(oldFile, delimiter=',')
    #     headers = next(readCSV, None)
    #     writer.writerow(headers)

    #     for row in readCSV:
    #         row_copy = row

    #         writer.writerow(row_copy)
    # oldFile.close()
    # newFile.close()

    # t1 = time.time()
    # total = t1-t0
    # print(total)


if __name__ == "__main__":
    main()
{"RestaurantsTakeOut": "True", "BusinessParking": {"garage": False, "street": False, "validated": False, "lot": False, "valet": False}, "WiFi": "no", "RestaurantsDelivery": "False", "OutdoorSeating": "False", "RestaurantsAttire": "casual", "BusinessAcceptsCreditCards": "True", "RestaurantsGoodForGroups": "True",
    "RestaurantsReservations": "False", "HasTV": "False", "Ambience": {"romantic": False, "intimate": False, "touristy": False, "hipster": False, "divey": False, "classy": False, "trendy": False, "upscale": False, "casual": False}, "Alcohol": "none", "RestaurantsPriceRange2": "1", "GoodForKids": "True"},
