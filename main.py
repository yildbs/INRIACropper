import glob
import cv2
import codecs


if __name__ == "__main__":
    # Absolute path recommended
    annotations_path = '/home/yildbs/Data/INRIA/Train_original/annotations/'
    images_path = '/home/yildbs/Data/INRIA/Train_original/pos/'

    image_name_list = glob.glob(images_path+'/*.png')

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
        # print(image_name.rjust(20), '<', str(image_size_x).rjust(4), ', ', image_size_y, '> ', rects)

        image = cv2.imread(images_path+'image_name'+'.png')


        for rect in rects:
            []