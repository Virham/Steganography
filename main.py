from PIL import Image
import sys


def convert_pixel(pixel, data):
    return tuple([p - (p % 2 == 1) + data[i] for i, p in enumerate(pixel[0:3])]) + ((pixel[3],) if len(pixel) > 3 else tuple())

def get_pixel_data(pixel):
    return [p & 1 for p in pixel[:3]]

def get_max_data_size(img):
    return (img.width * img.height * 3) // 8

def get_min_img_size(img, data):
    s = get_max_data_size(img)
    scale = max(1, len(data) // 8 / s)
    
    return (round(img.width * scale), round(img.height * scale))

def encode_string(string):
    data = []
    
    for l in string:
        bits = bin(ord(l))[2:]
        d = [int(bit) for bit in bits]
        if len(d) > 8:
            continue

        d = [0] * (8 - len(d)) + d
        data.extend(d)
    
    return data + [0] * 8 # end of file byte


def encode_image(img : Image, string) -> Image:
    data = encode_string(string)
    size = get_min_img_size(img, data)
    image = img.resize(size)

    pixels = image.load()
    for j in range(image.height):
        for i in range(image.width):
            index = (i + j * image.width) * 3

            if len(data) <= index + 2:
                d = data[index:]
                d += [0] * (3 - len(d))

                next_index = (i + j * image.width + 1)
                x,y = next_index % image.width, next_index // image.width
                pixels[x, y] = (255, 0, 0, 255)
                return image

            d = data[index:index+3]
            pixels[i, j] = convert_pixel(pixels[i, j], d)

    return image


def decode_image(image : Image):
    pixels = image.load()
    data = []
    byte = []
    
    for j in range(image.height):
        for i in range(image.width):
            byte.extend(get_pixel_data(pixels[i, j]))
            if len(byte) >= 8:
                d = "0b" + "".join([str(b) for b in byte[0:8]])
                byte = byte[8:]

                ascii = int(d, 2)
                if ascii < 10:
                    return "".join(data)

                data.append(chr(ascii))

    return "".join(data)





if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("ok")
        quit()

    if sys.argv[1] == "encode":
        if len(sys.argv) < 5:
            print("not enough arguments.")
            quit()

        img = Image.open(sys.argv[2])
        with open(sys.argv[3], "r") as f:
            text = f.read()
        
        output = sys.argv[4]
        encode_image(img, text).save(output)

    elif sys.argv[1] == "decode":
        if len(sys.argv) < 3:
            print("not enough arguments.")
            quit()
        
        print(decode_image(Image.open(sys.argv[2])))

    else:
        print("You dyslexic")

