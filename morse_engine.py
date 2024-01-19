from morse_code_key import morse_code_dict
import numpy as np
import simpleaudio as sa
import time

base_beep_duration = 0.06
base_delay = 0.1


class UserInput:
    """Class to store user provided text/morse and transform"""
    def __init__(self, raw_input):
        self.raw = raw_input
        self.morse_string = ""
        self.text_string = ""
        self.translation_dict = {}

    def encode_to_morse(self):
        """Transform text to morse"""
        morse_list = []
        for char in self.raw:
            morse_list.append(morse_code_dict[char])
            self.translation_dict[char] = morse_code_dict[char]
        self.morse_string = " ".join(morse_list)
        print(self.morse_string)

    def decode_to_string(self):
        """"Transform morse to text"""
        key_list = list(morse_code_dict.keys())
        value_list = list(morse_code_dict.values())
        text_list = []
        for item in self.raw.split(" "):
            if item != " ":
                position = value_list.index(item)
                text_list.append(key_list[position])
            else:
              text_list.append(" ")
        self.text_string = "".join(text_list)
        print("".join(text_list))


def play_morse(beep_duration, pause_duration):
    """Play morse code
        Base formula  y(t) = A*sin(2*pi*f*T + c)
        where:
        A = amplitude
        f = frequency (Hz)
        T = time(s)
        c = phase shift
        fs = sampling rate (Hz)
        ts = discrete sample times

        T = 1 / f =
    """
    fs = 44100
    f = 500
    ts = np.arange(fs * beep_duration) # equivalent to a range [0, T, fs) however T varies hence replaced bs
    # fs*beep_duration
    sample_array = np.sin(1.65 * np.pi * ts * f / fs)
    # Normalize array to 16 bit, 32767 = largest value for int16,
    # Formula
    # normalized array = Array * largest int16 value/max Array value
    normalized_array = sample_array * 32767 / np.max(np.abs(sample_array))
    normalized_array = normalized_array.astype(np.int16)  # turn to datatype int16
    sound_wave = sa.WaveObject(
        audio_data=normalized_array,
        num_channels=2,
        bytes_per_sample=2,
        sample_rate=fs)
    sound_wave.play()
    time.sleep(pause_duration)


def program():
    choice_1 = input("What would you like to do?\n"
                     "a. Encode to Morse Code\n"
                     "b. Decode to Text-form\n"
                     "e. Exit programme\n").lower()
    match choice_1:
        case "a":
            user_input = UserInput(input("Enter the Text to encode: ").upper())
            # user_input.raw = input("Enter the Text to encode: ").upper()
            user_input.encode_to_morse()
            for key, value in user_input.translation_dict.items():
                for char in value:
                    if char == "." or char == "-":
                        play_morse(base_beep_duration, base_delay)
                    elif char == "/":
                        play_morse(base_beep_duration, base_delay * 7)
                play_morse(base_beep_duration, base_delay * 3)
            return True
        case "b":
            user_input = UserInput(input("Enter the Code to encode: ").upper())
            user_input.decode_to_string()
            return True
        case "c":
            print("Exiting...")
            return False
        case _:
            print("Error!")
            return False


if __name__ == "__main__":
    continue_script = True
    while continue_script:
        continue_script = program()