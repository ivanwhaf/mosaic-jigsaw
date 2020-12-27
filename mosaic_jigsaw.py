import os
import time
import cv2
import numpy as np

raw_pic_path = 'raw.jpg'
source_pic_path = 'source'


def calculate_avg_rgb(img):
    # calculate img three rgb average value
    avg_b = np.mean(img[:, :, 0])
    avg_g = np.mean(img[:, :, 1])
    avg_r = np.mean(img[:, :, 2])
    return avg_r, avg_g, avg_b


def create_source_pic_bank(source_pic_path):
    # picture material
    sources = []
    files = os.listdir(source_pic_path)
    for pic_name in files:
        pic_path = os.path.join(source_pic_path, pic_name)
        print(pic_path)
        pic = cv2.imread(pic_path)
        try:
            avg_r, avg_g, avg_b = calculate_avg_rgb(pic)
        except:
            continue
        dic = {'pic_path': pic_path, 'pic': pic,
               'avg_rgb': [avg_r, avg_g, avg_b]}
        sources.append(dic)
    return sources


def find_nearest_pic(pic, sources):
    # find child picture's most like picture in sources
    c_r, c_g, c_b = calculate_avg_rgb(pic)
    nearest_idx = 0
    nearest_distance = 255
    for i, source in enumerate(sources):
        s_r, s_g, s_b = source['avg_rgb']
        distance = abs(s_r-c_r)+abs(s_g-c_g)+abs(s_b-c_b)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_idx = i
    return nearest_idx


def main():
    raw_pic = cv2.imread(raw_pic_path)
    h, w, _ = raw_pic.shape
    print('Raw picture weight:', w, 'height:', h)

    sources = create_source_pic_bank(source_pic_path)
    print('Sources loaded...')

    side1 = 10
    mosaic_pic_index = []  # index of most like pic's index
    for j in range(h//side1):
        t = []
        for i in range(w//side1):
            child_pic = raw_pic[j*side1:j*side1+side1, i*side1:i*side1+side1]
            idx = find_nearest_pic(child_pic, sources)
            t.append(idx)
        mosaic_pic_index.append(t)
    print('Find all nearest pictures of children pictures!')

    side2 = 50
    target_pic = np.zeros(
        (len(mosaic_pic_index)*side2, len(mosaic_pic_index[0])*side2, 3))

    for i in range(len(mosaic_pic_index)):
        for j in range(len(mosaic_pic_index[0])):
            nearest_pic = sources[mosaic_pic_index[i][j]]['pic']
            nearest_pic = cv2.resize(nearest_pic, (side2, side2))
            target_pic[i*side2:i*side2+side2, j*side2:j *
                       side2+side2, :] = nearest_pic[:, :, ]

    cv2.imwrite('target.jpg', target_pic)
    print('New picture weight:',
          target_pic.shape[1], 'height:', target_pic.shape[0])


if __name__ == "__main__":
    main()
