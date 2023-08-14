import sys
import wave

wav_file = sys.argv[1]
bin_file = sys.argv[2]

output_bits = 8
output_middle = 1 << (output_bits - 1)
output_bytes = 2
output_endian = "little"
input_bits = 16
input_channels = 2
stride = (input_bits // 8) * input_channels


def frame2uint(data):
    return (
        (int.from_bytes(data[:2], "little", signed=True) >> (input_bits - output_bits))
        + output_middle
    ).to_bytes(output_bytes, output_endian)


with wave.open(wav_file, "rb") as wav:
    assert wav.getsampwidth() == input_bits // 8
    assert wav.getnchannels() == input_channels
    assert wav.getframerate() == 48000
    print("Frame rate: {} kHz".format(wav.getframerate() / 1000))
    with open(bin_file, "wb") as bin:
        while True:
            data = wav.readframes(100)
            if not len(data):
                break
            for ind in range(0, len(data), stride):
                for i in range(2):
                    bin.write(frame2uint(data[ind : ind + stride]))
        for i in range(2):
            bin.write(output_middle.to_bytes(output_bytes, output_endian))
