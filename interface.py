import os        #import os to let us use bash
import pandas as pd         #import pandas to read our blasted files
import glob             #import glob to read files
import ftplib       #import ftp library to connect on the web

import tkinter as tk    #import Tkinter for interface
from tkinter import *
from tkinter import ttk

#import the other file for the function launch
from RBH import *
from alignment import *
from super_alignment import *
from cluster_function import *
#__________________

def select_proteome():        #function to select proteomes for blast
    """
    Argument:[none]
    Return : the list of proteomes (file.faa) to blast
    Author: DUPLAN Alexandre
    """
    #empty list of file.faa to blast
    faa_files_selected=[]

    #for each checkbutton
    for name, checkbutton in organism_dico.items():

        #if checkbutton (of a proteomes) is checked
        if checkbutton.var.get()==1:

            #and if the proteomes is not in the list to be blast
            if checkbutton['text'] not in faa_files_selected:

                #append the proteomes in the list
                faa_files_selected.append(checkbutton['text'])

        #if the checkbutton is unchecked
        if checkbutton.var.get()==0:

            #and if the proteomes is in the list to be blast (but you don't want it)
            if checkbutton['text'] in faa_files_selected:

                #remove the proteomes from the selection
                faa_files_selected.remove(checkbutton['text'])

    # list of file.faa to blast
    return faa_files_selected

def launch():
    """
    Arguments: None
    Result: Created a folder of clusters, aligned clusters, a super-alignment file and display the phylogenetic tree
    Author: Alexandre Duplan and Leonardo Mirandola
    """

    #select proteomes from tkinter interface
    proteomes = select_proteome()

    #create Databases for each proteomes selected
    RBH_DB_creator(proteomes)

    #Returns all non redondant combinations for each proteomes selected to have a RBH
    multi_RBH(*proteomes)

    #remove redundance between cluster SP and cluster AC
    cluster_AC_nr, cluster_SP_nr = cluster_species_redundance_remover(RBH_analysor(RBH_comparator()), cluster_species_finder(RBH_analysor(RBH_comparator())))

    #create a folder of the aligned cluster using MAFFT
    cluster_alignment(cluster_AC_nr,cluster_SP_nr)

    #In the aligned clusters folder add the missing proteomes with gaps
    gap_filer(proteomes)

    #start the creation of the super_alignment file and phylogenetic tree
    cluster_reader(proteomes)

    #remove all Databases created for each proteomes selected
    RBH_DB_remover(proteomes)

#_____Tkinter_____________
#creation of the window
window = Tk()

# creation of tab system
tab_system = ttk.Notebook(window)

#call the tab system
tab_system.pack()

#add the first tab
tab1 = ttk.Frame(tab_system)
tab1.pack()

# name of the first tab
tab_system.add(tab1, text='launch')

# add the second tab
tab2 = ttk.Frame(tab_system)
tab2.pack()

# name of the second tab
tab_system.add(tab2, text='add genome')

#label in the first tab
label = Label( tab1, text='CHOOSE YOUR GENOMES', relief=RAISED )
label.pack()

#list of checkbutton already existing, we don't want to add 2 times the same Checkbutton
list_already=[]

#dictionary of all the checkbuttons (key:proteomes.faa; value:checkbutton)
organism_dico = dict()

#function to create checkbutton on the first tab
def list_file_faa():
    """
    Argument: [None] but get all proteomes from the current directory (thank's to the function "proteome_file_finder")
    Result: create all checkbuttons to select proteomes for the blast
    Author: DUPLAN Alexandre
    """

    #for all value in proteome_file_finder (all proteomes => all file.faa find by proteome_file_finder)
    for i, value in enumerate(proteome_file_finder()):

        #if the checkbutton doesn't already exist
        if value not in list_already:

            #create the checkbutton
            organism_dico[value] = Checkbutton(tab1, text=value, onvalue=True, offvalue=False, command=select_proteome)

            #the value of checkbutton [unchecked;checked] is [0;1] and is initialised at 0
            organism_dico[value].var = BooleanVar(tab1, value=False)
            organism_dico[value]['variable'] = organism_dico[value].var

            #call the checkbutton created
            organism_dico[value].pack(padx=100, pady=1)

            #append the proteomes name in list_already to not create this checkbutton two times (with the "Refresh" Button)
            list_already.append(value)

#creation of buttons in first tab:

#create the button to launch the blast between the selected proteomes
boutonLaunch = Button(tab1, text = 'Launch', command = launch)
boutonLaunch.pack(padx=100, pady=10)#call the button "launch"

#create the button to refresh, if you add proteomes with get_seq function in tab_2 and you want to see the checkbutton of this new proteomes to put it in the list, to blast
boutonRefresh = Button(tab1, text = "Refresh", command = list_file_faa)
boutonRefresh.pack() #call the button refresh

#button to close the tkinter window
BoutonQuit_tab1 = Button(tab1, text = 'Quit', command = window.destroy)
BoutonQuit_tab1.pack(padx=100, pady=10)     #call the button quit

#call all checkbuttons to see the list of proteomes to be selected for the blast
list_file_faa()

#option_1_:__ADD_Genome_From_The_Web
FTP_HOST = "ftp.ncbi.nlm.nih.gov"   #FTP connect to ncbi
FTP_USER = "anonymous"
FTP_PASS = ""

# initialize FTP session
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

# force UTF-8 encoding
ftp.encoding = "utf-8"

# print the welcome message of NCBI
print(ftp.getwelcome())

# change the current working directory to refseq
ftp.cwd('genomes/refseq/')

# directory of bacteria_________________________________________________________
# change the current working directory to bacteria
ftp.cwd('bacteria/')
print("*"*50, "addition of the list of bacteria from refseq", "*"*50)

#append all lines from ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria in a list named data_bac
data_bac = []
ftp.dir(data_bac.append)

#creation of name list of bacteria
organism_bac=[]#empty list

#for each line in the list data_bac (directory refseq/bacteria)
for line in data_bac:

    #separate lines by spaces
    organism_line_bac=line.split(' ')

    #append the organism name in the list organism_bac
    organism_bac.append(str(organism_line_bac[-1]))

# return to directory of refseq
ftp.cwd('..')

# directory of archae___________________________________________________________
# change the current working directory to archaea
ftp.cwd('archaea/')
print("*"*50, "addition of the list of archaea from refseq", "*"*50)

#append all lines from ftp.ncbi.nlm.nih.gov/genomes/refseq/archae in a list named data_archaea
data_archaea = []
ftp.dir(data_archaea.append)

#creation of name list of archaea
organism_arc=[]#empty list

#for each line in the list data_archaea (directory refseq/archaea)
for line in data_archaea:

    #separate lines by spaces
    organism_line_arc=line.split(' ')

    #append the organism name in the list organism_arc
    organism_arc.append(str(organism_line_arc[-1]))

# return to directory of refseq
ftp.cwd('..')

# directory of vertebrate_mammalian_____________________________________________
# change the current working directory to vertebrate_mammalian
ftp.cwd('vertebrate_mammalian/')
print("*"*50, "addition of the list of vertebrate_mammalian from refseq", "*"*50)

#append all lines from ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian in a list named data_vertebrate_mammalian
data_vertebrate_mammalian = []
ftp.dir(data_vertebrate_mammalian.append)

#creation of name list of vertebrate_mammalian
organism_vertebrate_mammalian=[]

#for each line in the list data_vertebrate_mammalian (directory refseq/vertebrate_mammalian)
for line in data_vertebrate_mammalian:

    #separate lines by spaces
    organism_line_vertebrate_mammalian=line.split(' ')

    #append the organism name in the list organism_vertebrate_mammalian
    organism_vertebrate_mammalian.append(str(organism_line_vertebrate_mammalian[-1]))

ftp.cwd('..')# return to directory of refseq

#Function changes the current directory, choose the name of the organism and his taxon to download his sequence
def directory_choice():
    """
    Argument: [None] but get the sequences name input by the user and split it in 2
    Result: the name of the organism selected and his taxon
    Author: DUPLAN Alexandre
    """
    #get the entry input by the USER
    valeur_temp = entry_organism.get()# (example = "bac:salmonella_bongori")

    #split the value to get the tax id and the organism name (ex: "bac"+"salmonella_bongori")
    valeur = valeur_temp.split(":", 1)

    #the word after ":" is used to change the name of the organism selected
    global organism_selected
    organism_selected=valeur[-1]

    #the word before ":" is used to change the taxon
    tax_id=valeur[0]
    global taxon

    #the word before ":" is used to change the label text, the directory and the taxon name
    if (tax_id == 'bac'):
        l.config(text='Bacteria selected ')
        ftp.cwd('bacteria/')
        taxon='bacteria'

    elif (tax_id == 've_m'):
        l.config(text='vertebrate_mammalian selected')
        ftp.cwd('vertebrate_mammalian/')
        taxon='vertebrate_mammalian'

    else:
        l.config(text='archae selected')
        ftp.cwd('archaea/')
        taxon='archaea'

#function to find and download the protein.faa from refseq
accession_data=[] #empty list to append the accession code
def get_seq():
    """
    Argument: [None] but get the name of the organism selected and his taxon
    Result: download the sequence
    Author: DUPLAN Alexandre
    """
    #changes the current directory, choose the name of the organism and his taxon
    directory_choice()

    #display the selected organism name to the USER
    labelRes.configure(text=" Organism name : " + str(organism_selected))

    #with the function directory_choice, we are now in the current directory (bacteria, archaea or vertebrate_mammalian) to download the organism
    #so we change the directory to go in the directory of our organism and in the all version of his proteomes sequenced
    cwd_dir=str(organism_selected)+'/all_assembly_versions/'
    print(ftp.cwd(cwd_dir))

    #find the accession code (in the directory "all_assembly_versions", there is only one directory and his name is the accession code of our organism)
    print(ftp.dir(accession_data.append))

    #get the accession code from the only one line in accession_data
    str_data="".join(accession_data)
    accession=str_data.split('/')[-1]

    #command os.system to get the sequence of our organism target
    os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/"+taxon+"/"+organism_selected+"/all_assembly_versions/"+accession+"/"+accession+"_protein.faa.gz ")

    #the sequence downloaded is a compressed file, so we gunzip this file
    os.system("gunzip "+accession+"_protein.faa.gz ")

    #rename the file with the organism name
    os.system("mv "+accession+"_protein.faa "+(organism_selected.replace("_", "-"))+"-protein.faa")

    # get out from the directory, go back to /genomes/refseq/
    print(ftp.cwd('..'))
    print(ftp.cwd('..'))
    print(ftp.cwd('..'))


# creation of a text field
labelnote = Label(tab2, text="note: please CTRL+C/CTRL+V a line from the list to download \n \n to search :")
labelRes = Label(tab2, text = " waiting")

# creation of an input field in the first tab
value_organism = StringVar()
entry_organism = Entry(tab2, textvariable= value_organism, width =30)

# creation of the download and quit buttons in the second tab
boutonResearch = Button(tab2, text = "download", command = get_seq)
boutonQuitter = Button(tab2, text = " Quit", command = window.quit)

#label that displays the tax_id => ex: bacteria is selected
l = Label(tab2, bg='white', width=20, text='empty')

# display of created objects
l.pack()
labelRes.pack()
entry_organism.pack()
boutonResearch.pack()
boutonQuitter.pack()
labelnote.pack()

#boxlist of all selectable organism
class Organism_refseq(Frame):

    #in class, we need to create function init
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    # Create main GUI window
    def create_widgets(self):
        """
        Arguments: [none]
        Result: create the listbox
        Author: DUPLAN Alexandre
        """

        #variable of our entry is a string
        self.search_var = StringVar()

        #Indicate the function (update_list) to execute each time the value of search_var is modified
        self.search_var.trace("w", self.update_list)

        #create the field to search in the second tab
        self.entry = Entry(tab2, textvariable=self.search_var, width=30)

        #create the listbox in the second tab
        self.lbox = Listbox(tab2, width=45, height=15)

        #call the field and the listbox created
        self.entry.pack(padx=100, pady=1)
        self.lbox.pack(padx=100, pady=1)

    # Function for updating the list/doing the search.
    # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self, *args):
        """
        Arguments: [none] or the term write by the USER (search_var)
        Result: adds all organisms (bacteria, archaea and vertebrate_mammalian) get on NCBI in the listbox, according to the word input by the USER
        Author: DUPLAN Alexandre
        """
        #get the variable i the field (the word input by the USER)
        search_term = self.search_var.get()

        # lbox_list to populate the listbox (lbox)
        lbox_list = []

        #append each words of organism_bac in lbox_list
        organism_bac_head = ["bac:" + item for item in organism_bac]
        lbox_list.extend(organism_bac_head)

        #append each words of organism_arc in lbox_list
        organism_arc_head = ["arc:" + item for item in organism_arc]
        lbox_list.extend(organism_arc_head)

        #append each words of organism_vertebrate_mammalian in lbox_list
        organism_vertebrate_mammalian_head = ["ve_m:" + item for item in organism_vertebrate_mammalian]
        lbox_list.extend(organism_vertebrate_mammalian_head)

        #delete words from the lbox
        self.lbox.delete(0, END)

        #Input all organisms name from the list (lbox_list) in the listbox (lbox) when nothing it's write in search_term
        #When a word is written in the search_term, the loop adds only the term that contains the word in search term
        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)



Organism_refseq() #call the class

window.mainloop() #call the window Tkinter
