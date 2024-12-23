# Instructions to Superblock Finder after Eggimann (2022)

The repository at https://github.com/dymat/superblocks/tree/master was cloned, and several files were modified to make the code run smoothly (e.g. Mannheim was added as a city). 
It was utilized to identify potential Superblocks for our project. 


First, the environment has to be set up using [this file](https://github.com/celthome/superblocks_mannheim/blob/main/conf/env.yml). 
The python scripts also require a postgres database with postgis installed (user: postgres; password: postgres; host: localhost; port: 5432; database: superblocks).

Then [preprocess_psm.py](https://github.com/celthome/superblocks_mannheim/blob/main/SF/superblocks-master/superblock_finder/preprocess_osm.py) can be run to download and preprocess the data for the area of interest.
After that, potential superblocks can be identified using [superblock.py](https://github.com/celthome/superblocks_mannheim/blob/main/SF/superblocks-master/superblock_finder/superblock.py).

The results can be extracted from the associated PostgreSQL database used by the script and visualized e.g. in QGIS.

