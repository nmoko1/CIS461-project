from PIL import Image
import numpy

def binaryconvert (message):
   return ''.join(format(ord(x), '08b') for x in message)

message = binaryconvert("secret message")

def messageconvert (binarymsg):
    chars = []
    for i in range (0, len(binarymsg), 8):
        byte = binarymsg[i:i+8]
        chars.append(chr(int(byte, 2)))
    return "".join(chars)

def encode_message (img_path, message, output_path):
    img = Image.open(img_path)

    img_array = numpy.array(img)

    binary_msg = binaryconvert(message) + "1111111111111110"

    flat_img = img_array.flatten()

    if len(binary_msg) > len(flat_img):
        raise Exception("Message too long for image") 

    for i in range(len(binary_msg)):
        flat_img[i] = (flat_img[i] & 0xFE) | int(binary_msg[i])

    encoded_img_array = flat_img.reshape(img_array.shape)
    encoded_img = Image.fromarray(encoded_img_array)
    encoded_img.save(output_path)

    print(f"Message encoded and saved to {output_path}")

def decode_message(encoded_image_path):
    img = Image.open(encoded_image_path)
    img_array = numpy.array(img)
    flat_img = img_array.flatten()

    binary_message = ""
    for pixel in flat_img:
        binary_message += str(pixel & 1)
    
    delimiter = "1111111111111110"
    binary_message = binary_message.split(delimiter)[0]

    secret_message = messageconvert(binary_message)
    return secret_message

encode_message("project_image.png", "secret message", "encoded_projimage.png")

hidden_message = decode_message("encoded_projimage.png")
print(hidden_message)
