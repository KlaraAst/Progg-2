
'''
Deluppgift 1: Skriv en funktion OU4_1(filename) som tar ett argument (filename) läser in denna fil (exempelvis tempdata.csv)
och beräknar medeltemperaturen för hela tidsperioden, och returnerar denna.

Deluppgift 2: Skriv en annan funktion OU4_2(filename) som beräknar årsmedelvärderna för data i filen filename och plottar dem
som stapeldiagram. Sista året kan du utelämna, där är inte serien komplett. Spara även årsmedelvärdena i en ny CSV-fil med namnet
givet av "mean_"+filename  (exempelvis mean_tempdata.csv) med år och årsmedelvärde i två kolumner.

Deluppgift 3: Årsmedelvärderna varierar kraftigt och det kan vara svårt att se några trender, och du ska nu skriva kod för att
beräkna medelvärden under större intervall än ett år, samt visualisera detta.
'''


import matplotlib.pyplot as plt
import numpy as np

from prettytable import PrettyTable
import pandas as pd
from pandas import *


def OU4_1(filnamn):  #Ange med ''

    # reading CSV file
    data = read_csv(filnamn, dtype={"# Year": int, " Month": int, " Day": int, " Temp": float})
    #print(data.columns)  #Kolla kolumnnamn

    temp = data[' Temp'].tolist()   #Kolumndata till lista ----> Lagt till mellanslag då dessa finns i filen. Kan även ändras i filen själv
    med_temp = sum(temp)/len(temp)  #Medelvärde

    return med_temp

print('Medeltemperatur =', OU4_1('tempdata.csv'))


#%%

#'tempdata.csv'

def OU4_2(filnamn):  #Ange med ''

    data = read_csv(filnamn, dtype={"# Year": int, " Month": int, " Day": int, " Temp": float})

    temp = data[' Temp'].tolist()  # Kolumndata till lista
    year = data['# Year'].tolist()

    temp_sum_list = [temp[0]]  # Första värden
    year_list = [year[0]]

    index_tot = 1  # counter för indexering i loop --> inte noll då första värden lagts in i listorna
    index_year = 1   #Indexering för alla värden i datan



    while year[index_tot] != 2024:  ## Skippar år 2024                  XXXXX

        # Kollar om året vid index är nytt eller redan förekommer
        if year[index_tot] in year_list:

            temp_sum_list[index_year - 1] = temp_sum_list[index_year - 1] + temp[index_tot]  # Adderar föregående sparat värde med det nya för samma år
            index_tot = 1 + index_tot

        if year[index_tot] not in year_list:

            year_list.append(year[index_tot])  #Lägger till nytt förekommande år
            temp_sum_list.append(temp[index_tot])   #Lägger till nya temperaturer på nytt index

            index_tot = 1 + index_tot
            index_year = 1 + index_year   #Ändras endast för nytt år då alla temperaturer för ett specifikt års index ska summeras



    temp_med_list = [temp_sum_list[i-1]/365 for i in range(len(temp_sum_list))]    #Medelvärde per år (365 dagar)


#%%
    ############# Snygg tabell över vad som sparas i CSV-fil #############

    columns = ["År", "Medeltemperatur [*C]"]
    myTable = PrettyTable()
    myTable.add_column(columns[0], year_list)
    myTable.add_column(columns[1], temp_med_list)
    #print(myTable)


#%%
    ############# Skapar CSV-fil #############


    csv_file_path = 'mean_tempdata.csv'
    csv_data = np.array(['Ar', 'Medeltemperatur [*C]'])

    tot_rows_add = []

    for i in range(len(year_list)-1):   #-1 då 2024 kommer med

        add_row = [year_list[i], temp_med_list[i]]
        tot_rows_add.append(add_row)

    csv_data = np.r_[[csv_data], tot_rows_add]

    # Open the file in write mode
    with open(csv_file_path, mode='w', newline='') as file:

    # Create a csv.writer object
        writer = csv.writer(file)

        # Data till CSV fil
        writer.writerows(csv_data)


    ############# Bar plot #############

    plt.ylabel('Medeltemperatur')
    plt.xlabel('År')
    plt.bar(year_list, temp_med_list)   #Stapeldiagram
    plt.show()

    return temp_med_list, year_list


#%%

import csv
import numpy as np
from pandas import *


def OU4_3(interval, filnamn):  #Ange med ''

    #interval = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    temp_med_list = OU4_2(filnamn)[0]  # Listor från OU4_2
    year_list = OU4_2(filnamn)[1]

    # Antal år = 268 (utan 2024)
    year_list.pop(268)
    temp_med_list.pop(268)

    n = int(len(interval)/2) # Antal "Sidovärde"

    temp_med_interval = []
    year_intervals = []
    interval_sum = [] #summering av "current" intervall
    counter = 0

    for year in year_list:

        n_interval = 0  # indexering för intervall
        interval_sum.append(temp_med_list[year_list.index(year)])   #Motsvarande med.temp, motsvarar värdet när counter +/- i är noll

        for i in range(n):

            if counter - i > 0:    #Undviker negativ indexering om counter-i blir negativ
                try:
                    if temp_med_list[counter - i] not in interval_sum:     #Undviker repetition när i = 0
                        interval_sum.append(temp_med_list[counter - i])
                        n_interval = n_interval + 1  # Anger antal värden som tagits med i intervall för beräkning av medelvärdet i med_value_copy
                except IndexError:
                    pass

            if counter + i > 0:    #Undviker negativ indexering om counter-i blir negativ
                try:
                    if temp_med_list[counter + i] not in interval_sum:     #Undviker repetition när i = 0
                        interval_sum.append(temp_med_list[counter + i])
                        n_interval = n_interval + 1  # Anger antal värden som tagits med i intervall för beräkning av medelvärdet i med_value_copy
                except IndexError:
                    pass


        med_value_copy = sum(interval_sum) / n_interval    #Medelvärde, intervall kopia för att kunna nollställa lista
        temp_med_interval.append(med_value_copy)
        year_intervals.append(counter+1)    #Sparar vilket intervall vi är på genom counter. +1 å counter är 0 vi start för inexering, men representerar intervall 1

        interval_sum.clear()

        counter = counter + 1

    plt.ylabel('Medeltemperatur för valt intervall [*C]')
    plt.xlabel('Årsintervall')
    plt.bar(year_intervals, temp_med_interval)  # Stapeldiagram
    plt.show()



    ########## Subtraherar globalt medelvärde ###########

    med_glob = OU4_1('tempdata.csv')   #Globalt medelvärde

    plt.ylabel('Medeltemperatur per intervall minus globalt medel [*C]')
    plt.xlabel('Årsintervall')

    temp_glob = [temp_med_interval[i-1] - med_glob for i in range(len(temp_med_interval))]
    plt.bar(year_intervals,temp_glob)  # Stapeldiagram
    plt.show()



######### Kallar funktion #############

size = int(input('Storlek av intervall: '))
interval = []                                              # XXXXXX   Godkänt intervall????

for i in range(size):
    interval.append(i)

OU4_3(interval, 'tempdata.csv')



