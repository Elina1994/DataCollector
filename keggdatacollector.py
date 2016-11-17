#!/usr/bin/env python3

"""
   Author: Elina Wever
   Email : e.e.wever@st.hanze.nl
   Date: 03-10-2016
   Purpose: Filter entry file and retrieve all pathways for each entry(organism)
   Version: 0.0.1

"""
import os
from urllib.request import urlopen


class ProcessEntryFile:
    """This class opens and filters an entry file and retrieves all pathways for each entry(organism)
       Input: Complete entry (text) file from KEGG
       Output: Individual files with pathway codes and organism codes
    """

    def __init__(self):
        """Constructor for ProcessEntryFile"""
        self.separator = os.sep
        self.path_to_organism_file = '//172.16.6.53{0}StageStorage{0}PathwayViewer{0}Datasets{0}Kegg{0}KeggOrganisms_20161117.kegg'.format(self.separator)
        self.path = '//172.16.6.53{0}StageStorage{0}Pathways{0}'.format(self.separator)
        self.filtered_list = []
        self.entry_dict = {}

    def create_folder(self):
        """Creates folder named Pathways"""

        if not os.path.exists(self.path):
            os.mkdir(self.path)
        return self.path

    def filter_file(self):
        """Opens an entry text file and returns this for usage
           Input: Complete entry text file
           Output: Filtered dictionary with entries and organism name
        """

        with open(self.path_to_organism_file) as unfiltered_file:
            for line in unfiltered_file:  # Filter plants and animals out of this file
                if not line.__contains__("Animals") and not line.__contains__("Plants"):
                    self.filtered_list.append(line)

        for line in self.filtered_list:
            entries = line.split("\t")[1]
            organism = line.split("\t")[2]
            self.entry_dict[entries] = organism

        return self.entry_dict

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
                pathway_files = self.path + entry + ".txt"
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
                        save_files = open(self.path + entry + ".txt", "w")  # Write files to Pathway map
                        save_files.write(adapted_result)
                        save_files.close()
        print("Finished fetching files..")

if __name__ == "__main__":
    process = ProcessEntryFile()
    process.create_folder()
    entry_dictionary = process.filter_file()
    process.retrieve_files(entry_dictionary)

