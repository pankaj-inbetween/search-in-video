### Search Inside a Video

Quick demo showcasing how to search inside a video using caption / subtitles powered by Astra DB's Vector search

#### Setup

For this demo, I'm using the [Physicswallah's Complete Zoology in One Shot Video from YouTube](https://www.youtube.com/watch?v=haDg_l9jjxA).

Subtitles for this video is [here](./sub.srt)

Set the following environment variable

```
OPENAI_API_KEY=
ASTRA_DB_API_ENDPOINT=
ASTRA_DB_APPLICATION_TOKEN=
```


#### Understanding Subtitles Format

```
1
00:00:25,439 --> 00:00:27,800
hi my dear students hello everyone if I

2
00:00:27,800 --> 00:00:29,960
am Audible and visible properly please

```
```
<index>
<start-time> --> <end-time>
<text>

```

#### Chunking

Append all subtitle texts for a given time window. This demo uses 1 minute window 

```
def split_by_timewindow(subs, window_in_minutes):
    docs = []
    t = ''
    split_time = datetime.time(hour=0,minute=window_in_minutes, second=0)
    for s in subs:
        if s.start.to_time() < split_time:            
            t = t + ' ' + s.text 
        else:            
            start_time =  (split_time.hour*3600) + (split_time.minute*60) + (split_time.second) - 60
            docs.append(Document(page_content=t,metadata={"link":f"{youtube_link}&t={start_time}s", "start_time":start_time}))
            t = s.text            
            split_time = (datetime.datetime(1, 1, 1,split_time.hour,split_time.minute, split_time.second) +  datetime.timedelta(minutes=window_in_minutes)).time()                
    return docs
```

#### Indexing and Search

Chunks are loaded into AstraDB using `langchain` SDK
Notebook converts the search results to a dataframe for easier viewing

