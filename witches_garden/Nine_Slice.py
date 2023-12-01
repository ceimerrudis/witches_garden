import pygame

def Nine_Slice_Rect(rect, left, top, right, bottom, img_width = False, img_height = False):
    width = rect.w - left - right
    height = rect.h - top - bottom 
    if (img_height == False or img_height == False):
        img_width = width
        img_height = height

    top_left_slice = pygame.Rect(       rect.x + 0,             rect.y + 0,             left,   top)
    
    #
    top_slice_total = pygame.Rect(            rect.x + left,          rect.y + 0,             width,  top)
    top_slice = []
    x = 0
    while x < top_slice_total.width:
        w = top_slice_total.width - x
        if w > img_width:
            w = img_width
        top_slice.append((pygame.Rect(top_slice_total.x + x, top_slice_total.y, w, top), 1))
        x += img_width

    top_right_slice = pygame.Rect(      rect.x + left + width,  rect.y + 0,             right,  top)
    
    #
    left_slice_total = pygame.Rect(           rect.x + 0,             rect.y + top,           left,   height)
    left_slice = []
    y = 0
    while y < left_slice_total.height:
        h = left_slice_total.height - y
        if h > img_height:
            h = img_height
        left_slice.append((pygame.Rect(left_slice_total.x, left_slice_total.y + y, left, h), 3))
        y += img_height

    #
    center_total = pygame.Rect(         rect.x + left,          rect.y + top,           width,  height)
    center = []
    y = 0
    while y < center_total.height:
        x = 0
        while x < center_total.width:
            w = center_total.width - x
            if w > img_width:
                w = img_width

            h = center_total.height - y
            if h > img_height:
                h = img_height
            center.append((pygame.Rect(center_total.x + x, center_total.y + y, w, h), 4))
            x += img_width
        y += img_height

    #
    right_slice_total = pygame.Rect(          rect.x + left + width,  rect.y + top,           right,  height)
    right_slice = []
    y = 0
    while y < right_slice_total.height:
        h = right_slice_total.height - y
        if h > img_height:
            h = img_height
        right_slice.append((pygame.Rect(right_slice_total.x, right_slice_total.y + y, right, h), 5))
        y += img_height

    bottom_left_slice = pygame.Rect(    rect.x + 0,             rect.y + top + height,  left,   bottom)
    
    #
    bottom_slice_total = pygame.Rect(         rect.x + left,          rect.y + top + height,  width,  bottom)
    bottom_slice = []
    x = 0
    while x < bottom_slice_total.width:
        w = bottom_slice_total.width - x
        if w > img_width:
            w = img_width
        bottom_slice.append((pygame.Rect(bottom_slice_total.x + x, bottom_slice_total.y, w, bottom), 7))
        x += img_width


    bottom_right_slice = pygame.Rect(   rect.x + left + width,  rect.y + top + height,  right,  bottom)

    ktv = []
    ktv.append((top_left_slice, 0))
    ktv += top_slice
    ktv.append((top_right_slice, 2))
    ktv += left_slice
    ktv += center
    ktv += right_slice
    ktv.append((bottom_left_slice, 6))
    ktv += bottom_slice
    ktv.append((bottom_right_slice, 8))
    return ktv

def nine_slice(image, left, top, right, bottom):
    image_rect = image.get_rect()
    sliced_image_rect = Nine_Slice_Rect(image_rect, left, top, right, bottom)

    result = []
    for rect in sliced_image_rect:
        result.append(image.subsurface(rect[0]))
    
    return result, image_rect.w - left - right, image_rect.h - top - bottom 
