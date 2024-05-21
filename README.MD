# Steganography
hide files in images

This project hides a given file in a given image, and let't you decode images. It works with any given filetype and upscales the image if more space needed.

### To hide a file:
```bash
python3 main.py encode path/image path/hidden_file path/output_image
```

### To retrieve a file:
```bash
python3 main.py decode path/output_image path/retrieved_file
```

## Example:    
### Encoding:
#### *text.txt*
> This is a hidden message.


#### *galaxy.png*
<img src="media/galaxy.png" width=500>

```bash
python3 main.py encode media/galaxy.png media/text.txt encoded.png
```

#### encoded.png
<img src="media/encoded.png" width=500>

### Decoding:
```bash
python3 main.py decode encoded.png output.txt
```
#### output.txt
> This is a hidden message.
