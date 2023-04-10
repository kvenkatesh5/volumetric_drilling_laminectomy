import os
from pathlib import Path

anatomy_dict = {
    "Bone": "255 249 219",
    "Malleus": "233 0 255",
    "Incus": "0 255 149",
    "Stapes": "63 0 255",
    "Bony_Labyrinth": "91 123 91",
    "IAC": "244 142 52",  # orange structure
    "Superior_Vestibular_Nerve": "255 191 135",
    "Inferior_Vestibular_Nerve": "121 70 24",
    "Cochlear_Nerve": "219 244 52",
    "Facial_Nerve": "244 214 49",
    "Chorda_Tympani": "151 131 29",
    "ICA": "216 100 79",
    "Sinus_+_Dura": "110 184 209",  # blue structure
    "Vestibular_Aqueduct": "91 98 123",
    "TMJ": "100 0 0",  # dark red structure
    "EAC": "255 225 214",  # Other big structure in the front
}

if __name__ == "__main__":



    edtexec_p = Path("./../EDT/cmake-build/bin/EDTFromGrid")
    # imglist_p = Path("./resources/volumes/ear3_171/ear3_171.txt")
    # imglist_p = Path("./resources/volumes/ear3_256/ear3_256.txt")
    # imglist_p = Path("./resources/volumes/ear3_512/ear3_512.txt")
    # imglist_p = Path("./resources/volumes/ear3_512_2/ear3_512_2.txt")
    # imglist_p = Path("./resources/volumes/ear3_512_4/ear3_512_4.txt")

    CTname = "RT143_256"
    # CTname = "RT147_256"
    # CTname = "RT138_256"
    # CTname = "LT143_256"
    # CTname = "LT151_256"

    imglist_p = Path("./resources/volumes/" + CTname +"/" + CTname +".txt")

    os.system("echo Hello from the other side!")
    os.system("ls")

    for name, value in anatomy_dict.items():
        print(f"generate edt for {name}. ({value})")

        # dst_p = Path(f"./edt_grids/{name}.edt")
        # dst_p = Path(f"./edt_grids_LT151/{name}.edt")
        dst_p = Path(f"./edt_grids_" + CTname + "/" + name + ".edt")
        # Execute command to generate EDT.
        cmd = f"{edtexec_p} --in {imglist_p} --id {value} --out {dst_p}"
        print(f"executing: {cmd}")
        os.system(cmd)
