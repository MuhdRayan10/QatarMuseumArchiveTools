import subprocess
import ffmpeg
import argparse
import sys
import os


def r3d_to_mov(input_path):
    output_path = os.path.splitext(input_path)[0] + '.mov'
    command = ["redline", "--exportPreset", "A", "-i", input_path, "-w", "201", "-R", "4", 
               "--useRMD", "1", "-c", "1", "-G", "32", "--o", output_path]

    print("Running R3D -> MOV conversion...")
    subprocess.run(command, check=True)
    print(f"Conversion complete: {output_path}")

def mov_to_mp4(input_path):
    output_path = os.path.splitext(input_path)[0] + '.mp4'

    print("Running MOV -> MP4 conversion...")
    ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac', preset="fast").run(overwrite_output=True)
    print(f"Conversion complete: {output_path}")

mov_to_mp4("/Users/rayan/Downloads/sample.mov")