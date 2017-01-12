# DataCollector

This README describes the usage and purpose of different written modules.

This package contains different .py files with different functions. These are:
 * ncbi_datacollector
 * keggdatacollector
 * accessionscollector
 
 ## NCBI Data Collector
 
 The ncbi_datacollector module retrieves all complete genomes of every single micro-organism. It's input is a set of accession id's which 
 are generated by the accessionscollector.py. This collector generates folders for each rank (Bacteria,Archaea,Eukaryota,Viruses and Viroids). It retrieves all complete genomes and saves them in the right folder. This retrieval of data is very time consuming.
 
 * How do I set up ?
   The only installation needed to succesfully run this program is Biopython(1.68) and Python(3.5).
   
 * Error handling
   Most of the errors occuring are caught by this data collector module. One of the most common errors are caused by NCBI's servers. It    often occures that this script loses connection with NCBI. If this happens the program will notify you and automatically restarts and    resumes the data retrieval.
   
 ## KEGG Data Collector
 
 The keggdatacollector module retrieves all available pathway files of each organism based on a single entry code. An example of an 
 entry code is "pan". These entry codes are extracted from a file downloaded of the following link: http://rest.kegg.jp/list/organism .
 The retrieved files with all pathways known for each organism are saved as a text file.
 
 * How do I set up ? 
   Installation of Python(3.5) only is enough to run this program
   
 ## Accessions Collector
 
 The accessionscollector collects all accession id's of different NCBI files and puts them in a single list. This list is used by the
 ncbi_datacollector module to retrieve genbankfiles from NCBI.The files that are used to extract accession numbers are available at:  ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/ (prokaryotes.txt). and at : ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/IDS/    (Bacteria.ids, Archaea.ids, Eukaryota.ids, Viruses.ids, Viroids.ids).
 
 * Limitations
   You are only able to use the text files mentioned above. The other text files available at the link will cause errors within the        script. It is also unnecessary to save other files than mentioned because these do not contain valueable data.
 
 
