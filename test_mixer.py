import contextlib
import unittest
import mixer
import wave
import os


class TestMixer(unittest.TestCase):
    def test_mix_two_files(self):
        segments = [
            {"file": "audio1.wav", "start": 0, "end": 5},
            {"file": "audio2.wav", "start": 2, "end": 7}
        ]
        output_file = "test_output.wav"
        mixer.mix_audio(segments, output_file)

        self.assertTrue(os.path.exists(output_file), "Output file should exist")

        with contextlib.closing(wave.open(output_file, 'rb')) as outfile:
            self.assertGreater(outfile.getnframes(), 0, "Output file should have frames")

    def test_invalid_segment_times(self):
        segments = [
            {"file": "audio1.wav", "start": 7, "end": 2}
        ]
        output_file = "test_output.wav"

        with self.assertRaises(ValueError):
            mixer.mix_audio(segments, output_file)

    def test_mix_single_file(self):
        segments = [
            {"file": "audio1.wav", "start": 1, "end": 3}
        ]
        output_file = "test_output.wav"
        mixer.mix_audio(segments, output_file)

        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        with contextlib.closing(wave.open(output_file, 'rb')) as outfile:
            self.assertGreater(outfile.getnframes(), 0, "Output file should have frames")

    def test_file_not_found(self):
        segments = [
            {"file": "nonexistent_file.wav", "start": 0, "end": 5}
        ]
        output_file = "test_output.wav"

        with self.assertRaises(FileNotFoundError):
            mixer.mix_audio(segments, output_file)

    def tearDown(self):
        try:
            os.remove("test_output.wav")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
