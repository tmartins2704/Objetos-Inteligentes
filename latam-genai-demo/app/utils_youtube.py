# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from utils_vertex import get_text_response
from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_url: str, lang: str) -> str:
    video_id = video_url.split("v=")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    except Exception as e:
        print(e)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["en", "es", "pt"])
        translated_transcript = transcript.translate(lang)
        transcript = translated_transcript.fetch()
    transcript = "\n".join([item["text"] for item in transcript])
    return transcript


def get_video_summary(video_url: str, lang: str) -> str:
    with open(f"./prompts/{lang}_summary_video.txt", "r") as f:
        prompt = f.read()
    transcript = get_transcript(video_url, lang)
    if not transcript:
        return "could not find the video transcript."
    prompt = prompt.format(transcript[:50000])
    summary = get_text_response(prompt, model="text-bison-32k")
    return summary


def get_structured_video_info(video_url: str, lang: str, entities: str) -> dict:
    with open("./prompts/video_extraction.txt", "r") as f:
        prompt = f.read()
    transcript = get_transcript(video_url, lang)
    if not transcript:
        return "could not find the video transcript."
    prompt = prompt.format(transcript[:50000], entities, lang)
    content = get_text_response(prompt, model="text-bison-32k")
    content = content.replace("```json", "").replace("```", "").replace('"""', "")
    content = json.loads(content)
    return content
