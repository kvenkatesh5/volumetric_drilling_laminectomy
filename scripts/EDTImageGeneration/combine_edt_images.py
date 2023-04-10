from PIL import Image
import numpy as np
from pathlib import Path
import glob
import click


def load_images(path: Path, verbose: bool = False):
    if not path.exists():
        print(f"[Error] {path} does not exist.")
        exit(0)

    img_list = []
    # Assuming that the images are saved in png format
    num_imgs = len(glob.glob(str(path / '*.png')))
    if verbose:
        print(f"number of images:{num_imgs}.")

    for index in range(num_imgs): 
        file_name = 'edtplane_' + str(index) + '.png'
        file_name = path/file_name
        img = Image.open(file_name)
        img = img.convert('RGB')
        img_list.append(np.array(img))

    return img_list

def save_images(path: Path, img_list: list):
    if not path.exists():
        print(f"[Error] {path} does not exist.")
        exit(0)
    
    for index, img in enumerate(img_list):
        file_name = 'edtplane_' + str(index) + '.png'
        Image.fromarray(img).save(path / file_name)
    

@click.command()
@click.option("--input_dir", required=True, multiple=True, help="multiple paths(>1) to source edt_images")
@click.option("--output_dir", required=True, help="path to output folder.")
def combine_edt_images(input_dir: Path, output_dir: Path):

    # Check whether you have more than 1 edt files declared to combine
    # if (len(input_dir) < 2):
    #     print(f"[Error] Declare more than one to combine the edts.")
    #     exit(0)
    assert len(input_dir) > 1, "[Error] Declare more than one to combine the edts."
    img_input_lists = []
    
    for path in input_dir:
        path = Path("/home/virtualdrilling/volumetric_drilling") / path
        img_tmp_list = load_images(path=path)
        img_input_lists.append(img_tmp_list)

    # Combine the lists
    combined_img_list = []
    for index, img_list in enumerate(img_input_lists):
        if index == 0:
            combined_img_list = img_list
            print(f"combining {1}/{len(img_input_lists)}....")

        else:
            print(f"combining {index+1}/{len(img_input_lists)}....")
            # Check the image size and number
            assert len(combined_img_list) == len(img_list), "[Error] the number of the edt images does not match."
            assert combined_img_list[0].shape == img_list[0].shape,  "[Error] the size of the edt image does not match({combined_img_list[0].shape}, {img_list[0].shape})."

            for i in range(len(combined_img_list)):
                for x in range(combined_img_list[i].shape[0]):
                    for y in range(combined_img_list[i].shape[1]):
                        # Check for the R channel and get the mimnimum value
                        if (combined_img_list[i][x, y][0] > img_list[i][x, y][0]):
                            combined_img_list[i][x, y][0] = img_list[i][x,y][0]
                        
                        if(combined_img_list[i][x, y][1] < img_list[i][x, y][1]):
                            combined_img_list[i][x, y][1] = img_list[i][x, y][1]

    # Save the img_list
    output_dir = Path("/home/virtualdrilling/volumetric_drilling") / output_dir
    print(f"Saving images to {output_dir}...")
    save_images(path=output_dir, img_list=combined_img_list)


if __name__ == "__main__":
    combine_edt_images()
