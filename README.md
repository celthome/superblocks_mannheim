# NoiseModelling and Superblock Finder Analysis

This repository provides a detailed workflow for modeling traffic noise and accessibility in urban superblocks. Using open-source software and data, it evaluates noise propagation and POI accessibility, aimed at enhancing urban planning.

![Alt text](https://github.com/celthome/superblocks_mannheim/blob/544bd00927d87d3e104a5d541b9a95a0aa296420/figures/workflow.png "Workflow Overview")

Workflow Overview

1. Noise Modeling with NoiseModelling (NM)

We set up a local instance of NM following CNOSSOS-EU guidelines, which models sound propagation based on road type defaults. OpenStreetMap (OSM) data, sourced via BBBike.de, supports baseline noise level calculations.

2. Superblock Accessibility Assessment

POI accessibility within superblocks was analyzed using the 5-Minute City (FMC) approach. POIs (categories: Food, Commercial, Health, Education, Recreation) were extracted from OSM using Overpass API, processed for accessibility with OpenRouteService (ORS), and filtered for superblock compliance.

3. Superblock Finder and Suitability Analysis

We implemented Superblock Finder (SF) locally to identify suitable building blocks based on network and spatial criteria (e.g., street loop length, density). The Network Disruption Index (NDI) calculates minimal traffic impact.

4. Noise Re-Simulation for Superblocks

Using the adjusted road classifications, we simulated three noise scenarios within superblocks, comparing changes in area-specific noise levels (ΔLden) against baseline metrics.

Data Sources and APIs 
- POI Data: OSM, extracted via Overpass API 
- Accessibility Isochrones: OpenRouteService (ORS)
- Noise Propagation: NoiseModelling (NM)
- Population Data: WorldPop

For further setup instructions, refer to the individual GitHub repositories and their respective documentation:

- NoiseModelling: https://github.com/Universite-Gustave-Eiffel/NoiseModelling
- Superblock Finder: https://github.com/dymat/superblocks/tree/master
- OpenRouteService: https://github.com/GIScience/openrouteservice

Note: Full methodological details will be added soon.
