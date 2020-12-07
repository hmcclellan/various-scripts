def main():

    import csv
    import hashlib
    import os
    import time
    import binascii
    import http.client
    import json
    import geopy.distance


    t0 = time.time()

    salt = open('../../../Desktop/dataviz/project_sandbox/salt.txt', 'r').read()
    salt_bytes = salt.encode('utf-8')
    mb_key = open('../../../Desktop/dataviz/project_sandbox/mbkey.txt', 'r').read()

    
    # years = [2015, 2016, 2017, 2018, 2019]
    years = [2019]

    limit=599
    counted = 0

    conn = http.client.HTTPSConnection("api.mapbox.com")
    conn.request("GET", "/geocoding/v5/mapbox.places/minneapolis,mn.json?access_token="+mb_key)
    response = json.loads(conn.getresponse().read())
    start_line = response["features"][0]["center"]

    for year in years:

        newFile = open('../../../Desktop/dataviz/anonymized' +
                       '_tcm_'+str(year)+'.csv', "w")
        writer = csv.writer(newFile)

        with open('../../../Desktop/dataviz/project_sandbox/tcm_'+str(year)+'.csv') as oldFile:
            readCSV = csv.reader(oldFile, delimiter=',')
            headers = next(readCSV, None)
            headers.append("LatLong")
            headers.append("DistanceToStartLine")
            rowNumber=0
            writer.writerow(headers)

            for row in readCSV:
                rowNumber= rowNumber+1
                row_copy = row

                runnerName = row[1].encode('utf-8')

                hashed = hashlib.pbkdf2_hmac('sha256', runnerName, salt_bytes, 4)

                row_copy[1] = binascii.hexlify(hashed)

                if(counted==limit):
                    time.sleep(63)
                    counted=0
                    "/"
                
                counted = counted+1
                location = row[4]+","+row[5]
                location = location.replace(' ', '%20')
                conn = http.client.HTTPSConnection("api.mapbox.com")
                conn.request("GET", "/geocoding/v5/mapbox.places/"+location+".json?access_token="+mb_key)
                response = json.loads(conn.getresponse().read())
                lat_long=""
                distance_to_start_line = ""
                try:
                    center = response["features"][0]["center"]
                    lat_long = str([center[1], center[0]])
                    distance_to_start_line = geopy.distance.geodesic((center[1], center[0]), (start_line[1], start_line[0])).mi
                except Exception:
                    lat_long=""
                    distance_to_start_line = ""
                finally:
                    row_copy.append(lat_long)
                    row_copy.append(distance_to_start_line)
                writer.writerow(row_copy)
        oldFile.close()
        newFile.close()

    t1 = time.time()
    total = t1-t0
    print(total)


if __name__ == "__main__":
    main()
