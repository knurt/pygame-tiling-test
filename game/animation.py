# Problem: An Animation object doesn't make any sense without frames
# so maybe they should be commited in the constructor.


class Animation:
    
    def __init__(self, order):
        self.__order = order
        self.__frames = []


    def add_frame(self, image, rect, duration, offset):
        self.__frames.append(Animationframe(image, rect, duration, offset))

        # initializing the index when the first frame is added
        if len(self.__frames) == 1:
            self.__curr_index = 0
            self.__curr_delay = self.__frames[0].duration


    def show(self, surface, pos):
        # abbreviations
        ci = self.__curr_index
        image_index = self.__order[ci]
        curr_img = self.__frames[ci].image
        curr_rect = self.__frames[ci].rect

        pos = (
                pos[0] - self.__frames[ci].offset[0],
                pos[1] - self.__frames[ci].offset[1])

        surface.blit(curr_img, pos, curr_rect)

        self.__curr_delay -= 1
        if self.__curr_delay <= 0:
            ci += 1
            if ci >= len(self.__order):
                ci = 0
            self.__curr_delay = self.__frames[ci].duration

        self.__curr_index = ci
        
        
        
class Animationframe:
    
    def __init__(self, image, rect, duration, offset):
        """
        image: of the type 'surface'
        rect: rectangle defining the section of the image displayed
        duration: how many frames the animationstate lasts
        offset: x/y-tuple, defines offset
        """
        self.image = image
        self.rect = rect
        self.duration = duration
        self.offset = offset

        
