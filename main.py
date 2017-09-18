import glob
import cv2
import codecs


if __name__ == "__main__":
    # Absolute path recommended
    annotations_path = '/home/yildbs/Data/INRIA/Train_original/annotations/'
    images_path = '/home/yildbs/Data/INRIA/Train_original/pos/'

    image_name_list = glob.glob(images_path+'/*.png')

    fit_to_ratio = True
    h_over_w = 1.0
    margin_pixel = 0
    margin_ratio = 1.0

    for image_name in image_name_list:
        image_name = image_name[image_name.rfind('/')+1:image_name.rfind('.')]
        image_size_x = 0
        image_size_y = 0
        image_channels = 0
        rects = []
        with codecs.open(annotations_path+'/'+image_name+'.txt', 'r', "ISO-8859-1") as f:
            for line in f:
                line = line.replace('(', ' ').replace(')', ' ').replace(',', ' ')
                splits = [int(s) for s in line.split() if s.isdigit()]

                if line.rfind('Image size') != -1:
                    image_size_x = splits[0]
                    image_size_y = splits[1]
                    image_channels = splits[2]
                elif line.rfind('Bounding box for object') != -1:
                    x1 = splits[1]
                    y1 = splits[2]
                    x2 = splits[3]
                    y2 = splits[4]
                    rects.append([x1, y1, x2, y2])

            image = cv2.imread(images_path + '/' + image_name + '.png')

            try:
                cv2.destroyAllWindows()
                for idx, rect in zip(range(9999), rects):
                    x1, y1, x2, y2 = rect

                    width = x2 - x1
                    height = y2 - y1

                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2

                    if width < height:
                        height = height * margin_ratio + margin_pixel
                        width = height / h_over_w
                    else:
                        width = width * margin_ratio + margin_pixel
                        height = width * h_over_w

                    width = int(width)
                    height = int(height)
                    x1 = int(cx - width / 2)
                    x2 = int(cx + width / 2)
                    y1 = int(cy - height / 2)
                    y2 = int(cy + height / 2)

                    if x1 < 0:
                        x2 = x2 - x1
                        x1 = 0 #x1 - x1
                    if x2 > image_size_x - 1:
                        x1 = x1 - (x2 - (image_size_x - 1))
                        x2 = x2 - (x2 - (image_size_x - 1))
                    if x1 < 0:
                        raise 'image_size_x is too small to crop'
                    if x2 > image_size_x - 1:
                        raise 'image_size_x is too small to crop'

                    if y1 < 0:
                        y2 = y2 - y1 # x1 - x1
                        y1 = 0 #y1 - y1
                    if y2 > image_size_y - 1:
                        y1 = y1 - (y2 - (image_size_y - 1))
                        y2 = y2 - (y2 - (image_size_y - 1))

                    cropped = []
                    cropped = image[y1:y2, x1:x2,:]
                    cv2.imshow('cropped_'+str(idx), cropped)
                cv2.imshow('image', image)
                cv2.waitKey(0)
            except:
                pass

        # print(image_name.rjust(20), '<', str(image_size_x).rjust(4), ', ', image_size_y, '> ', rects)