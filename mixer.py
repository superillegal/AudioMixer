import wave
import contextlib

def mix_audio(segments, output_file):
    """Mixes audio segments from multiple files into a single output file.

    Args:
        segments: A list of dictionaries, where each dictionary represents an audio segment.
                  Each dictionary should have the following keys:
                    - "file": The path to the audio file.
                    - "start": The start time of the segment in seconds.
                    - "end": The end time of the segment in seconds.
        output_file: The path to the output WAV file.
    """

    if len(segments) == 1:
        segment = segments[0]
        try:
            with contextlib.closing(wave.open(segment["file"], 'rb')) as infile, \
                    contextlib.closing(wave.open(output_file, 'wb')) as outfile:
                outfile.setparams(infile.getparams())

                frames = infile.getnframes()
                framerate = infile.getframerate()

                start_frame = int(segment["start"] * framerate)
                end_frame = int(segment["end"] * framerate)

                if start_frame < 0 or end_frame > frames or start_frame >= end_frame:
                    raise ValueError("Invalid segment times")

                infile.setpos(start_frame)
                outfile.writeframes(infile.readframes(end_frame - start_frame))
        except Exception as e:
            raise

    try:
        outfile = wave.open(output_file, 'wb')

        # Get parameters from the first file (assume all files have the same parameters)
        with contextlib.closing(wave.open(segments[0]["file"], 'rb')) as first_file:
            outfile.setparams(first_file.getparams())

        for segment in segments:
            try:
                with contextlib.closing(wave.open(segment["file"], 'rb')) as infile:
                    frames = infile.getnframes()
                    framerate = infile.getframerate()

                    start_frame = int(segment["start"] * framerate)
                    end_frame = int(segment["end"] * framerate)

                    if start_frame < 0 or end_frame > frames or start_frame >= end_frame:
                        raise ValueError("Invalid segment times")

                    infile.setpos(start_frame)
                    outfile.writeframes(infile.readframes(end_frame - start_frame))

            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {segment['file']}")
            except wave.Error as e:
                raise Exception(f"Error reading WAV file: {e}")



    except Exception as e:
        raise
    finally:
        if 'outfile' in locals() and outfile:
            outfile.close()


def run_mixer():
    segments = []

    num_segments = int(input("Enter the number of audio segments to mix: "))

    for i in range(num_segments):
        file = input(f"Enter the path to audio file {i+1}: ")
        start = int(input(f"Enter the start time (in seconds) for segment {i+1}: "))
        end = int(input(f"Enter the end time (in seconds) for segment {i+1}: "))

        segments.append({"file": file, "start": start, "end": end})

    output_file = input("Enter the desired output file name (e.g., mixed_output.wav): ")

    try:
        mix_audio(segments, output_file)
        print(f"Audio successfully mixed and saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_mixer()
