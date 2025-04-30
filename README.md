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
# Crack Detection 
## SAM (Segment Anything Model)
To download the sam model for processing:
```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```
This goes into `/crack_detection`

TODO
- add a progress bar
To download videos for testing:
## yt-dlp
Note: this is a command **only** for downloading test videos.
```bash
yt-dlp -f "bestvideo[ext=mp4][height<=720]" --merge-output-format mp4 <video_url>
```
These videos download at 720p, to avoid higher resolutions which take longer to process.

## TODO
task                               | progress    | note
-----------------------------------|-------------|-----------------
progress bar                       | not started | should be simple
combining processing scripts       | in progress | going well
output "crack level" number to csv | not started |