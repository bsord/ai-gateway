import requests
from typing import Optional, Type
from pydantic import Field, BaseModel
from langchain.tools import BaseTool
from services.text_to_speech import get_audio

import json
import numpy as np
import moviepy.editor as mp

class MakeShortFormVideoSchema(BaseModel):
    titles: list[str] = Field(description="array of strings that contains 3 of the best news headlines")
    intro: str = Field(description="Intro text for the video")
    summary: str = Field(description="Text for outro slide thanking the viewer")
    narration: str = Field(description="a short narrative script that explains the news headlines. it should also include the intro at the beginning and summary at the end")

class MakeShortFormVideoTool(BaseTool):
    name = "make_short_form_video"
    description = "useful for when you need to make a short form video from news titles"
    args_schema: Type[MakeShortFormVideoSchema] = MakeShortFormVideoSchema

    def _run(self, titles: list[str], intro: str, summary: str, narration: str) -> str:
        """Use the tool."""
        

        self.create_title_slides(titles, intro, summary, narration)
        
        return titles
    
    async def _arun(self, subreddit: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("make short form video does not support async")
    
    def generate_gradient_background(self, width, height, duration):

        # Define the start and end colors of the gradient
        start_color = (255, 0, 0)  # Red
        end_color = (0, 0, 255)  # Blue

        # Generate the gradient array
        gradient = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                gradient[y, x] = [
                    int(start_color[c] * (1 - x / width) + end_color[c] * (x / width))
                    for c in range(3)
                ]

        # Create a gradient image clip
        gradient_clip = mp.ImageClip(gradient, duration=duration)

        return gradient_clip


    def create_title_slides(self, json_array, intro, summary, narration):
        # generate narration audio
        narration_audio_file = get_audio(narration)

        # Set video dimensions
        video_width = 400
        video_height = 800

        # Set slide duration
        slide_duration = 4.75  # Adjust as desired
        padding = 4

        # Create video clip
        clips = []

        # Add intro slide
        intro_text = intro
        intro_clip = mp.TextClip(intro_text, fontsize=70, color='white', size=(video_width, video_height), font="DejaVu-Sans", method='caption')
        intro_clip = intro_clip.set_duration(slide_duration)
        clips.append(intro_clip)

        # Add title slides
        for title in json_array:

            # Generate a random gradient background
            background_gradient_clip = self.generate_gradient_background(video_width, video_height, slide_duration)

            # Create text clip with the title
            title_clip = mp.TextClip(title, fontsize=50, color='white', size=(video_width, video_height), font="DejaVu-Sans", method='caption')

            # Center the text on the background image
            title_clip = title_clip.set_position(('center', 'center'))

            # Set the slide duration
            title_clip = title_clip.set_duration(slide_duration)

            # Overlay the title on the background image
            slide_clip = mp.CompositeVideoClip([background_gradient_clip, title_clip])
            slide_clip.crossfadein(padding)
            clips.append(slide_clip)

        # Add summary slide
        summary_text = summary
        summary_clip = mp.TextClip(summary_text, fontsize=70, color='white', size=(video_width, video_height), font="DejaVu-Sans", method='caption')
        summary_clip = summary_clip.set_duration(slide_duration)
        clips.append(summary_clip)

        # add transition
        slided_clips = [mp.CompositeVideoClip([clip.fx( mp.transfx.slide_in, 1, 'bottom')]) for clip in clips]

        # Concatenate all the clips
        final_clip = mp.concatenate_videoclips(slided_clips, method="chain")

        # Set the video output filename
        output_filename = 'title_slides_video.mp4'

        # add narration audio
        audioclip = mp.AudioFileClip(narration_audio_file)
        compositeaudioclip = mp.CompositeAudioClip([audioclip])
        final_clip.audio = compositeaudioclip

        # Write the video to a file
        final_clip.write_videofile(output_filename, codec='libx264', fps=30)