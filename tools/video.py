import requests
from typing import Optional, Type
from pydantic import Field, BaseModel
from langchain.tools import BaseTool

import json
import numpy as np
import moviepy.editor as mp
from moviepy.video.tools.drawing import color_gradient

class MakeShortFormVideoSchema(BaseModel):
    titles: str = Field(description="pipe delimited list of news titles")
    intro: str = Field(description="Intro text for the video")
    summary: str = Field(description="Summary of all the news headlines combined into a single sentence")

class MakeShortFormVideoTool(BaseTool):
    name = "make_short_form_video"
    description = "useful for when you need to make a short form video from news titles"
    args_schema: Type[MakeShortFormVideoSchema] = MakeShortFormVideoSchema

    def _run(self, titles: str, intro: str, summary: str) -> str:
        """Use the tool."""

        list_of_titles = titles.strip('][').split(', ')
        #list_of_titles = ['title 1', 'title 2', 'title 3']
        self.create_title_slides(list_of_titles, intro, summary)
        
        return list_of_titles
    
    async def _arun(self, subreddit: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("make short form video does not support async")
    


    def create_title_slides(self, json_array, intro, summary):
        # Set video dimensions
        video_width = 800
        video_height = 600

        # Set slide duration
        slide_duration = 2.5  # Adjust as desired

        # Create video clip
        clips = []

        # Add intro slide
        intro_text = intro
        intro_clip = mp.TextClip(intro_text, fontsize=70, color='white', size=(video_width, video_height), font="DejaVu-Sans")
        intro_clip = intro_clip.set_duration(slide_duration)
        clips.append(intro_clip)

        # Add title slides
        for title in json_array:

            # Create text clip with the title
            title_clip = mp.TextClip(title, fontsize=50, color='white', size=(video_width, video_height), font="DejaVu-Sans")

            # Center the text on the background image
            title_clip = title_clip.set_position(('center', 'center'))

            # Set the slide duration
            title_clip = title_clip.set_duration(slide_duration)

            # Overlay the title on the background image
            slide_clip = mp.CompositeVideoClip([title_clip])

            clips.append(slide_clip)

        # Add summary slide
        summary_text = summary
        summary_clip = mp.TextClip(summary_text, fontsize=70, color='white', size=(video_width, video_height), font="DejaVu-Sans")
        summary_clip = summary_clip.set_duration(slide_duration)
        clips.append(summary_clip)

        # Concatenate all the clips
        final_clip = mp.concatenate_videoclips(clips)

        # Set the video duration
        video_duration = len(json_array) * slide_duration + slide_duration * 2
        final_clip = final_clip.set_duration(video_duration)

        # Set the video output filename
        output_filename = 'title_slides_video.mp4'

        # Write the video to a file
        final_clip.write_videofile(output_filename, codec='libx264', fps=24)