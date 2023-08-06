Builds E.coli model with DNA, free and bound transcription factors data file for lammps mimicing real bp density of E.coli

atom type = angle

6 types of atoms represents
    1 = DNA monomer
    2 = DNA monomer specific sites
    3 = free transcription factors binding sites
    4 = bound transcription factor binding sites
    5 = stem point for transcription factors no affinity to "2"
    6 = cell membrane molecules

buindNwrite module:
uses all other modules 
to read previously collapsed DNA data file via position module and creates a membrane around it using membrane module
it also creates free transcription factors in given microMolarite via freeTF module within the parameters which are found by using radius thus preserving the bp density of E.coli
angler and bonder are there to create necessary bonds and angles
it doesn't return anything just creates a data file 
it takes 3 parameters
1 = um of free transcription factors
2 = data file to read
3 = name of the data file to create then write everything.