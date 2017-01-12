#!/usr/bin/env python3


"""
Author: Elina Wever
Email: e.e.wever@st.hanze.nl
Date: 20-09-2016
Purpose: Collecting and storing all complete genomes of every single micro-organism
Version: 0.0.2

Usage Command Line : python3 ncbi_datacollector.py <name/of/directory/foldername/>

NOTE: accessionscollector.py needs to be stored in the same folder as ncbi_datacollector.py !
"""

from Bio import Entrez
import os
import re
import sys
from urllib.error import URLError
import accessionscollector


class CollectCompleteGenomes:
    """This class collects all complete genomes from NCBI for each micro-organism
     and stores them in different folders"""

    def __init__(self, record_files):
        """Constructor of class CollectCompleteGenomes"""
        self.path_separator = os.sep    # Get system specific path_to_pathway_dir separator
        self.pathway = ""
        self.folder_list = []   # List to store folder names for each species
        self.filename = ""      # Defines the filename for each record
        self.record_files = record_files
        self.fetch_files = ""


    def determine_platform_and_set_path(self):
        """Determines if the platform is Windows or Linux based"""
        # Platform is Windows
        if os.name == "nt":
            self.pathway = sys.argv[1] + self.path_separator
        else:
            self.pathway = sys.argv[1] + self.path_separator
        return self.pathway

    def create_folders(self):
        """Creates a folder for every species to collect.
           Input:  path_to_pathway_dir to directory to save
           Output: 4 different folders for each species in the created Genomes directory
        """

        self.folder_list = ["Bacteria", "Archaea", "Eukaryota", "Viruses", "Viroids"]  # Define all folder names

        for item in self.pathway:
            if not os.path.exists(self.pathway):  # Create folder Genomes if not already existing
                os.mkdir(self.pathway)

        for folder in self.folder_list:  # Loop through all objects in list and save each individual as a folder
            if not os.path.exists(self.pathway+folder):  # check if folders already exist and create them if not
                os.mkdir(self.pathway+folder)            # create folder for every species
        return self.folder_list

    def collect_genomes(self, folders):
        """ Collects every complete genome from every micro-organism. Also checks if some genbank files already exist
            if they exist the won't be collected again. If they do not exist they will be collected

           Input: List of all accession id's
           Output: All complete genomes per species
        """
        print("Starting program and checking for updates (this may take a while) ...")
        restart_program = True
        count_restarts = 0   # Count total amount of restarts to make it limited
        while restart_program:  # Restart program if crash due an external error has been encountered
            try:
                while True and count_restarts < 35:
                    restart_program = False    # Do not restart when no error is encountered
                    Entrez.email = "elinastellark@gmail.com"         # Tell NCBI who you are
                    found_accessions = []    # List for existing accession id's
                    missing_accessions = []  # List for non existing accession id's
                    accession_ids = acc.accession_list

                    for folders in folder_list:
                        self.folders = folders   # Extract folder names from list
                        for accession in accession_ids:                # Extract accessions from each list
                            complete_path = self.pathway + self.folders + self.path_separator + accession + ".gb"
                            if os.path.isfile(complete_path):       # Check which files already are available
                                found_accessions.append(accession)  # Add accessions that already exist to list

                    for target in accession_ids:        # Loop through list of all accession id's
                        if target in found_accessions:  # If accession id exists skip this id
                            continue
                        else:
                            missing_accessions.append(target)   # If accession id does not exist add to list
                            parts = [missing_accessions[i:i + 1] for i in range(0, len(missing_accessions), 1)]
                            for partial_list in parts:
                                
                                # Convert list of accessions to usable input for Entrez.fetch
                                convert_accession_ids = ",".join(partial_list)
                                self.fetch_files = Entrez.efetch(db="nucleotide", id=convert_accession_ids,
                                                                             rettype="gb", retmode="text")
                            collect.save_genbank_file(self.fetch_files)
                            print("Saved genbank file")
                            self.fetch_files.close()
                    print("Program finished....")
                    return self.fetch_files

            except URLError as an_error:
                restart_program = True
                count_restarts += 1
                print("Processes interrupted because of: ", an_error.reason)
                print("Restarting program and continuing process..")

    def save_genbank_file(self, genbank_files):
        """ Writes all collected genbank files to the right folder
            Input: Set of genbank files
            Output: Separated genbank files in different folders
        """

        genbank_files = self.fetch_files  # Assign new value to retrieved genbank files
        genbank_record = []               # Create list to store genbank lines in
        genbank_line = ""

        for line in genbank_files:             # Read content of each genbank file
            genbank_line += line
            if line.startswith("Accession".upper()):
                split_line = line.split("   ")[1].strip("\n")
                self.filename = split_line.split(" ")[0]
            if line.startswith('//'):          # Split file in multiple files if line starts with "//"
                genbank_record.append(genbank_line)
                genbank_line = ""

        for record in genbank_record:
            search_area = record.strip("\n")
            for rank in self.folder_list:          # Rank contains: Bacteria,Archaea, Viruses, Viroids and Eukaryota
                search_organism = re.search(rank+";", search_area) or re.search(rank+"\.", search_area)  # Search for organism name in file
                if search_organism:                             # If any match is found continue and save records
                    match = search_organism.group(0).strip(";")
                    determined_organism = match.strip(".")
                    if rank.upper() == determined_organism.upper():       # Check if folder name equals rank name
                        self.record_files = open(self.pathway + rank + "/" + self.filename + ".gb", "w")
                        self.record_files.write(record.strip())  # Write information to file and remove first newline
                        self.record_files.close()
        return self.record_files

if __name__ == "__main__":
    print(__doc__)
    collect = CollectCompleteGenomes("")
    collect.determine_platform_and_set_path()
    acc = accessionscollector.CollectAccessionIds()
    acc.collect_ids()
    folder_list = collect.create_folders()
    fetch_files = collect.collect_genomes(folder_list)
