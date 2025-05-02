csuf-cpe-seniorProject
# Table of contents
<!-- TOC -->

- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Crack Detection](#crack-detection)
    - [SAM Segment Anything Model](#sam-segment-anything-model)
    - [yt-dlp](#yt-dlp)
    - [TODO](#todo)

<!-- /TOC -->
# Overview
Spring 2025 computer engineering senior project at California State University of Fullerton by Esteban Vasco, Mason Phan, Devin Lai, and Wyatt Allen.
## Overall TODO
task                           | progress    | note
-------------------------------|-------------|-----
run everything with one script | not started | :D
# Crack Detection 
## SAM (Segment Anything Model)
To download the sam model for processing:
```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```
This goes into `/crack_detection` alongside the scripts

To download videos for testing:
## yt-dlp
This is a command line utility, look up how to download if you are interested in using it.
Note: this is a command **only** for downloading **test** videos.
```bash
yt-dlp -f "bestvideo[ext=mp4][height<=720]" --merge-output-format mp4 <video_url>
```
These videos download at 720p, to avoid higher resolutions which take longer to process.

## TODO
task                               | progress    | note
-----------------------------------|-------------|-----------------
progress bar                       | not started | not essential
estimated time till finish         | not started | kinda lowkey essential
combining processing scripts       | finished    | .
output "crack level" number to csv | wip         |
test alternate SAM models          |             | looking for lighter to run model thats good enough processing quality fast