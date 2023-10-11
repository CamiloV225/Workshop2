# Workshop2 with Apache Airflow

In this workshop we will develope an ETL pipeline of airflow, that will allow us to use Apache Airflow to create a scalable and automated ETL pipeline for processing two datasets:

1.Spotify songs dataset: A collection of song data from Spotify, including track information, artist details, and audio features.
2.Grammy Awards nominated songs dataset: A list of songs that have been nominated for Grammy Awards, including categories and years.

By merging these datasets, you will be able to generate insightful plots and visualizations that can provide valuable information about the relationships between Grammy-nominated songs and their audio features from Spotify.

## Prerequisites
Before you get started with this workshop, make sure you have the following prerequisites:

- Apache Airflow installed.
- Python 3.10 and required dependencies
- Libraries like MySQL, pandas and others.
- Basic knowledge of ETL concepts.

 ## Workflow Overview
 The workflow for this project involves the following steps:

Extract data from Spotify and Grammy Awards sources.
Transform and clean the data to prepare it for analysis.
Load the transformed data into a database or data store.
Generate meaningful plots and visualizations from the merged data.
