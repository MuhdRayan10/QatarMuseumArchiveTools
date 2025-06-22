import subprocess

def convert_r3d_to_mp4(input_path, output_path):
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def create_output_path(input_path):
    return ""

def r3d_to_mp4(input_path):
    try:

        output_path = create_output_path(input_path)
        cmd = ["ffmpeg", "-y", "-i", input_path, "-c:v", "libx264", "-preset", "slow", "-crf", "18", output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except subprocess.CalledProcessError:
        print("Could not convert")
        return False