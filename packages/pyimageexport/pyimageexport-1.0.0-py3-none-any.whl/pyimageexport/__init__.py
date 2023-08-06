import os
import io
import base64
from PIL import Image

FORMATS_RGB = [
    "bmp", "eps", "gif", "im", "jpeg", "jpg",
    "png", "ppm", "sgi", "tiff", "webp"
]
FORMAT_BASE64 = "base64"
FORMAT_BLOB = "blob"


class PyImageExport(object):
    """Package to convert various formats of raster graphics images
    in a single line of code. A good alternative for image conversion,
    saving in databases, or image transmission."""

    def __init__(self):
        self.input_image = ""
        self.input_format = ""
        self.output_format = ""
        self.output_name = ""
        self.output_path = "./"
        self.output = ""

    def __validateParams(self, *args, **kwargs):
        """Function to get and validate parameters"""

        # Input image
        if "input_image" in kwargs:
            self.input_image = kwargs["input_image"]
        else:
            print("Error: input_image is a necessary parameter.")
            return False

        # Input format
        if "input_format" in kwargs:
            input_format = kwargs["input_format"].lower()
            if input_format in FORMATS_RGB or \
                input_format == FORMAT_BASE64 or \
                    input_format == FORMAT_BLOB:
                self.input_format = input_format
            else:
                print(f"\"{input_format}\" is not a valid input format.")
                return False
        else:
            return False

        # Output format
        if "output_format" in kwargs:
            self.output_format = kwargs["output_format"]
        else:
            print("Error: output_format is a necessary parameter.")
            return False

        # Output name
        if "output_name" in kwargs:
            self.output_name = kwargs["output_name"]
        else:
            if os.path.exists(str(self.input_image)):
                file_name = os.path.splitext(
                    os.path.basename(kwargs["input_image"]))[0]
                self.output_name = file_name

        # Output path
        if "output_path" in kwargs:
            self.output_path = kwargs["output_path"]
        else:
            if self.input_image in FORMATS_RGB:
                self.output_path = os.path.dirname(self.input_image)

        return True

    def __inputRGB(self):
        if self.output_format in FORMATS_RGB:
            try:
                output = "{}/{}.{}".format(
                    self.output_path, self.output_name, self.output_format)
                img = Image.open(self.input_image)
                if self.input_format == "png":
                    img = img.convert("RGBA")
                    img.load()
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    background.save(
                        output, self.output_format.upper(), quality=80)
                else:
                    img = img.convert("RGB")
                    img.save(output)
                self.output = output
            except Exception as e:
                print("Error:", e)
        elif self.output_format == FORMAT_BASE64:
            try:
                with open(self.input_image, "rb") as reader:
                    file_encode = base64.b64encode(reader.read())
                    self.output = file_encode
            except Exception as e:
                print("Error:", e)
        elif self.output_format == FORMAT_BLOB:
            try:
                with open(self.input_image, "rb") as reader:
                    file_encode = io.BytesIO(reader.read())
                    self.output = file_encode.getvalue()
            except Exception as e:
                print("Error:", e)

    def __inputBase64(self):
        if self.output_format in FORMATS_RGB:
            try:
                output = "{}/{}.{}".format(
                    self.output_path, self.output_name, self.output_format)
                with open(self.output, "wb") as writer:
                    writer.write(base64.b64decode(self.input_image))
                self.output = output
            except Exception as e:
                print("Error:", e)
        elif self.output_format == FORMAT_BLOB:
            self.output = base64.b64decode(self.input_image)

    def __inputBlob(self):
        if self.output_format in FORMATS_RGB:
            try:
                output = "{}/{}.{}".format(
                    self.output_path, self.output_name, self.output_format)
                with open(self.output, "wb") as writer:
                    writer.write(self.input_image)
                self.output = output
            except Exception as e:
                print("Error:", e)
        elif self.output_format == FORMAT_BASE64:
            self.output = base64.b64encode(self.input_image)

    def export(self, *args, **kwargs):
        """
        Export image to another format.
        Parameters
        ----------
        input_image: str | bytes
            location of the image or base64 image(in str) or image(in bytes)
        input_format: str
            type of input_image format(png, jpeg, base64, blob, etc...)
        output_format: str
            type of output format(png, jpeg, base64, blob, etc...)
        output_name: str
            file name for the export(ignore if output_format if base64 or blob)
        output_path: str
            path for the export(ignore if output_format if base64 or blob)
        """

        # Get all the info
        if self.__validateParams(*args, **kwargs):
            if self.input_format in FORMATS_RGB:
                self.__inputRGB()
            elif self.input_format == FORMAT_BASE64:
                self.__inputBase64()
            elif self.input_format == FORMAT_BLOB:
                self.__inputBlob()
            return self.output
        else:
            return False

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"\"{self.input_image}\", \"{self.input_format}\")")

    def __str__(self):
        return (f"{self.__class__.__name__}: The image "
                f"\"{self.input_image}\" was converted to "
                f"{self.output_format.upper()} format.")
