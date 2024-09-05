import csv

input_year_s = int(input("Please input the first year:"))
input_year_e = int(input("Please input the last year:"))

output_files = {}

for i in range(0, (input_year_e - input_year_s)+1, 1):
    input_file_name = "data_" + str(input_year_s+i) + ".csv"
    input_file = open(input_file_name, encoding="utf-8")

    reader = csv.reader(input_file)
    header = next(reader)

    for row in reader:
        match row[3]:
            case "JCR資料庫-AHCI":
                category = "JCR_AHCI"

            case "JCR資料庫-SCIE":
                category = "JCR_SCIE"

            case "JCR資料庫-SSCI":
                category = "JCR_SSCI"

            case "JCR資料庫-ESCI":
                category = "JCR_ESCI"

            case "Scopus":
                category = "Scopus"

            case "TCI資料庫(國家圖書館-臺灣人文及社會科學引文資料庫)":
                category = "TCI"

            case "THCI":
                category = "THCI"

            case "TSSCI":
                category = "TSSCI"

            case "文學院認列核心期刊":
                category = "文學院認列核心期刊"

            case "管理學院傑出期刊":
                category = "管理學院傑出期刊"

            case _:
                category = row[3]

        output_file_name = f"{category}({input_year_s}~{input_year_e}).csv"

        if output_file_name not in output_files:
            output_files[output_file_name] = open(output_file_name, 'a+', newline='', encoding="utf-8-sig")
        
        writer = csv.writer(output_files[output_file_name])
        writer.writerow(row)