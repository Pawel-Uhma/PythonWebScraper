import pandas as pd
import numpy as np
import csv,time

def main():
    df = pd.read_csv("scraper/oferty_mieszkań.csv")

    shape = df.drop_duplicates().shape
    rows_no_duplicates = shape[0]
    print(rows_no_duplicates)

    print("PRICE")
    price_median = round(np.median(df['price']))
    print("MEDIAN : " + str(price_median))
    price_average = round(np.average(df['price']))
    print("AVERAGE : " + str(price_average))

    print("PRICE_PM")
    price_pm_median = round(np.median(df['price_pm']))
    print("MEDIAN : " + str(price_pm_median))
    price_pm_average = round(np.average(df['price_pm']))
    print("AVERAGE : " + str(price_pm_average))

    print("SIZE")
    size_median = round(np.median(df['size']),4)
    print("MEDIAN : " + str(size_median))
    size_average = round(np.average(df['size']),4)
    print("AVERAGE : " + str(size_average))


    file_name = "data_science/timetable.csv"
    cur_time = time.time()
    csv_file = open(file_name, 'a',newline = '',encoding="utf8")
    writer = csv.writer(csv_file,delimiter = ',')
    writer.writerow([cur_time, rows_no_duplicates,price_median, price_average,price_pm_median,price_pm_average,size_median, size_average])
    csv_file.close()





if __name__ == "__main__":
    main()