class ImageUtils:
    @staticmethod
    def image_attribute(image):
        """
        Extracts attributes from the image dictionary and concatenates them into a single string.
        :param image: Dictionary containing image attributes.
        :return: String of concatenated attributes separated by space.
        """

        tags = image['Tags']
        return f"{tags}"