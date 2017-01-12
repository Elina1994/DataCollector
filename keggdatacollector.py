#!/usr/bin/env python3

"""
   Author: Elina Wever
   Email : e.e.wever@st.hanze.nl
   Date: 03-10-2016
   Purpose: Filter entry file and retrieve all pathways for each entry(organism)
   Version: 0.0.2

   Usage Command Line: python3 keggdatacollector.py  <filepath_to_file_with_organisms> <filepath_to_pathway_folder>

"""
import os
import sys
from urllib.request import urlopen


class ProcessEntryFile:
    """This class opens and filters an entry file and retrieves all pathways for each entry(organism)
       Input: Complete entry (text) file from KEGG
       Output: Individual files with pathway codes and organism codes
    """

    def __init__(self):
        """Constructor for ProcessEntryFile"""
        self.system_separator = os.sep
        self.path_to_organism_file = sys.argv[1]
        self.path_to_pathway_dir = ""
        self.filtered_list = []
        self.entry_dict = {}

    def determine_platform_and_set_path(self):
        """Determines if the platform is Windows or Linux based"""
        # Platform is Windows
        if os.name == "nt":
            self.path_to_pathway_dir = sys.argv[2] + self.system_separator
        else:
            self.path_to_pathway_dir = sys.argv[2] + self.system_separator
        return self.path_to_pathway_dir
        
    def create_folder(self):
        """Creates folder named Pathways"""

        if not os.path.exists(self.path_to_pathway_dir):
            os.mkdir(self.path_to_pathway_dir)
        return self.path_to_pathway_dir

    def filter_file(self):
        """Opens an entry text file and returns this for usage
           Input: Complete entry text file
           Output: Filtered dictionary with entries and organism name
        """
        print(self.path_to_pathway_dir)
        try:
            with open(self.path_to_organism_file) as unfiltered_file:
                for line in unfiltered_file:  # Filter plants and animals out of this file
                    if not line.__contains__("Animals") and not line.__contains__("Plants"):
                        self.filtered_list.append(line)

            for line in self.filtered_list:
                entries = line.split("\t")[1]
                organism = line.split("\t")[2]
                self.entry_dict[entries] = organism

            return self.entry_dict
        except FileNotFoundError as no_file :
            sys.exit("Given file or directory was not found.. please check if you provided the right path")

    def retrieve_files(self, entry_dictionary):
        """Splits entry_dict's keys in parts of max 100 and retrieves + saves all pathway files
           Input: Filtered list with only entries
           Output: List with all results
        """
        print("Start fetching files...")
        # Split list with entry in parts of 96 items per list (creates 44 lists with entries)
        entry_parts = [list(self.entry_dict.keys())[i:i + 96] for i in range(0, len(list(self.entry_dict.keys())), 96)]

        for partial_lists in entry_parts:
            for entry in partial_lists:
                pathway_files = self.path_to_pathway_dir + entry + ".txt"
                if os.path.isfile(pathway_files):  # Check if files already exist and skip if True
                    continue
                else:
                    url = "http://rest.kegg.jp/link/" + entry + "/pathway"  # Define url to retrieve data of
                    result = urlopen(url).read()
                    adapted_result = result.decode("utf-8")     # Convert result to usable format
                    if adapted_result.strip() == "":
                        print("The following entry was not saved because there was no content to display :", entry)
                        continue
                    else:

                        print("Retrieving following entry files: ", entry)
                        save_files = open(self.path_to_pathway_dir + entry + ".txt", "w")  # Write files to Pathway map
                        save_files.write(adapted_result)
                        save_files.close()
        print("Finished fetching files..")

if __name__ == "__main__":
    process = ProcessEntryFile()
    process.determine_platform_and_set_path()
    process.create_folder()
    entry_dictionary = process.filter_file()
    process.retrieve_files(entry_dictionary)

