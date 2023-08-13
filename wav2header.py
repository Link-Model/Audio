import sys
import wave

var_name = sys.argv[1]
wav_file = sys.argv[2]
header_file = sys.argv[3]

def frame2uint(data):
    return "{:>3}".format((int.from_bytes(data[:2], "little", signed=True) >> 8) + (1 << 7))

max_row_size = 15

with wave.open(wav_file, 'rb') as wav:
    assert wav.getsampwidth() == 2
    assert wav.getnchannels() == 2
    assert wav.getframerate() == 48000
    print("Frame rate: {} kHz".format(wav.getframerate() / 1000))
    with open(header_file, 'w+') as header:
        header.write("const int {}_length = {};\n".format(var_name, wav.getnframes() + 1))
        header.write("uint16_t {}[] = ".format(var_name))
        header.write("{\n  ")
        row_size = 0
        while True:
            data = wav.readframes(100)
            if not len(data):
                break
            for ind in range(0, len(data), 4):
                header.write("{}, ".format(frame2uint(data[ind:ind+4])))
                row_size += 1
                if row_size >= max_row_size:
                    header.seek(header.tell() - 1)
                    header.write("\n  ")
                    row_size = 0
        header.write(str(1 << 7))
        header.write("};\n")
