# IPL RAG Chatbot

The IPL RAG Chatbot is a Retrieval-Augmented Generation (RAG) chatbot designed to answer queries related to the Indian Premier League (IPL). It uses ball-by-ball IPL data stored in CSV files and provides context from the CSV schema. The chatbot leverages DuckDB to execute dynamically generated queries, allowing you to extract insights from a DuckDB database where the CSVs are preprocessed and loaded.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Overview

This project builds a chatbot that:
- Receives user queries about IPL data.
- Uses a custom agent to generate a DuckDB query based on the CSV schema.
- Executes the query on a DuckDB database populated with IPL ball-by-ball data.
- Returns the query result to answer the user’s inquiry.

## Architecture

Key components of the system include:

- **Query Agent:** Implements the RAG logic to convert user queries into executable DuckDB queries. The agent is built using a base agent class and a dedicated prompt generator with context providers.
- **Context Provider:** Supplies schema and sample data from the CSV files, aiding the query generation process.
- **Preprocessor:** Loads IPL CSV files into a DuckDB database and generates a human-readable schema description.
- **DuckDB Integration:** Executes the generated queries on a DuckDB database (configured via `config.py`), returning results as a Pandas DataFrame.

## Features

- **Dynamic Query Generation:** Translates natural language IPL queries into executable DuckDB SQL.
- **CSV Preprocessing:** Automates loading and schema generation from IPL ball-by-ball CSV data.
- **Contextual Assistance:** Provides detailed context to the query agent through the CSV file schema.
- **Logging & Error Handling:** Uses RichHandler for enhanced logging and error alerts.
- **Modular Structure:** Separates configuration, preprocessing, querying, and context providing into dedicated scripts.

## Setup and Installation

1. **Clone the Repository:**
```bash
   git clone <repository-url>
   cd <project-directory>
