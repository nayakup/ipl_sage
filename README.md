# IPL RAG Chatbot

The IPL RAG Chatbot is a Retrieval-Augmented Generation (RAG) chatbot designed to answer queries related to the Indian Premier League (IPL). It uses ball-by-ball IPL data stored in CSV files and provides context from the CSV schema. The chatbot leverages DuckDB to execute dynamically generated queries, allowing you to extract insights from a DuckDB database where the CSVs are preprocessed and loaded.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Usage](#usage)
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

## Usage

# How to Use IPL Sage (The IPL Data Analysis Assistant)

Welcome to **IPL Sage**! This assistant helps you analyze IPL cricket data and generates DuckDB queries for your questions. Here’s how to get started:

## 🏏 What Can You Ask?

You can ask any question related to IPL statistics, such as:
- "Who has taken the most wickets in the 2025 season?"
- "Which team has the best bowling economy rate for the 2025 season?"
- "Which player has the highest number of sixes in the tournament?"

## 🚀 How to Interact

1. **Start the Bot:**  
   Run the assistant from your terminal using:

   uv run -m main

(Make sure you are in the project root directory.)

2. **Ask Your Question:**  
Type your IPL-related question at the prompt and press Enter.

3. **View the Output:**  
The bot will display:
- The reasoning behind the generated DuckDB query.
- The actual DuckDB query you can use.
- (If applicable) The results of the query in a table.

## 💡 Tips

- Be as specific as possible in your questions for best results.
- If you want to understand how a query was generated, ask for the reasoning.
- You can use the example questions shown at startup to get started.

---

Enjoy exploring IPL data with IPL Sage!
