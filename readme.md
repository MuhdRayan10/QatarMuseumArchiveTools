# R3D to MP4 Conversion Interface

This part of the repo contains a **Python** utility to batch-convert **RED `.R3D`** camera files into **H.264 `.mp4`** files via an intermediate **ProRes** (.mov) data file. It creates a new directory containing the converted files in the exact same structure as the source directory.

## Prerequisites

* **Windows or macOS** with access to terminal.
* **Python 3.8+**
* **REDCINE‑X Pro** (provides the `redline` CLI tool).
* **FFmpeg** (for converting `.mov` into `.mp4`.
* **Python packages**: `ffmpeg-python`, `subprocess`, `time`, `os` 

  ```bash
  pip install ffmpeg-python

## Functions To Get Used To

* **`r3d_to_mov(input_path, output_dir)`**: Converts a single `.R3D` clip to a `.mov` using REDline.
* **`mov_to_mp4(input_path)`**: Re-encodes the `.mov` into `.mp4` with the help of `ffmpeg-python`.
* **`convert_file(input_path, output_dir)`**: Handles the complete process of `.R3D` to `.mp4` file conversion while removing any intermediate files.
* **`convert_directory(input_dir)`**: Recursively processes all `.R3D` files in `input_dir`, and creates a new directory of similar structure containing the converted files.


  ```

## Installation

1. **Clone the repo**:

   ```bash
   git clone https://github.com/MuhdRayan10/QatarMuseumArchiveTools
   cd QatarMuseumArchiveTools
   ```
2. **Install Python dependencies** (none so far, but in case):

   ```bash
   pip install -r requirements.txt
   ```
3. **Confirm that `redline` and `ffmpeg`** are working from your shell (if not, update your `PATH`):

   ```bash
   which redline
   which ffmpeg
   ```

## Usage

<Working on this section>


## Customisability

Will add features that can help users tweak the quality of the conversion, and many other things. A GUI is also being developed.

## License

This project is licensed under the **MIT License**. See [LICENSE](https://opensource.org/license/mit) for details.

---

