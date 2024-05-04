import streamlit as st
import mysql.connector
import pandas as pd
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import re

# Initialize the YouTube API service
api_service_name = "youtube"
api_version = "v3"
api_key="AIzaSyDGmG3O25HaHf_7vNxvKRl7GwvvXpL1yPg"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


# Function to fetch data from MySQL database
def fetch_data(query):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="youtube")
    df = pd.read_sql(query, mydb)
    mydb.close()
    return df


# Function to execute predefined queries
def execute_query(question):
    query_mapping = {
        "What are the names of all the videos and their corresponding channels?": """
            SELECT videos.Video_title, channels.channel_name
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id;
        """,
        "Which channels have the most number of videos, and how many videos do they have?": """
            SELECT channel_name, COUNT(*) AS video_count
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            GROUP BY channel_name
            ORDER BY video_count DESC
            LIMIT 1;
        """,
        "What are the top 10 most viewed videos and their respective channels?": """
            SELECT videos.Video_title, channels.channel_name
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            ORDER BY videos.Video_viewcount DESC
            LIMIT 10;
        """,
        "How many comments were made on each video, and what are their corresponding video names?": """
            SELECT videos.Video_title, COUNT(*) AS comment_count
            FROM videos
            JOIN comments ON videos.Video_Id = comments.video_id
            GROUP BY videos.Video_title;
        """,
        "Which videos have the highest number of likes, and what are their corresponding channel names?": """
            SELECT videos.Video_title, channels.channel_name
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            ORDER BY videos.Video_likecount DESC
            LIMIT 1;
        """,
        "What is the total number of likes for each video, and what are their corresponding video names?": """
            SELECT videos.Video_title, SUM(videos.Video_likecount) AS total_likes
            FROM videos
            GROUP BY videos.Video_title;
        """,
        "What is the total number of views for each channel, and what are their corresponding channel names?": """
            SELECT channels.channel_name, SUM(videos.Video_viewcount) AS total_views
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            GROUP BY channels.channel_name;
        """,
        "What are the names of all the channels that have published videos in the year 2022?": """
            SELECT DISTINCT channels.channel_name
            FROM channels
            JOIN videos ON channels.channel_id = videos.channel_id
            WHERE YEAR(videos.Video_pubdate) = 2022;
        """,
        "What is the average duration of all videos in each channel, and what are their corresponding channel names?": """
            SELECT channels.channel_name, AVG(videos.Video_duration) AS average_duration
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            GROUP BY channels.channel_name;
        """,
        "Which videos have the highest number of comments, and what are their corresponding channel names?": """
            SELECT videos.Video_title, channels.channel_name
            FROM videos
            JOIN channels ON videos.channel_id = channels.channel_id
            ORDER BY videos.Video_commentcount DESC
            LIMIT 1;
        """
    }

    query = query_mapping.get(question)
    if query:
        return fetch_data(query)
    else:
        return pd.DataFrame()


# Function to fetch channel data using YouTube API
def fetch_channel_data(new_channel_id):
    try:
        # Check if the channel ID already exists in the database
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="youtube")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM channels WHERE channel_id = %s", (new_channel_id,))
        existing_channel = cursor.fetchone()
        mydb.close()

        if existing_channel:
            # Show error message if the channel ID already exists
            st.error("Channel ID already exists in the database.")
            return pd.DataFrame()
        
        request = youtube.channels().list(
            part="contentDetails,snippet,statistics",
            id=new_channel_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:

        # Parse the response and return relevant channel data
            data = {
                'channel_id': new_channel_id,
                'channel_name': response['items'][0]['snippet']['title'],
                'channel_des': response['items'][0]['snippet']['description'],
                'channel_playid': response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                'channel_vidcount': response['items'][0]['statistics']['videoCount'],
                'channel_viewcount': response['items'][0]['statistics']['viewCount'],
                'channel_subcount': response['items'][0]['statistics']['subscriberCount']
            }

            # Insert the channel data into MySQL database
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="youtube")
            cursor = mydb.cursor()
            cursor.execute("""
                INSERT INTO channels (channel_id, channel_name, channel_des, channel_playid, channel_vidcount, channel_viewcount, channel_subcount)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['channel_id'], data['channel_name'], data['channel_des'], data['channel_playid'], data['channel_vidcount'], data['channel_viewcount'], data['channel_subcount']))
            mydb.commit()
            mydb.close()

            return pd.DataFrame(data, index=[0])
        else:
            st.error("No items found in the response.")
            return pd.DataFrame()
    except HttpError as e:
        st.error(f"HTTP Error: {e}")
        return pd.DataFrame()
    except KeyError as e:
        st.error(f"KeyError: {e}. Please make sure the channel ID is correct.")
        return pd.DataFrame()


# Function to fetch video data using YouTube API
def all_video_Ids(channel_ids):
  all_video_ids = []
  for new_channel_id in channel_ids:
    video_ids = []
    try:
      response = youtube.channels().list(part="contentDetails", id=new_channel_id).execute()
      if 'items' in response and len(response['items']) > 0:
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None

        while True:
          response1 = youtube.playlistItems().list(
              part="snippet",
              maxResults=50,
              pageToken=next_page_token,
              playlistId=playlist_id
          ).execute()
          for i in range(len(response1.get('items', []))):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
          next_page_token = response1.get('nextPageToken')

          if next_page_token is None:
            break
      else:
        st.error(f"No channels found for ID: {new_channel_id}")
    except HttpError as e:
      st.error(f"HTTP Error: {e}")
    except KeyError as e:
      st.error(f"KeyError: {e}")

    all_video_ids.extend(video_ids)
  return all_video_ids


# Function to fetch video data using YouTube API
def fetch_video_data(all_video_ids):
    video_data = []
    for video_id in all_video_ids:
        request = youtube.videos().list(
            part="contentDetails,snippet,statistics",
            id=video_id
        )
        response = request.execute()

        for details in response["items"]:
            data = {
                'Video_Id': details['id'],
                'Video_title': details['snippet']['title'],
                'channel_id': details['snippet']['channelId'],
                'Video_Description': details['snippet']['description'],
                'Video_pubdate': details['snippet']['publishedAt'],
                'Video_thumbnails': details['snippet']['thumbnails']['default']['url'],
                'Video_viewcount': details['statistics']['viewCount'],
                'Video_likecount': details['statistics'].get('likeCount', 0),
                'Video_favoritecount': details['statistics']['favoriteCount'],
                'Video_commentcount': details['statistics'].get('commentCount', 0),
                'Video_duration': iso8601_duration_to_seconds(details['contentDetails']['duration']),
                'Video_caption': details['contentDetails']['caption']
            }
            video_data.append(data)

    # Insert video data into MySQL database
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="youtube")
    cursor = mydb.cursor()
    for video in video_data:
        cursor.execute("""
            INSERT INTO videos (Video_Id, Video_title, channel_id, Video_Description, Video_pubdate, Video_thumbnails, Video_viewcount, Video_likecount, Video_favoritecount, Video_commentcount, Video_duration, Video_caption)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (video['Video_Id'], video['Video_title'], video['channel_id'], video['Video_Description'], video['Video_pubdate'], video['Video_thumbnails'], video['Video_viewcount'], video['Video_likecount'], video['Video_favoritecount'], video['Video_commentcount'], video['Video_duration'], video['Video_caption']))
    mydb.commit()
    mydb.close()

    return pd.DataFrame(video_data)


# Function to fetch comment data using YouTube API
def fetch_comment_data(new_channel_id):
    comment_data = []
    all_video_ids = all_video_Ids([new_channel_id])
    for video_id in all_video_ids:
        next_page_token = None
        while True:
            try:
                request_comments = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token)
                response_comments = request_comments.execute()

                for comment in response_comments["items"]:
                    data = {
                        'comment_id': comment['snippet']['topLevelComment']['id'],
                        'video_id': comment['snippet']['topLevelComment']['snippet']['videoId'],
                        'channel_id': comment['snippet']['channelId'],
                        'author_name': comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'text_display': comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'published_date': comment['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                    comment_data.append(data)

                next_page_token = response_comments.get('nextPageToken')

                if next_page_token is None:
                    break
            except HttpError as e:
                if e.resp.status == 403:
                    st.warning(f"Comments are disabled for some videos in channel ID: {new_channel_id}")
                    break
                else:
                    raise

    # Insert comment data into MySQL database
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="youtube")
    cursor = mydb.cursor()
    for comment in comment_data:
        cursor.execute("""
            INSERT INTO comments (comment_id, video_id, channel_id, author_name, text_display, published_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (comment['comment_id'], comment['video_id'], comment['channel_id'], comment['author_name'], comment['text_display'], comment['published_date']))
    mydb.commit()
    mydb.close()

    return pd.DataFrame(comment_data)


def iso8601_duration_to_seconds(duration):
    match = re.match(r'^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$', duration)
    if not match:
        return None

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds


def main():
    st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
    st.sidebar.header("Tables")

    selected_option = st.sidebar.radio("Select Option", ("Channels", "Videos", "Comments", "Queries", "Enter YouTube Channel ID"))

    if selected_option == "Channels":
        st.header("Channels")
        channels_df = fetch_data("SELECT * FROM channels;")
        channels_df.index += 1
        st.dataframe(channels_df)

    elif selected_option == "Videos":
        st.header("Videos")
        videos_df = fetch_data("SELECT * FROM videos;")
        videos_df.index += 1
        st.dataframe(videos_df)

    elif selected_option == "Comments":
        st.header("Comments")
        comments_df = fetch_data("SELECT * FROM comments;")
        comments_df.index += 1
        st.dataframe(comments_df)

    elif selected_option == "Queries":
        st.header("Queries")
        query_question = st.selectbox("Select Query", [
            "What are the names of all the videos and their corresponding channels?",
            "Which channels have the most number of videos, and how many videos do they have?",
            "What are the top 10 most viewed videos and their respective channels?",
            "How many comments were made on each video, and what are their corresponding video names?",
            "Which videos have the highest number of likes, and what are their corresponding channel names?",
            "What is the total number of likes for each video, and what are their corresponding video names?",
            "What is the total number of views for each channel, and what are their corresponding channel names?",
            "What are the names of all the channels that have published videos in the year 2022?",
            "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "Which videos have the highest number of comments, and what are their corresponding channel names?"
        ])
        if query_question:
            query_result_df = execute_query(query_question)
            query_result_df.index += 1
            st.dataframe(query_result_df)

    elif selected_option == "Enter YouTube Channel ID":
        st.header("Enter YouTube Channel ID")
        channel_id = st.text_input("Channel ID")
        if st.button("Fetch Channel Data"):
            channel_df = fetch_channel_data(channel_id)
            channel_df.index+=1
            st.subheader("Channel Data")
            st.write(channel_df)

        if st.button("Fetch Video Data"):
            all_video_ids = all_video_Ids([channel_id])
            video_df = fetch_video_data(all_video_ids)
            video_df.index+=1
            st.subheader("Video Data")
            st.write(video_df)

        if st.button("Fetch Comment Data"):
            comment_df = fetch_comment_data([channel_id])
            comment_df.index+1
            st.subheader("Comment Data")
            st.write(comment_df)


if __name__ == "__main__":
    main()