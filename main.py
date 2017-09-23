import glob
import cv2
import codecs
import os
import random


def get_human_part_image(part, rect, image, offset=0):
    org_x1, org_y1, org_x2, org_y2 = rect
    if offset == 0:
        offset = [0, 0, 0, 0]

    rect_width = org_x2 - org_x1
    rect_height = org_y2 - org_y1

    relative_position_of_part_x1 = part[0]
    relative_position_of_part_y1 = part[1]
    relative_position_of_part_x2 = part[2]
    relative_position_of_part_y2 = part[3]

    x1 = org_x1 + rect_width * relative_position_of_part_x1
    y1 = org_y1 + rect_height * relative_position_of_part_y1
    x2 = org_x1 + rect_width * relative_position_of_part_x2
    y2 = org_y1 + rect_height * relative_position_of_part_y2

    rect_width = x2 - x1
    rect_height = y2 - y1

    x1 += rect_width * offset[0]
    y1 += rect_height * offset[1]
    x2 += rect_width * offset[2]
    y2 += rect_height * offset[3]

    image_width = image.shape[1]
    image_height = image.shape[0]

    rect_width = x2 - x1
    rect_height = y2 - y1

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    rect_size = int(max(rect_width, rect_height))

    if rect_size >= image_width:
        raise 'image_width is too small to crop'
    if rect_size >= image_height:
        raise 'image_width is too small to crop'

    x1 = int(center_x - rect_size / 2)
    x2 = int(center_x + rect_size / 2)
    y1 = int(center_y - rect_size / 2)
    y2 = int(center_y + rect_size / 2)

    if x1 < 0:
        x2 = x2 - x1
        x1 = 0  # x1 - x1
    if x2 > image_width - 1:
        x1 = x1 - (x2 - (image_width - 1))
        x2 = x2 - (x2 - (image_width - 1))

    if y1 < 0:
        y2 = y2 - y1  # x1 - x1
        y1 = 0  # y1 - y1
    if y2 > image_height - 1:
        y1 = y1 - (y2 - (image_height - 1))
        y2 = y2 - (y2 - (image_height - 1))

    cropped = []
    cropped = image[y1:y2, x1:x2, :]
    return cropped

def crop_and_save_as_human_parts(annotations_path, images_path, save_path):
    image_name_list = glob.glob(images_path+'/*.png')
    for image_name in image_name_list:
        image_name = image_name[image_name.rfind('/')+1:image_name.rfind('.')]
        rects = []
        with codecs.open(annotations_path+'/'+image_name+'.txt', 'r', "ISO-8859-1") as f:
            for line in f:
                line = line.replace('(', ' ').replace(')', ' ').replace(',', ' ')
                splits = [int(s) for s in line.split() if s.isdigit()]

                if line.rfind('Image size') != -1:
                    image_width = splits[0]
                    image_height = splits[1]
                    image_channels = splits[2]
                elif line.rfind('Bounding box for object') != -1:
                    x1 = splits[1]
                    y1 = splits[2]
                    x2 = splits[3]
                    y2 = splits[4]
                    rects.append([x1, y1, x2, y2])

            image = cv2.imread(images_path + '/' + image_name + '.png')

            try:
                for idx, rect in zip(range(9999), rects):
                    parts = {}
                    parts['head'] = [0.3, 0.0, 0.7, 0.2]
                    parts['upper_body'] = [0.0, 0.0, 1.0, 0.5]
                    parts['upper_body_above_knee'] = [0.0, 0.0, 1.0, 0.75]
                    parts['lower_body_under_shoulder'] = [0.0, 0.3, 1.0, 1.0]
                    parts['lower_body'] = [0.0, 0.5, 1.0, 1.0]
                    parts['full_body'] = [0.0, 0.0, 1.0, 1.0]
                    parts['full_body_without_head'] = [0.0, 0.2, 1.0, 1.0]

                    offsets = {}
                    offsets['center'] = [0., 0., 0., 0.]
                    offsets['wide'] = [-0.1, -0.1, 0.1, 0.1]
                    offsets['left'] = [-0.1, 0., -0.1, 0.]
                    offsets['right'] = [0.1, 0., 0.1, 0.]
                    offsets['top'] = [0., -0.05, 0., -0.05]
                    offsets['bot'] = [0., 0.05, 0., 0.05]
                    offsets['left_top'] = [-0.1, -0.05, -0.1, -0.05]
                    offsets['right_top'] = [0.1, -0.05, 0.1, -0.05]
                    offsets['left_bot'] = [-0.1, 0.05, -0.1, 0.05]
                    offsets['right_bot'] = [0.1, 0.05, 0.1, 0.05]
                    images = []
                    try:
                        for part in parts.keys():
                            for offset in offsets.keys():
                                cropped = get_human_part_image(parts[part], rect, image, offsets[offset])
                                save_filename = save_path + '/' + part + '/' + 'cropped_' + image_name + '_' + offset + '.jpg'
                                try:
                                    os.makedirs(save_filename[:save_filename.rfind('/')])
                                except:
                                    pass
                                cv2.imwrite(save_filename, cropped)
                    except:
                        pass
            except:
                pass

def crop_and_save_as_random(images_path, save_path):
    image_name_list = glob.glob(images_path+'/*.*')
    for image_name in image_name_list:
        image_name_without_extension = image_name[image_name.rfind('/')+1:image_name.rfind('.')]
        image = cv2.imread(image_name)

        image_width = image.shape[1]
        image_height = image.shape[0]
        min_size = min(40, int(image_width / 5)) - 1
        max_size = min(200, int(image_width / 2)) - 1

        cv2.imshow('image', image)

        for idx in range(100):
            rect_size = random.randint(min_size, max_size)
            x = random.randint(0, image_width - rect_size - 1)
            y = random.randint(0, image_height - rect_size - 1)
            cropped = image[y:y+rect_size, x:x+rect_size,:]
            save_filename = save_path + '/' + 'cropped_' + image_name_without_extension + '_' + '%06d' % idx + '.jpg'
            try:
                os.makedirs(save_filename[:save_filename.rfind('/')])
            except:
                pass
            cv2.imwrite(save_filename, cropped)
            #
            # cv2.imshow('cropped', cropped)
            # cv2.waitKey(0)

if __name__ == "__main__":
    print('Current working directory : ', os.getcwd())

    print('Saving start !')
    # Absolute path recommended
    annotations_path = '/home/yildbs/Data/INRIA/Train_original/annotations/'
    images_path = '/home/yildbs/Data/INRIA/Train_original/pos/'
    save_path = './output_train_pos/'
    crop_and_save_as_human_parts(annotations_path, images_path, save_path)
    print('Saving end')

    print('Saving start !')
    # Absolute path recommended
    annotations_path = '/home/yildbs/Data/INRIA/Test_original/annotations/'
    images_path = '/home/yildbs/Data/INRIA/Test_original/pos/'
    save_path = './output_test_pos/'
    crop_and_save_as_human_parts(annotations_path, images_path, save_path)
    print('Saving end')

    print('Saving start !')
    images_path = '/home/yildbs/Data/INRIA/Train_original/neg/'
    save_path = './output_train_neg/'
    crop_and_save_as_random(images_path, save_path)
    print('Saving end')

    print('Saving start !')
    images_path = '/home/yildbs/Data/INRIA/Test_original/neg/'
    save_path = './output_text_neg/'
    crop_and_save_as_random(images_path, save_path)
    print('Saving end')


    print('Program end')

