import argparse
import subprocess
import shutil
from pathlib import Path


def convert_r3d_to_mp4(input_file: Path, output_file: Path, redline_exe: str) -> None:
    """Run REDline to convert a single R3D file to MP4."""
    cmd = [
        redline_exe,
        "--i", str(input_file),
        "--o", str(output_file),
        "--codec", "H264",
        "--format", "MP4",
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert .R3D files to .mp4 using the REDline tool from the R3D SDK"
    )
    parser.add_argument("source", help="Input .R3D file or a directory containing R3D files")
    parser.add_argument(
        "-o",
        "--out-dir",
        default=".",
        help="Directory to write converted mp4 files",
    )
    parser.add_argument(
        "--redline",
        default=shutil.which("REDline"),
        help="Path to the REDline executable (defaults to first found on PATH)",
    )
    args = parser.parse_args()

    if not args.redline or not Path(args.redline).exists():
        raise SystemExit(
            "REDline executable not found. Install the R3D SDK and provide the path via --redline."
        )

    src = Path(args.source)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if src.is_file():
        if src.suffix.lower() != ".r3d":
            raise SystemExit("Input file must have .R3D extension")
        out_file = out_dir / f"{src.stem}.mp4"
        convert_r3d_to_mp4(src, out_file, args.redline)
    else:
        for r3d_file in src.rglob("*.R3D"):
            out_file = out_dir / f"{r3d_file.stem}.mp4"
            convert_r3d_to_mp4(r3d_file, out_file, args.redline)


if __name__ == "__main__":
    main()
