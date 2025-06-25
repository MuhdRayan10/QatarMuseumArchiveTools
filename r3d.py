import subprocess
import ffmpeg
import os


def r3d_to_mov(input_path, output_dir):
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + '.mov')
    command = ["redline", "--exportPreset", "A", "-i", input_path, "-w", "201", "-R", "4", 
               "--useRMD", "1", "-c", "1", "-G", "32", "--o", os.path.splitext(os.path.basename(output_path))[0]]

    print("Running R3D -> MOV conversion...")
    subprocess.run(command, check=True)
    print(f"Conversion complete: {output_path}")

    return output_path

def mov_to_mp4(input_path):
    output_path = os.path.splitext(input_path)[0] + '.mp4'

    print("Running MOV -> MP4 conversion...")
    ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac', preset="fast").run(overwrite_output=True)
    print(f"Conversion complete: {output_path}")

    return output_path


def convert_file(input_path, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)

    mov_path = r3d_to_mov(input_path, output_dir)
    mp4_path = mov_to_mp4(mov_path)

    final_mp4 = os.path.join(output_dir, os.path.basename(mp4_path))
    os.replace(mp4_path, final_mp4)

    try:
        os.remove(mov_path)
    except OSError:
        pass

    return final_mp4

convert_file("/Users/rayan/Downloads/sample.r3d", "/Users/rayan/Downloads/output")