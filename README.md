# nlptask1-

# NLP Web Application

## Overview

This repository contains the source code for a simple Natural Language Processing (NLP) web application built with Spring Boot and Thymeleaf. The application allows users to input text, processes it to calculate NLP statistics, and displays the results.

## Features

- **Web Scraping:** The application includes a web scraper written in Python to gather health-related content from a specified website.

- **NLP Statistics Calculation:** NLP statistics, such as the number of sentences, words, average word length, lexical diversity, common words, percentage of stop words, and noun count, are calculated for the input text.

- **Web Application:** The Java-based Spring Boot application provides a user interface for users to input text, submit the form, and view the calculated NLP statistics.

## Project Structure

The project is organized as follows:

- `python_scraper/`: Contains the Python script for web scraping.

- `nlp-web-app/`: The Spring Boot web application written in Java.

## Setup and Usage

### Web Scraping

1. Install the required Python libraries:

    ```bash
    pip install requests beautifulsoup4 nltk
    ```

2. Run the Python scraper:

    ```bash
    python python_scraper/scraper.py
    ```

### Spring Boot Web Application

1. Ensure you have Maven installed.

2. Open the `nlp-web-app` directory.

3. Build the project:

    ```bash
    mvn clean install
    ```

4. Run the Spring Boot application:

    ```bash
    mvn spring-boot:run
    ```

5. Access the application in your web browser at [http://localhost:8080/nlp](http://localhost:8080/nlp).


