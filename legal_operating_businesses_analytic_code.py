import pandas, folium, math, webbrowser
import matplotlib.pyplot as plot
from folium.plugins import HeatMap
from time import sleep

# ====================================================================================================||

dataset = pandas.read_csv("Legally_Operating_Businesses.csv")

# ====================================================================================================||

def line_separator():
    print("====================================================================================================||")

def introduction():
    line_separator()
    print('''[INTRODUCTION]
This program is to help the user to analyze data in the file 'Leagally Operating Businesses\'''')
    
    pause()
    return None

# ====================================================================================================||

def pause():
    return sleep(1)

def confirm():
    while True:
        user_input = input("Confirm: ").lower()

        if user_input == "yes" or user_input == "y":
            pause()
            return True
        
        elif user_input == "no" or user_input == "n":
            pause()
            return False
        
        else:
            print("Please confirm your selection by entering 'yes' or 'no': ")
            pause()

def print_list(list, title):
    line_separator()
    print(f"[{title}]")
    
    for i in range(len(list)):
        print(f"[{i+1}] {list[i]}")

    pause()

def return_function(string):
    string = string.lower()
    string = string.split()
    function = "_".join(string)
    return eval(function + "()")

def get_category(type):
    category_list = []

    for i in dataset.columns:
        category_list.append(i)
    
    while True:        
        user_input = input(("Category: ")).lower()
        pause()

        match user_input:
            case "return":
                main_menu()
            
            case "help":
                print_list(category_list, "CATEGORY LIST")
            
            case _:
                for i in category_list:
                    if user_input in i.lower():
                        print(f"Category matched: {i}")

                        if confirm():
                            return dataset[i]
                        
                        else:
                            return_function(type)
            
                print(f"Category '{user_input}' not found, enter 'help' to acquire available categories")

# ====================================================================================================||

def main_menu():  
    main_menu_list = ["search directory", "count dictionary", "location spread map"]

    while True:
        line_separator()
        print('''[MAIN MENU]
Enter an operator to start with.''')

        user_input = input("Enter: ").lower()
        pause()
        
        match user_input:
            case "exit":
                exit()
            
            case "help":
                print_list(main_menu_list, "OPERATOR LIST")
            
            case _:
                for i in main_menu_list:
                    if user_input in i:
                        print(f"Command operator matched: {i}")

                        if confirm():
                            return_function(i)

                        else:
                            main_menu()

                print(f"Command '{user_input}' not found, enter 'help' to acquire available command operators")

# ====================================================================================================||

def search_directory():  
    line_separator()
    print('''[SEARCH DIRECTORY]
Enter a category.''')

    category = get_category(type="search directory")

    while True:
        search_list = []

        line_separator()
        print('''[SEARCH DIRECTORY]''')

        user_input = input(f"Search field: ").lower()
        pause()

        if user_input == "return":
            main_menu()

        else:
            for i in category:
                if str(i).lower() != "nan":
                    if user_input in i.lower():
                        search_list.append(i)

            if len(search_list) == 0:
                print("No result found")
            
            elif len(search_list) == 1:
                print(f"Search result: {search_list[0]}")
                
                pause()
                return get_info(category, search_list[0])

            elif len(search_list) > 30:
                print(f"There are currently {len(search_list)} results found, please be more specific to help limit search results")
                
            else:
                print_list(search_list, "SEARCH RESULT")

                while True:
                    user_input = input("Select result: ")
                    
                    try:
                        print(f"Search result: {search_list[int(user_input) - 1]}")
                        
                        pause()
                        return get_info(category, search_list[int(user_input) - 1])
                    
                    except (TypeError, IndexError, ValueError):
                        print("Please enter the number displayed as an option")

def count_dictionary():
    line_separator()
    print('''[COUNT DICTIONARY]
Enter a category.''')

    category = get_category(type="count dictionary")

    line_separator()
    print("[COUNT DICTIONARY]")

    count_dict = {}

    for i in range(len(category)):
        if str(category[i]) != "nan":
            if category[i] in count_dict:
                count_dict[category[i]] += 1
            else:
                count_dict[category[i]] = 1
        
    if len(count_dict) < 20:
        for key, value in count_dict.items():
            print(f"{key}: {value}")
            
        return get_graph(count_dict)
    
    else:
        print("Dictionary overflowed, please try another category")
        count_dictionary()

def location_spread_map():
    line_separator()
    print('''[ALL BUILDING LOCATION SPREAD MAP]
Do you want to get the map of the location spread of all legally operating businesses?''')

    if confirm():
        dataset.dropna()
        latitude_mean = dataset["Latitude"].mean()
        longitude_mean = dataset["Longitude"].mean()

        list_of_datapoints = []
        for _, each_row in dataset.iterrows():
            if not math.isnan(each_row["Latitude"]):
                list_points = []
                list_points.append(each_row["Latitude"])
                list_points.append(each_row["Longitude"])
                list_of_datapoints.append(list_points)

        map = folium.Map(location=[latitude_mean, longitude_mean], zoom_start = 10.5)
        HeatMap(list_of_datapoints).add_to(map)
        map.save("legal_op_businessess_all_building_spread.html")

        webbrowser.open_new_tab("legal_op_businessess_all_building_spread.html")

        main_menu()
    else:
        main_menu()

# ====================================================================================================||

def get_info(category, search_result):
    line_separator()
    print('''[GET INFO]
Do you want to get all the information related to the search result?''')

    if confirm():
        for i in range(len(category)):
            if category[i] == search_result:
                line_separator()
                print("[BUILDING INFORMATION]")

                print(dataset.iloc[i])
                return get_building_location(dataset.iloc[i])
    else:
        search_directory()

def get_building_location(building):
    line_separator()
    print('''[BUILDING LOCATION MAP]
Do you want to get the map location of the building?''')

    if confirm():
        if str(building[25]) != "nan" and str(building[24]) != "nan":
            location_point = []
            location_point.append([building[25], building[24]])

            map = folium.Map(location=[building[25], building[24]], zoom_start = 17.5)
            HeatMap(location_point).add_to(map)
            map.save("legal_op_businessess_building_location.html")

            webbrowser.open_new_tab("legal_op_businessess_building_location.html")
            search_directory()

        else:
            print("The building does not have a specific latitude and longitude")
            search_directory()

    else:
        search_directory()

def get_graph(dictionary):
    line_separator()
    print('''[GRAPH]
Do you want to get the graph of the values counted?''')

    if confirm():
        x_value = []
        y_value = []

        for key, value in dictionary.items():
            x_value.append(key)
            y_value.append(value)

        plot.figure(figsize=(12,7))
        plot.bar(x_value, y_value)
        plot.xticks(rotation=27.5)
        plot.show()

        count_dictionary()

    else:
        count_dictionary()

# ====================================================================================================||

def start_program():
    introduction()

    while True:
        try:
            main_menu()
        
        except (TypeError, ValueError, IndexError, ZeroDivisionError):
            line_separator()
            print("[ERROR]")
            print("Unknown error occured, redirecting to Main Menu")
            
            pause()
            
            main_menu()

# ====================================================================================================||

start_program()