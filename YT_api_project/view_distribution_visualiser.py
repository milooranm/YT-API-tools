# API client library
import pprint
import googleapiclient.discovery
import plotly.express as px


pp = pprint.PrettyPrinter(indent=2).pprint
# API information
#from YT_api_project import SECRET
MYAPI='AIzaSyAFlP7QxP07DLTmB03-ohtW3GXupREqoOM'



def main():
    chplist = input("copy paste the channelID here: ")
    # Uses the channelID to find the name of the channel playlist
    chplist = "UU" + chplist[2:]
    video_view_list = lister(chplist)
    pp(video_view_list)
    fig = px.bar(y=video_view_list)
    fig.show()


def lister(PlaylistId):
    # Create a YouTube API service object
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=MYAPI)
    videos_ids = []
    # The following set of code finds and saves the first page of results to videos_ids
    request = youtube.playlistItems().list(
        part="snippet", maxResults=50, playlistId=PlaylistId
    )
    response = request.execute()
    for item in response["items"]:
        videos_ids.append(item["snippet"]["resourceId"]["videoId"])
    # The next bit of code cycles through the different pages of results using pagetokens
    # and then adds the videos it finds to videos_ids
    nextPageToken = response.get("nextPageToken")
    while "nextPageToken" in response:
        nextPage = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=PlaylistId,
                maxResults="50",
                pageToken=nextPageToken,
            )
            .execute()
        )
        for item in nextPage["items"]:
            videos_ids.append(item["snippet"]["resourceId"]["videoId"])
        if "nextPageToken" not in nextPage:
            response.pop("nextPageToken", None)
        else:
            nextPageToken = nextPage["nextPageToken"]
    # Initialize a list to store the list of viewcounts
    views = []
    # Loops through videos_ids to find and save the viewcount for each video
    for i in range(0, len(videos_ids)):
        VideoId = videos_ids[i]
        r = (
            youtube.videos()
            .list(part="statistics", id=VideoId, fields="items(statistics),")
            .execute()
        )
        view = r["items"][0]["statistics"]["viewCount"]
        views.append(int(view))
    # Sort the list in descending order
    views = sorted(views, reverse=True)
    return views


if __name__ == "__main__":
    main()