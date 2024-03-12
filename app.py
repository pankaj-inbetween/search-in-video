import pysrt
import datetime 
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os 
import pandas as pd 

load_dotenv()

subs = pysrt.open('sub.srt')
youtube_link = "https://www.youtube.com/watch?v=haDg_l9jjxA"

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
            print(start_time, s.start)
    return docs

t=split_by_timewindow(subs, 1)

embedding = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name="test",
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
)

vstore.add_documents(t)

result = vstore.similarity_search_with_relevance_scores("bio technology application in agriculture", k=1)

for r in result:
    print(r[0].metadata['link'])
    print(r[0].page_content)

