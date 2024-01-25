import pygame

class Extracter:

    def scale_image(self, image: pygame.Surface, scale_factor: float) -> pygame.Surface:
        """
        Scales and returns the given image
        :param image: the original pygame.Surface
        :param scale_factor: how much to scale the image by
        :return: the scaled image
        """
        if scale_factor == 1: return image
        width, height = image.get_rect().size[0], image.get_rect().size[1]
        return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))


    def extract_platforms(self, source_path='assets/images/jungle tileset.png', scale_factor=1) -> list:
        """
        Extracts platform tiles from the tile sheet and returns them as a list
        NOTE: each tile is 16x16
        :param scale_factor:
        :param source_path: the relative path to the tile sheet
        :return:list of images for each platform tile
        """
        sheet = pygame.image.load(source_path).convert_alpha()
        platform_coords = [(0, 16, 27, 27), (26, 16, 27, 27), (53, 16, 27, 27)]  # left, centre, right
        return [self.scale_image(sheet.subsurface(coords), scale_factor) for coords in platform_coords]

    def extract_images(self, path: str, sprite_width: int, scale_factor=1) -> list:
        """
        Extracts images from a sprite sheet and returns them as a list

        :param scale_factor:
        :param path: relative path to sprite sheet
        :param sprite_width: width of a sprite in pixels
        :return: list of images of the sprite sheets
        """
        sheet = pygame.image.load(path)
        width, h = sheet.get_size()
        sprites = int(width / sprite_width)
        images = []
        for x in range(sprites):
            images.append(self.scale_image(sheet.subsurface(x * sprite_width, 0, sprite_width, h), scale_factor))
        return images

