"""
Author: Elina Wever
Email: e.e.wever@st.hanze.nl
Date: 22-09-2016
Purpose: Collecting and storing all available accession id´s for every micro-organism in a single list
Version: 0.0.1

NOTE: this class should eventually replace the current accessionscollector.py
"""

import accessionscollector


class CollectAllAccessions:
    """Collects all accesion id's from all complete genomes
    """

    def __init__(self):
        """Constructor for CollectAllAccessions """
        self.pathway = acc.pathway + "prokaryotes.txt"  # Use same path as in another class
        self.accession_list = []

    def filter_file(self):
        """"Filters input files until only accession id's are left
            Input: Some .txt files with a lot of information
            Output: A list with all accession id's from every complete genome
        """
        to_be_filtered_list = []

        with open(self.pathway, encoding="utf-8") as complete_files:  # Type utf-8 is needed to prevent an error during opening
            for lines in complete_files:
                if lines.__contains__("Complete Genome"):
                    accessions = lines.split("\t")[9]   # Extract accessions from file
                    accessions = accessions.split(",")  # Adapt accessions
                    to_be_filtered_list.append(accessions)  # Add all accessions to list
                    self.accession_list = [i for sublist in to_be_filtered_list for i in sublist]  # Flatten list
            print(self.accession_list)
            return self.accession_list

if __name__ == "__main__":
    acc = accessionscollector.CollectAccessionIds()
    collect = CollectAllAccessions()
    collect.filter_file()
