import subprocess
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

r3d_to_mov("/Users/rayan/Downloads/sample.R3D")