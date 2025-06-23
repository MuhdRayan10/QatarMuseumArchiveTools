import subprocess

input_path = "input.R3D"
output_path = "output.mp4"

cmd = [
    "ffmpeg",
    "-i", input_path,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    output_path
]

subprocess.run(cmd, check=True)
