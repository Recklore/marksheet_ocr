import cv2
import numpy as np


def correct_illumination(img):
    #CLAHE (adaptive histogram equalisation)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(img)


def denoise(img):
    #Median blur (salt and pepper noise removal)

    return cv2.medianBlur(img, ksize=3)


def grayscale_it(img):

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def binarise(img):

    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    threshed = cv2.adaptiveThreshold( img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)
    return threshed


def correct_perspective(img):
    #Canny edge detection + Hough transform

    edges = cv2.Canny(img, 50, 160, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,
                            threshold=50,
                            minLineLength=int(0.2*min(img.shape[:2])),
                            maxLineGap=60)
    if lines is None:
        return img
    

    #Separating horizontal and vertical lines

    horiz = []
    vert = []
    for x1,y1,x2,y2 in lines.reshape(-1,4):
        dx = x2-x1; dy = y2-y1
        angle = abs(np.degrees(np.arctan2(dy, dx)))
        length = np.hypot(dx, dy)
        if angle < 20 and length > 0.2*min(img.shape[:2]):
            horiz.append((x1,y1,x2,y2))
        elif angle > 70 and length > 0.15*min(img.shape[:2]):
            vert.append((x1,y1,x2,y2))

    if not horiz or not vert:
        return img
    

    #Finding extreme most lines
    
    horiz_sorted = sorted(horiz, key=lambda l: (l[1]+l[3])/2)
    vert_sorted = sorted(vert, key=lambda l: (l[0]+l[2])/2)

    top = horiz_sorted[0]
    bottom = horiz_sorted[-1]
    left = vert_sorted[0]
    right = vert_sorted[-1]


    #Getting Border point from lines

    def intersect(l1, l2):
        x1,y1,x2,y2 = l1; x3,y3,x4,y4 = l2
        denom = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if abs(denom) < 1e-6: return None
        px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/denom
        py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/denom
        return [px,py]
    
    tl = intersect(top, left)
    tr = intersect(top, right)
    br = intersect(bottom, right)
    bl = intersect(bottom, left)

    if None in (tl, tr, br, bl):
        return img
    

    #Correcting perspective based on border points 

    def four_point_transform(image, pts):
    
        (tl, tr, br, bl) = pts
        widthA = np.hypot(br[0] - bl[0], br[1] - bl[1])
        widthB = np.hypot(tr[0] - tl[0], tr[1] - tl[1])
        maxWidth = int(max(widthA, widthB))

        heightA = np.hypot(tr[0] - br[0], tr[1] - br[1])
        heightB = np.hypot(tl[0] - bl[0], tl[1] - bl[1])
        maxHeight = int(max(heightA, heightB))

        dst = np.array([[0,0],
                        [maxWidth-1, 0],
                        [maxWidth-1, maxHeight-1],
                        [0, maxHeight-1]], dtype="float32")

        M = cv2.getPerspectiveTransform(pts, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    
    pts = np.array([tl,tr,br,bl], dtype="float32")
    return four_point_transform(img, pts)

def deskew(img):

    #Invert image + projection profile

    if np.mean(img == 255) > 0.5:
        inv_img = cv2.bitwise_not(img)

    best_angle = 0
    best_score = -1

    for angle in np.arange(-10, 10.1, 0.5):
        (h, w) = inv_img.shape
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        rotated = cv2.warpAffine(inv_img, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)

        projection = np.sum(rotated == 255, axis=1)

        score = np.var(projection)

        if score > best_score:
            best_score = score
            best_angle = angle

    (h, w) = img.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), best_angle, 1.0)
    deskewed = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=255)
    
    return deskewed

def preprocess_image(img):

    # Grayscale -> Illumination Correction -> Perspective Correction -> Deskewing ->  Denoise -> Binarisation

    processed_img = grayscale_it(img)
    processed_img = correct_illumination(processed_img)
    processed_img = correct_perspective(processed_img)
    processed_img = deskew(processed_img)
    processed_img = denoise(processed_img)
    processed_img = binarise(processed_img)

    return processed_img

if __name__ == "__main__":
    PATH = input("Enter image path: ")
    img = cv2.imread(PATH)
    preprocess_image(img)