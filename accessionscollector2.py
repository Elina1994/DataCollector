"""
Author: Elina Wever
Email: e.e.wever@st.hanze.nl
Date: 22-09-2016
Purpose: Collecting and storing all available accession id´s for every micro-organism in a single list
Version: 0.0.1

NOTE: this class should eventually replace the current accessionscollector.py
"""

import accessionscollector
import glob


class CollectAllAccessions:
    """Collects all accesion id's from every single input file
    """

    def __init__(self):
        """Constructor for CollectAllAccessions """
        self.pathway = acc.pathway + "prokaryotes.txt"  # Use same path as in another class
        self.accession_list = []
        self.file_list = []

    def filter_file(self):
        """"Filters input files until only accession id's are left
            Input: Some .txt plus .ids files with a lot of information
            Output: A list with all accession id's from all processed files
        """
        to_be_filtered_list = []
        file_types = ("*.ids", "*.txt")
        txt_files_list = []
        ids_files_list = []

        for files in file_types:
            self.file_list.extend(glob.glob(acc.pathway + files))

        for names in self.file_list:

            with open(names, encoding="utf-8") as complete_files:  # Type utf-8 is needed to prevent an error during opening
                filename = str(complete_files.name)
                if filename.endswith(".txt"):
                    for lines in complete_files:
                        if lines.__contains__("Complete Genome"):
                            accessions = lines.split("\t")[9]   # Extract accessions from file
                            accessions = accessions.split(",")  # Adapt accessions
                            to_be_filtered_list.append(accessions)  # Add all accessions to list
                            txt_files_list = [i for sublist in to_be_filtered_list for i in sublist]  # Flatten list

                else:
                    for lines in complete_files:
                        if lines.__contains__("eukaryota"):  # Skip header
                            continue
                        else:
                            accessions = lines.split("\t")[4]
                            accessions = accessions.replace("-", "")  # Remove - sign to avoid Bad Request error
                            ids_files_list.append(accessions)  # Extract accession id from each line and save in a list

        self.accession_list = txt_files_list + ids_files_list
        return self.accession_list


if __name__ == "__main__":
    acc = accessionscollector.CollectAccessionIds()
    collect = CollectAllAccessions()
    collect.filter_file()
