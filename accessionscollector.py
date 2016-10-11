#!/usr/bin/env python3


"""
Author: Elina Wever
Email: e.e.wever@st.hanze.nl
Date: 22-09-2016
Purpose: Collecting and storing all available accession id´s for every micro-organism in a single list
Version: 0.0.1
"""
import os
import glob
import fileinput


class CollectAccessionIds:
    """This class reads different .ids files and extracts plus returns a list of all accession id's """

    def __init__(self):
        """"Constructor for CollectAccessionIds class"""
        self.accession_list = []      # Create list to store all accessions
        self.path_separator = os.sep  # Get system specific path separator
        self.pathway = "//172.16.6.53{0}StageStorage{0}voorbeelddata{0}ncbi_genomes{0}".format(self.path_separator)
        self.file_list = []           # Create list to store file names
        self.accession_list = []

    def collect_ids(self):
        """ This method reads multiple files and extracts all accession id's
            Input: .ids/.txt files
            Output: A list of all accession id's
        """

        self.file_list = glob.glob(self.pathway+"*.ids")      # Get all folders ending with .ids or .txt (using glob module)

        for lines in fileinput.input(self.file_list):         # Iterate over multiple file lines from different files
            if lines.__contains__("eukaryota"):               # Skip header
                continue
            else:
                accessions = lines.split("\t")[4]
                self.accession_list.append(accessions)  # Extract accession id from each line and save in a list
        return self.accession_list                            # Return list with accession id's
