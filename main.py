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

        with codecs.open(annotations_path+'/'+image_name+'.txt', 'r', "utf-8") as f:
            for line in f:
                bbb = line[0]
                aaa =  line.split(' ,()')
                splits = [int(s) for s in line.split() if s.isdigit()]

                if line.rfind('Image size') != -1:
                    image_size_x = splits[1]
                    image_size_y = splits[2]

