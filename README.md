# Project-1
Hello, I’m interested in Data Science field and You can reach me at venkateshms2017@gmail.com


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
