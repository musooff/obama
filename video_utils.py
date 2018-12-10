import subprocess
from typing import List



ffmpeg_exe = "/usr/bin/ffmpeg /usr/share/ffmpeg /usr/share/man/man1/ffmpeg.1.gz"

COMMAND_BASE =  [ffmpeg_exe]
COMMAND_BASE += ["-n"      ] # disable file overwriting



class Video():
  def __init__(self, path=str, speed=1.0):
    self.path  = path
    self.speed = speed



def concatenate_videos(videos=list[Video], output_file=str):
  video_count  = len(videos)
  video_speeds = [float(1/x.speed) for x in videos]
  audio_speeds = [float(x.speed  ) for x in videos]

  cmd_input_files = []
  filters, concat = ("", "")
  for i, x in enumerate(videos):
    cmd_input_files += ["-i", x.path]
    filters += f"[{i}:v] setpts = {video_speeds[i]} * PTS [v{i}];"
    filters += f"[{i}:a] atempo = {audio_speeds[i]}       [a{i}];"
    concat  += f"[v{i}][a{i}]"
  concat += f"concat = n = {video_count}:v = 1:a = 1 [v_all][a_all]"

  filter_complex = f"{filters}{concat}".replace(" ", "")

  cmd_filter_complex = [
    "-filter_complex", filter_complex,
  ]
  cmd_map = [
    "-map", "[v_all]",
    "-map", "[a_all]",
  ]
  command = sum([
    COMMAND_BASE,
    cmd_input_files,
    cmd_filter_complex,
    cmd_map,
    [output_file],
  ], [])

  subprocess.run(command)
