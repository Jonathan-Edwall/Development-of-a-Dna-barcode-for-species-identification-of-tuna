"""
=============================================================================================================
=      =====================================  ===============================================  ==============
=  ===  ====================================  ===============================================  ==============
=  ====  ===================================  ===============================================  ==========  ==
=  ===  ====   ===  =   ====   ====   ======  ===   =========   ====   ===    ========    ===  ===   ===    =
=      ====  =  ==    =  ==  =  ==     ===    ==  =  =======  =  ==  =  ==  =  =======  =  ==  ==     ===  ==
=  ===  ======  ==  =======  =====  =  ==  =  ==     ========    =====  ==  =  =======  =  ==  ==  =  ===  ==
=  ====  ===    ==  =======  =====  =  ==  =  ==  =============  ===    ==    ========    ===  ==  =  ===  ==
=  ===  ===  =  ==  =======  =  ==  =  ==  =  ==  =  =======  =  ==  =  ==  ==========  =====  ==  =  ===  ==
=      =====    ==  ========   ====   ====    ===   =========   ====    ==  ==========  =====  ===   ====   =
=============================================================================================================
¤ This python script creates a barcode gap plot for potential barcode candidates. 
¤ The script is currently modified to work for only DNA-barcode candidates for species identification of the tuna tribe Thunnini.
¤
¤ The script could be used for any barcode-candidates and is not restricted to work only for tunas. However, to make the script applicable for other/additional species, the user will have to manually change the contents of the lists "Long_name_list" and/or "Short_name_list" and make sure all the species being studied are included in these 2 lists. To avoid missleading results, make sure any outgroup is not included in these 2 lists.
¤ These modifications will ensure that these non-tuna species will be included in the plot (as long as they have inter and intra k2p-values in the input-file) :)
¤
¤
¤ !!! Input-file: The inputfile required for this script to function, must be a column-DistanceData-file in csv-format, created from the software "MEGA 11".
¤ Other versions of Mega-software might work, but as of now, the code has been developed to work for MEGA 11.
¤ ~~ Common errors if the script does not work:
¤ *The inputfile is in xlsx-format (instead of in csv-format), leading to the failure of reading the input-file using "with open"
¤
¤ Author: Jonathan Edwall
¤ Email: edwalljonathan@gmail.com
"""
import re
import numpy as np
import matplotlib.pyplot as plt
import math

input_DistanceDATA_file = input(f"Name the file you want to create a barcode gap plot from \n (Don't forget to write the full filename) \n")

"""The 2 lists below store information about how the full name or the abbreviated name of species from the tuna family should look like """
Long_name_list = ['Allothunnus fallai','Auxis rochei','Auxis thazard','Euthynnus affinis','Euthynnus alletteratus', 'Euthynnus lineatus',
'Katsuwonus pelamis', 'Thunnus alalunga', 'Thunnus maccoyii','Thunnus obesus','Thunnus orientalis','Thunnus thynnus'
,'Thunnus atlanticus','Thunnus tonggol','Thunnus albacares'] #Salmo salar, the outgroup has been removed from the list. Dont want k2p-value from it

Short_name_list = ['Al.fallai',"A.fallai","Au.rochei","A.rochei",'Au.thazard',"A.thazard",'E.affinis','E.alletteratus','E.lineatus',
'K.pelamis','T.alalunga', 'T.maccoyii','T.obesus','T.orientalis','T.thynnus'
,'T.atlanticus','T.tonggol','T.albacares']#S.salar, the outgroup has been removed from the list. Dont want k2p-value from it



""" 
 #######                                                               
 #        #    #  #    #   ####   #####  #   ####   #    #   ####  
 #        #    #  ##   #  #         #    #  #    #  ##   #  #      
 #####    #    #  # #  #  #         #    #  #    #  # #  #   ####  
 #        #    #  #  # #  #         #    #  #    #  #  # #       # 
 #        #    #  #   ##  #         #    #  #    #  #   ##  #    # 
 #         ####   #    #   ####     #    #   ####   #    #   ####  
                                                                                                                                                                                                                                                                                    
"""



""" 
species_name_style_finder() finds out from the user if; 
the inputfile has the full species names, or the shortened version of them
"""
def species_name_style_finder():
    current_species_name_style = ""
    while current_species_name_style == "":
        print("\n ********* Enter how the species' names are written in the input Distance data-file from MEGA. Choose between: 1 or 2 *******")
        print(f' 1: Euthynnus affinis \n \t (The full species name) \n 2: E.affinis \n \t (The species names are abbreviated/shortened)')
        input_current_species_name_style = input(f"\n Input if {input_DistanceDATA_file} has the full species names or abbreviated/shortened species names \n (1/2) \n").lower()
        if input_current_species_name_style == "1" or input_current_species_name_style == "2":
            current_species_name_style = input_current_species_name_style
        else:
            print(f" \n\n!!!!!!!!!!!!!!!!!! Error: {input_current_species_name_style} is not an alternative \n Choose between: (1/2) !!!!!!!!!!!!!!!!!!")
    print(f"*****************************************************************************************************************************")
    return current_species_name_style



"""
find_species_long_species_name() finds the full species names for every row in the k2p distance matrix 
and then returns them
"""
def find_species_long_species_name(line): 
    pattern = re.compile(r"[a-zA-Z]{1,}[' ']{1,}[a-zA-Z]{5,}")
    match = pattern.findall(line)
    specieslist = []
    for hit in match:
        if hit in Long_name_list:
            specieslist.append(hit)
    return specieslist



""" 
find_species_short_species_name() finds the shortened species names for every row in the k2p distance matrix
and then returns them
"""
def find_species_short_species_name(line):  
    pattern = re.compile(r"[a-zA-Z]{1,2}['.'][a-zA-Z]{5,}")
    match = pattern.findall(line)
    specieslist = []
    for hit in match:
        if hit in Short_name_list:
            specieslist.append(hit)
    return specieslist



""" 
k2p_value_finder() finds the K2P-value for every row in the k2p distance matrix 
and then returns them
"""
def k2p_value_finder(line):
    number_pattern = re.compile(r"[0-1]{1,}[,.]{1}[0-9]{5,}")
    match = str(number_pattern.findall(line))
    k2p_value = match.replace("['","").replace("']","").replace(",",".")
    return float(k2p_value)



""" 
inter_intra_k2p_sorter() gets a k2p-value and the species names for every row in the k2p distance matrix 
and determines if the k2p-value is between species, or among species. 
In other words the functions sorts and determines if the K2P-value is for inter or intra divergence
"""
interk2p_dict = {}
intrak2p_dict = {}
def inter_intra_k2p_sorter(species_list,k2p_value): 
    k2p_value = float(k2p_value)
    species_1 = species_list[0]
    species_2 = species_list[1]
    if len(species_list) != 2:
        print(f" ERROR: this row has {len(species_list)} specimens, in other words: not 2 tuna specimens (as it should be!): \n {species_list} ")
    if species_1 == species_2:
        if species_1 in intrak2p_dict.keys():
            intrak2p_dict[species_1].append(k2p_value)
        else:
            intrak2p_dict[species_1] = [k2p_value]
    else: # if species 1 is not the same as species 2
        if species_1 in interk2p_dict.keys():
            interk2p_dict[species_1].append(k2p_value)
        else:
            interk2p_dict[species_1] = [k2p_value]

        if species_2 in interk2p_dict.keys():
            interk2p_dict[species_2].append(k2p_value)
        else:
            interk2p_dict[species_2] = [k2p_value]
    return



""" 
catching_introgression() finds occurences of potential introgression/ converging haplotypes between species
and prints out between which specimens this happened
"""
introgression_dict = {}
def catching_introgression(line,current_species_name_style,print_specimen_introgression):
    rowlist = line.split(",")
    species_1 = rowlist[0]
    species_2 = rowlist[1]
    if print_specimen_introgression == "y":
        print(f" !!!!!! {species_1} and {species_2} should get further examined, since they have 0 interspecies divergence. !!!!!! \n  ")
    species_string = str(rowlist[:-1])
    species_string = species_string.replace("[","").replace("]","").replace("'","")
    if current_species_name_style == "1":
        pattern = re.compile(r"[a-zA-Z]{1,}[' ']{1,}[a-zA-Z]{5,}")
        matchlist = pattern.findall(species_string)
        matchlist.sort()
        introgressioncouple_string = ""
        temp_counter = 0
        for el in matchlist:
            if temp_counter == 1:
                introgressioncouple_string += " & "
            introgressioncouple_string += el
            temp_counter += 1
        if introgressioncouple_string in introgression_dict.keys():
            introgression_dict[introgressioncouple_string].append(int(1))
        else:
            introgression_dict[introgressioncouple_string] = [int(1)]        
    elif current_species_name_style == "2":
        pattern = re.compile(r"[a-zA-Z]{1,2}['.'][a-zA-Z]{5,}")
        matchlist = pattern.findall(species_string)
        matchlist.sort()
        introgressioncouple_string = ""
        temp_counter = 0
        for el in matchlist:
            if temp_counter == 1:
                introgressioncouple_string += " & "
            introgressioncouple_string += el
            temp_counter += 1
        if introgressioncouple_string in introgression_dict.keys():
            introgression_dict[introgressioncouple_string].append(int(1))
        else:
            introgression_dict[introgressioncouple_string] = [int(1)]
    return 



""" 
barcode_gap_data_maker() takes the collected K2P-data and then creates the datapoints that will be used in the barcode gap plot 
and stores it in the dictionary barcode_gap_dict.
Key: species, value: maximum intraspecies & minimum interspecies divergence
"""
barcode_gap_dict = {}
def barcode_gap_data_maker():
    for key in interk2p_dict.keys():
        if key in intrak2p_dict.keys(): 
            max_intraspecies = max(intrak2p_dict[key]) # value on x-axis
            max_intraspecies *= 100 # percentage
            min_interspecies = min(interk2p_dict[key]) # value on y-axis
            min_interspecies *= 100 # percentage
            barcode_gap_dict[key] =[max_intraspecies,min_interspecies]
    return 



""" 
barcode_gap_plot_fun() plots the barcode gap plot, 
from the data stored in barcode_gap_dict
"""
def barcode_gap_plot_fun():        
    max_x = 0
    max_y = 0
    markerlist=["1","2","+","x","*","3","4","$¤$","$α$","$β$","$γ$","$δ$"] # List of markers used for distinguishing overlapping datapoints
    sorted_plot_list = sorted(barcode_gap_dict.items(),key=lambda x:x[1]) # A list gets created,where the elements are key-value tuples sorted after value. 
    prev_x = "none"
    prev_y = "none"
    marker_counter = 0
    point_counter = 0
    """
    Row 233-239: ¤¤¤ Parameters for DPI of the plot, legend location, legend size, markersize, axis tick size, axis size and title size is chosen here
    """
    dpi_plot = 200 # 1200 dpi is most commonly used for scientific papers. 
    legend_location = "best" # "upper center" is often a good option to use aswell
    legendsize = 20
    markersize = 90
    axis_ticksize = 20
    axis_size = 25
    title_size = 25

    print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    savepic = input('Want to save the plot? \n(y/n)\n').lower()
    if savepic == "y":
        fig,ax = plt.subplots(figsize=(19.20,10.80),dpi=dpi_plot) 
    else:
        fig,ax = plt.subplots() 
    
    print(f"\n ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ K2P-values used in the plot: ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
    for point in sorted_plot_list:
        point_counter += 1
        species = point[0]
        x = point[1][0]
        y = point[1][1]
        if prev_x == "none":
            prev_x = x
            prev_y = y
            plt.scatter(x,y,label=species, s=markersize)
        else:
            tolerance = 0.05
            if math.isclose(prev_x,x,abs_tol=tolerance) == True:    
                if math.isclose(prev_y,y,abs_tol=tolerance) == True:#To make overlapping points visible, random noise gets added (jitter), as well as a distinguishable marker from "markerlist" 
                    percentage = 3 / 100
                    jittered_x = x + ( percentage*np.random.rand() - percentage/2)
                    jittered_y = y + ( percentage*np.random.rand() - percentage/2)
                    plt.scatter(jittered_x,jittered_y,label=species,marker=markerlist[marker_counter],edgecolors=None,s=markersize)
                    marker_counter += 1
                else: 
                    if point_counter >= 11:
                        plt.scatter(x,y,label=species,marker="D",  s=markersize)
                    else:
                        plt.scatter(x,y,label=species,  s=markersize)
                    marker_counter = 0
                prev_x = x
                prev_y = y
            else:
                if point_counter >= 11:
                    plt.scatter(x,y,label=species,marker="D", s=markersize)
                else:
                    plt.scatter(x,y,label=species, s=markersize)
                marker_counter = 0
                prev_x = x
                prev_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        print(f"{species} has: Maximum Intraspecies Divergence: {x} \t Minimum interspecies divergence: {y} \t  ")
    print(f"¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ \n")
    plt.axline( (0,0), (max_x,max_x),color= "black")
    x_axis_max_value = np.ceil(max_x)
    x_interval = np.linspace(0,x_axis_max_value,6) # the values for the x-axis gets calculated
    plt.xticks(x_interval,fontsize = axis_ticksize)
    y_axis_max_value = np.ceil(max_y)
    y_interval = np.linspace(0,y_axis_max_value,6)
    if y_axis_max_value > x_axis_max_value: # scales the y-axis coordinate for the "barcode gap"-text after the rounded up maximum y-value
        plt.text(0,y_axis_max_value*0.96,'Barcode gap', size=20,color="Green",fontweight = 'bold',horizontalalignment = "left",verticalalignment="top")
        plt.text(x_axis_max_value,0,'No Barcode gap', size=20,color="red",fontweight = 'bold',horizontalalignment = "right",verticalalignment="bottom")
    else: # scales the y-axis coordinate for the "barcode gap"-text after the maximum height of the 1:1 ratio line
        plt.text(0,x_axis_max_value*0.96,'Barcode gap', size=20,color="Green",fontweight = 'bold',horizontalalignment = "left",verticalalignment="top")
        plt.text(x_axis_max_value,0,'No Barcode gap', size=20,color="red",fontweight = 'bold',horizontalalignment = "right",verticalalignment="bottom")
    plt.yticks(y_interval,fontsize = axis_ticksize)
    plt.text(max_x/2*0.85,max_x/2*1.15, s= "1:1 ratio",color="black", fontsize=20,fontweight = 'bold')
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    plt.title('Barcode gap -  ' + input(f"\nInsert the name of the barcode-candidate you study in {input_DistanceDATA_file}: \n"),fontsize = title_size, fontweight = 'bold')
    plt.xlabel('Max Intraspecies Divergence (%)',fontsize =axis_size,fontweight = 'bold')
    plt.ylabel('Min Interspecies Divergence (%)',fontsize =axis_size,fontweight = 'bold')
    plt.grid()
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    """
Row 314-319: ¤¤¤ If you want to be able to save the plot in the terminal and dont want to manually change the plot, 
make sure this block of code is uncommented
    """
    plt.legend(loc= legend_location, fontsize = legendsize)
    if savepic == 'y':
            # output_image = input('Name the image (will automatically be saved in .svg-format)\n')+".svg"
            output_image = input('Name the image (will automatically be saved in .png-format)\n')+".png" # uncomment this row if you want the plot to be saved in .png-format
            plt.savefig(output_image)
            print(f"\n  Done! The plot has now been saved as: {output_image}")
    """
Row 324: If you want to be able to drag the legend manually, while manually saving the plot, 
uncomment this row and comment row 314-319 
    """
    # plt.legend(loc= legend_location, fontsize = legendsize).set_draggable(state=True) # if you want to manually change the legend, uncomment this row
    plt.show()
    return



"""
main() is the main-function in the script, 
that calls all the functions so the barcode gap plot can be made in the end :)
"""
def main():  
    current_species_name_style = species_name_style_finder()
    """
Row 340-346: ¤¤¤ Collects info from the user if the user wants the specimens to be printed,
when potential introgression or identical haplotypes occures
    """
    print_specimen_introgression = ""
    while print_specimen_introgression == "":
        input_print_specimen_introgression = input(f"\nIf the script finds potential occurences of introgression / identical haplotypes between species;\nDo you want the 2 specimens involved to be printed out? (sequence id will then be included) \n *** Choose between: y (yes) or n (no) *** \n(y/n) \n").lower()
        if input_print_specimen_introgression == "y" or input_print_specimen_introgression == "n":
            print_specimen_introgression = input_print_specimen_introgression
        else:
            print(f" \n\n!!!!!!!!!!!!!!!!!! Error: {input_print_specimen_introgression} is not a valid option \n Choose between: (y/n) !!!!!!!!!!!!!!!!!!")
    print(f"\n \t\tPotential introgression / identical haplotypes between species:")
    """
Row 352-383: ¤¤¤ Collects k2p-data from the input-file and classifies the  
k2p-data as either inter or intra-species divergence
    """
    with open(input_DistanceDATA_file, 'r') as f: # the inputfile gets opened
        counter = 0
        for line in f:
            if counter == 0:
                counter += 1
                continue # if its the first line in the csvfile, then skip to the next row (next iteration)
            species_list = []
            if current_species_name_style == "1": 
                try:
                    species_list = find_species_long_species_name(line)
                    if len(species_list) < 2: # if row contains S.salar most likely
                        continue
                    k2p_value = k2p_value_finder(line)
                    inter_intra_k2p_sorter(species_list,k2p_value)
                    if species_list[0] != species_list[1]:
                        if k2p_value == 0:
                            catching_introgression(line,current_species_name_style,print_specimen_introgression)
                except:
                    raise SyntaxError(f"error occured at line: {line}. \n species 1 = {species_list[0]} \n species 2 = {species_list[1]}")
            elif current_species_name_style == "2": 
                try:
                    species_list = find_species_short_species_name(line)        
                    if len(species_list) < 2: # if row contains S.salar most likely
                        continue
                    k2p_value = k2p_value_finder(line) 
                    inter_intra_k2p_sorter(species_list,k2p_value)
                    if species_list[0] != species_list[1]:
                        if k2p_value == 0:
                            catching_introgression(line,current_species_name_style,print_specimen_introgression)
                except:
                    raise SyntaxError(f"error occured at line: {line}. \n species 1 = {species_list[0]} \n species 2 = {species_list[1]}")
            counter += 1
    barcode_gap_data_maker()
    """ 
Row 389-397: ¤¤¤ Prints information about the frequency of potential occurences of introgression / identical haplotypes between species, 
that has been spotted from the input-file.
    """ 
    key_list = []
    for key in introgression_dict.keys():
        key_list.append(key)
    key_list.sort() 
    introgression_count = 0
    for key in key_list:
        introgression_count += sum(introgression_dict[key])
        print(f" {key} showed {sum(introgression_dict[key])} occurences of potential introgression / identical haplotypes between eachother")
    print(f' \n !!!!!!!!!!! Out of {counter-1} k2p values, {introgression_count} showed signs of introgression / identical haplotypes !!!!!!!!!!! ')

    barcode_gap_plot_fun() # calling the function that does the barcode gap plot.



if __name__ == "__main__":
    main()






    







                                                                                                     