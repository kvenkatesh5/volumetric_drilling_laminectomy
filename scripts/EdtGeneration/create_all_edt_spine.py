import os
import re
from pathlib import Path
import click

@click.command()
@click.option('--input', help='Input in resources/volumes ex) spine1_512')
@click.option('--output', help='output directory. ex) edt_grids_256_spine1')

def create_edt_spine(input, output):

    # Pipelining create_list_of_images.py into this script
    def create_image_list_file(root):
        files = []
        for f in Path(root).glob("*.png"):
            step = re.findall("[0-9]+", f.name)
            if len(step) > 0:
                files.append([int(step[0]), str(f.resolve())])

        # Sort files
        files = sorted(files, key=lambda x: x[0])

        # Create txt
        f = Path(root)
        f = f / f.with_suffix(".txt").name

        with open(f, "w") as f_h:
            for s, name in files:
                f_h.write(name + "\n")

        print(f"saving to {f}")
        print(files[:4])
    
    create_image_list_file(Path("./resources/volumes/" + input))

    # EDT generation
    edtexec_p = Path("./../EDT/cmake-build/bin/EDTFromGrid")
    imglist_p = Path("./resources/volumes/" + input + "/" + input  + ".txt")

    print("Creating image using:", imglist_p)


    for name, value in spine_dict.items():
        print(f"generate edt for {name}. ({value})")

        dst_p = Path(f"./" + output + "/" + name + ".edt")
        # Execute command to generate EDT.
        cmd = f"{edtexec_p} --in {imglist_p} --id {value} --out {dst_p}"
        print(f"executing: {cmd}")
        os.system(cmd)


# spine_dict = {
#     "Vertebral_foramen": "177, 121, 100", #181 228 255",
#     "L1_minus_drilling": "77,  63,  0",# "219 244 20",
#     "L2_minus_drilling": "110, 184, 209", #182 156 219",
#     "L3_minus_drilling": "188, 65, 28", #214 230 130",
# }

# Colors using colors_for_segmentation file
# EDTs should be made based on a visually noncolored segmentation 
spine_dict = {
    "Vertebral_foramen": "241, 214, 145",
    "L1_minus_drilling": "241, 215, 144",
    "L2_minus_drilling": "240, 215, 145",
    "L3_minus_drilling": "242, 213, 146",
    "L4_minus_drilling": "242, 215, 145",
    # bottom boundary pieces to ensure back plane EDTs
    # "L1_bottom_boundary": "0, 0, 255",
    # "L2_bottom_boundary": "0, 255, 0",
    # "L3_bottom_boundary": "255, 0, 0",
}

# # our shot in the dark
# spine_dict = {
#     "Vertebral_foramen": "241, 214, 145",
#     "L1_minus_drilling": "0, 0, 254",
#     "L2_minus_drilling": "0, 254, 0",
#     "L3_minus_drilling": "254, 0, 0",
#     "L4_minus_drilling": "242, 215, 145",
# }


# IN CASES OF ERROR
# 1) is the segment occluded, hence color is mixed with another?

if __name__ == "__main__":
    create_edt_spine()