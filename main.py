import glob
import cv2
import codecs


def get_part_image(part, rect, image, offset=0):
    org_x1, org_y1, org_x2, org_y2 = rect
    if offset == 0:
        offset = [0, 0, 0, 0]

    offset_x1, offset_y1, offset_x2, offset_y2 = offset
    relative_position_of_part = {}
    relative_position_of_part['head'] = [0.3, 0.0, 0.7, 0.2]
    relative_position_of_part['upper_body'] = [0.0, 0.0, 1.0, 0.5]
    relative_position_of_part['lower_body'] = [0.0, 0.5, 1.0, 1.0]
    relative_position_of_part['full_body'] = [0.0, 0.0, 1.0, 1.0]
    relative_position_of_part['full_body_with_head'] = [0.0, 0.2, 1.0, 1.0]

    rect_width = org_x2 - org_x1
    rect_height = org_y2 - org_y1

    relative_position_of_part_x1 = relative_position_of_part[part][0] * (1.0 + offset_x1)
    relative_position_of_part_y1 = relative_position_of_part[part][1] * (1.0 + offset_y1)
    relative_position_of_part_x2 = relative_position_of_part[part][2] * (1.0 + offset_x2)
    relative_position_of_part_y2 = relative_position_of_part[part][3] * (1.0 + offset_y2)

    x1 = org_x1 + rect_width * relative_position_of_part_x1
    y1 = org_y1 + rect_height * relative_position_of_part_y1
    x2 = org_x1 + rect_width * relative_position_of_part_x2
    y2 = org_y1 + rect_height * relative_position_of_part_y2

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    rect_width = x2 - x1
    rect_height = y2 - y1

    image_width = image.shape[1]
    image_height = image.shape[0]

    rect_size = int(max(rect_width, rect_height))
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

    if x1 < 0:
        raise 'image_width is too small to crop'
    if x2 > image_width - 1:
        raise 'image_width is too small to crop'

    if y1 < 0:
        y2 = y2 - y1  # x1 - x1
        y1 = 0  # y1 - y1
    if y2 > image_height - 1:
        y1 = y1 - (y2 - (image_height - 1))
        y2 = y2 - (y2 - (image_height - 1))

    cropped = []
    cropped = image[y1:y2, x1:x2, :]
    return cropped


if __name__ == "__main__":
    # Absolute path recommended
    annotations_path = '/home/yildbs/Data/INRIA/Train_original/annotations/'
    images_path = '/home/yildbs/Data/INRIA/Train_original/pos/'
    save_path = './output_train/'

    # annotations_path = '/home/yildbs/Data/INRIA/Test_original/annotations/'
    # images_path = '/home/yildbs/Data/INRIA/Test_original/pos/'
    # save_path = './output_test/'

    image_name_list = glob.glob(images_path+'/*.png')

    fit_to_ratio = True
    h_over_w = 1.0
    margin_pixel = 0
    margin_ratio = 1.0

    for image_name in image_name_list:
        image_name = image_name[image_name.rfind('/')+1:image_name.rfind('.')]
        image_width = 0
        image_height = 0
        image_channels = 0
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
                cv2.destroyAllWindows()
                for idx, rect in zip(range(9999), rects):
                    parts = ['head', 'upper_body', 'lower_body', 'full_body', 'full_body_head']
                    offsets = {}
                    offsets['center'] = [0., 0., 0., 0.]
                    offsets['broad'] = [-0.1, -0.1, 0.1, 0.1]
                    offsets['left'] = [-0.1, 0., -0.1, 0.]
                    offsets['right'] = [0.1, 0., 0.1, 0.]
                    offsets['top'] = [0., -0.1, 0., -0.1]
                    offsets['bot'] = [0., 0.1, 0., 0.1]
                    offsets['left_top'] = [-0.1, -0.1, -0.1, -0.1]
                    offsets['right_top'] = [0.1, -0.1, 0.1, -0.1]
                    offsets['left_bot'] = [-0.1, 0.1, -0.1, 0.1]
                    offsets['right_bot'] = [0.1, 0.1, 0.1, 0.1]

                    images = []
                    try:
                        for part in parts:
                            cropped = get_part_image(part, rect, image, offsets['left_top'])
                            # images.append([part, cropped])
                            cv2.imshow(part, cropped)
                    # save_filename = save_path + image_name + '_cropped_' + '%06d' % idx + '.jpg'
                    # cv2.imwrite(save_filename, cropped)
                    # print('Cropped image is saved at ', save_filename)
                    except:
                        pass

                    cv2.waitKey(0)

            except:
                pass

