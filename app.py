from flask import Flask, render_template, flash
import requests
import urllib.request
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import csv


app = Flask(__name__)
app.secret_key = "password"

# Access Key - PIXABAY
pixabayKey = "26665956-581e1893500811328e88245c7"


def getVideoData():

    file = open("videoData.csv")
    csvreader = csv.reader(file)

    rows = []
    for row in csvreader:
        rows.append(row)

    # List -->> [[keyword, duration]]
    keyDurList = []

    for i in range(len(rows[1])):

        if i != 0:

            subtitle = rows[1][i]
            keyword = rows[2][i]
            duration = int(rows[3][i][0])
            tempList = [keyword, duration, subtitle]
            keyDurList.append(tempList)
            # print("Search", i, " : ", tempList)

    file.close()

    print("Keyword Duration List :", keyDurList)
    return(keyDurList)


# https://pixabay.com/api/videos/?key={KEY}&q={QUERY+SEARCH}&pretty=true

@app.route("/", methods=['GET'])
def getVideos():

    # Get keywords & durations of video search query
    keywordList = getVideoData()

    videoURL = []

    videos = []

    # Iterate through keywords & durations
    for word in keywordList:

        # Keyword
        queryString = word[0]

        query = {'key': pixabayKey, 'q': queryString,
                 'video_type': 'film', 'pretty': 'true'}
        res = requests.get('https://pixabay.com/api/videos/', params=query)

        print("Get URL: ", res.url)
        # res = requests.get('https://pixabay.com/api/videos/?key=26665956-581e1893500811328e88245c7&q=yellow+flowers&pretty=true')

        data = res.json()

        # Add "download=1" to download videos
        videoURL.append(data["hits"][0]["videos"]
                        ["tiny"]["url"] + "&download=1")
        print("Video URL: ", data["hits"][0]["videos"]["tiny"]["url"])

    # Iterate through Video URL's
    for i in range(len(videoURL)):

        videoLink = videoURL[i]
        videoName = str(i+1) + ".mp4"
        '''
        # Download Video
        print("Downloading starts...\n")
        urllib.request.urlretrieve(videoLink, videoName)
        print("Download completed..!!")
        '''
        # Crop in given duration
        clip = VideoFileClip(videoName)
        clip = clip.subclip(0, keywordList[i][1])

        # Subtitle
        # txt = (TextClip(keywordList[i][2], font='Arial',fontsize=16, color='white').with_duration(keywordList[i][1]))

        def generator(txt): return TextClip(
            txt, font='Arial', fontsize=16, color='white')

        subs = [((0, keywordList[i][1]), keywordList[i][2])]
        subtitles = SubtitlesClip(subs, generator)

        # subtitles = SubtitlesClip(transcript, txt)

        clip = CompositeVideoClip(
            [clip, subtitles.set_pos(('center', 'bottom'))])

        # clip.write_videofile(videoName)
        videos.append(clip)

    finalVideo = concatenate_videoclips(videos)
    finalVideo.write_videofile("Final Video.mp4")

    # showing final clip
    finalVideo.ipython_display(width=480)

    return "website-search-blender-integration"
