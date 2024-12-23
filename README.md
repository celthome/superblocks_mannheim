# NoiseModelling and Superblock Finder Analysis

This repository provides a detailed workflow for modeling traffic noise and accessibility in urban superblocks. Using open-source software and data, it evaluates noise propagation and POI accessibility, aimed at enhancing urban planning. 
Each step of the workflow is described in detail in dedicated folders (NM, ORS, SF) within this repository to facilitate reproduction.
Instructions for setting up the Python environment are provided [here](https://github.com/celthome/superblocks_mannheim/blob/main/conf/env.yml).
## Workflow

#### 1. Noise Modelling ([NM](https://github.com/celthome/superblocks_mannheim/tree/main/NM))
First, we set up a local instance of NM following CNOSSOS-EU guidelines, which models sound propagation based on road type defaults. OpenStreetMap (OSM) data, sourced via BBBike.de, supports baseline noise level calculations. 

#### 2. Superblock Accessibility Assessment ([ORS](https://github.com/celthome/superblocks_mannheim/tree/main/ORS))
POI accessibility within superblocks was analyzed using the 5-Minute City (FMC) approach. POIs (categories: Food, Commercial, Health, Education, Recreation) were extracted from OSM using Overpass API, processed for accessibility with OpenRouteService (ORS), and filtered for superblock compliance.

#### 3. Superblock Finder ([SF](https://github.com/celthome/superblocks_mannheim/tree/main/SF))
We implemented the SF locally to identify suitable building blocks based on network and spatial criteria (e.g., street loop length, density). The Network Disruption Index (NDI) calculates minimal traffic impact.

#### 4. Noise Simulation for Superblocks ([NM](https://github.com/celthome/superblocks_mannheim/tree/main/NM))
Using the adjusted road classifications and NM, we simulated three noise scenarios within superblocks, comparing changes in area-specific noise levels (ΔLden) against baseline metrics.


## Project Overview:
<img src="figures/workflow.png" alt="workflow_overview" width="700">


## Results 

#### Noise Simulation:

<img src="https://github.com/user-attachments/assets/4ca68693-941b-4605-912a-69cdb2293458" alt="simulation" width="700">
<br>

#### Noise level changes (ΔLden):

<<<<<<< HEAD
<img src="https://github.com/user-attachments/assets/77c06379-1954-4b14-8d82-70673cea5683" alt="db_delta" width="500">
<br>
=======
<img src="figures/db_delta.jpeg" alt="db_delta" width="500">
<br><br>
>>>>>>> 481c1d8b2e8bdc876fef48cfa0bd5b12e7ac8d63

#### Data Sources and APIs 
- POI Data: OSM, extracted via Overpass API 
- Accessibility Isochrones: OpenRouteService (ORS)
- Noise Propagation: NoiseModelling (NM)
- Population Data: WorldPop

For further setup instructions, refer to the individual GitHub repositories and their respective documentation:

- NoiseModelling: https://github.com/Universite-Gustave-Eiffel/NoiseModelling
- OpenRouteService: https://github.com/GIScience/openrouteservice
- Superblock Finder: https://github.com/dymat/superblocks/tree/master

Note: Full methodological details will be added soon.
