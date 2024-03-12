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

Chunks are loaded into AstraDB using `langchain` SDK.

Notebook converts the search results to a dataframe for easier viewing

```
result = vstore.similarity_search_with_relevance_scores("bio technology application in agriculture", k=1)
```
| ---- | ---- | ---- | ---- | 
| subtitle |	link | start_time | score | 
| whatever organic compounds are there we will isolate them now biotechnology application in agriculture there are various uh you know applications are there see with increasing population like we have read in the chapter number two of zoology which is reproductive Health there was a major issue and that major issue was related to the population increasing you know population in millions it was difficult to feed those number of individuals so what we did we tried to increase the agriculture right by that only we can provide them food so we started using some chemicals we started using some chemicals like insecticide and pesticides and we when we started using those insecticide and pesticide what happened production increased and because of that insecticide and pesticide they had some residual effects also though this lead to the Green Revolution also which later we realized	| https://www.youtube.com/watch?v=haDg_l9jjxA&t=21180s	| 21180	 | 0.943823 | 