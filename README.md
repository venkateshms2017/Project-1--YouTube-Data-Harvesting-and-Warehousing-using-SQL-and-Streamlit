# Project-1
👋 Hi, @riyasudeen here, I’m interested in Data Science field 🌱 DS 📫 You can reach me at riyaspaul82@gmail.com


# YouTube Data Harvesting and Warehousing using SQL and Streamlit


This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.

## STREAMLIT:
Streamlit library was used to create a user-friendly UI that enables users to interact with the programme and carry out data retrieval and analysis operations.

## PYTHON: 
Python is a powerful programming language renowned for being easy to learn and understand. Python is the primary language employed in this project for the development of the complete application, including data retrieval, processing, analysis, and visualisation.

## GOOGLE API CLIENT: 
The googleapiclient library in Python facilitates the communication with different Google APIs. Its primary purpose in this project is to interact with YouTube's Data API v3, allowing the retrieval of essential information like channel details, video specifics, and comments. By utilizing googleapiclient, developers can easily access and manipulate YouTube's extensive data resources through code.


## API Reference

#### Get all items for channels

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `part` | `string` | **Required**. contentDetails, snippet,statistics |

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. id-YouTube channel ID. |


#### Get all items for videos

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `part`      | `string` | **Required**. contentDetails,snippet,statistics |

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id-video_id |

#### Get all items for commentThreads

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `part`      | `string` | **Required**. snippet |

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id - video_id |

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `maxResults`      | `unsigned integer` | **Required**. 1-100 |

```http
  GET /api/items
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pageToken`      | `string` | **Required**. nextPageToken |


## Lessons Learned

Python scripting, Data Collection, Streamlit, API integration, Data Management using SQL  


## Workflow

There are two files

1. ipynb file has the program for collecting data with the help of Google API of YouTube and inputing a YouTube channel ID to retrieve all the relevant data (Channel name, subscribers, description, total video count, total view count, playlist ID for each channel, video ID, video title, video description, publication date, thumblnails, views, likes, duration, caption and comments of each video, author name, comment text, published date for each comments).

2. .py file has the program for input a new channel ID to get details for additional channels and store them in the mysql and display in Streamlit application.

## Demo in LinkedIn
https://www.linkedin.com/posts/riyasudeen-m-876b3a307_here-is-the-first-project-demo-video-in-python-activity-7192457905189634048-gXT1?utm_source=share&utm_medium=member_desktop




## Installation

Install packages with pip

```bash
pip install mysql.connector
pip install pandas
pip install sqlalchemy
pip install streamlit


import googleapiclient.discovery
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import re
from googleapiclient.errors import HttpError
import streamlit as st
