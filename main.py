from device_client import Device
import process_image
import traverse






d = Device()

def main():
    img = d.get_screen()
    letters = process_image.get_letters(img)
    word_lengths = process_image.get_word_lengths(img)

    traverse.find_words({letter:len(letters[letter]) for letter in letters}, word_lengths)

if __name__ == '__main__':
    main()


