#include "EdtReader.h"
#include <iostream>
#include <stdexcept>

#include "lodepng.h"

using namespace std;

void encodeTwoSteps(const char* filename, std::vector<unsigned char>& image, unsigned width, unsigned height) {
  std::vector<unsigned char> png;

  unsigned error = lodepng::encode(png, image, width, height);
  if(!error) lodepng::save_file(png, filename);

  //if there's an error, display it
  if(error) std::cout << "encoder error " << error << ": "<< lodepng_error_text(error) << std::endl;
}

int main(int argc, char* argv[])
{
    cout << "Edt Image generation example\n";
    cout << "Provided "<<argc<<" arguments.\n";

    char CT_scan [80];
    char structure[80];
    char resolution[5];
    strcpy(CT_scan, argv[1]);
    strcpy(structure, argv[2]);
    strcpy(resolution, argv[3]);
    cout<<"CT_scan: "<<CT_scan<<"\n";
    cout<<"structure: "<<structure<<"\n";
    cout<<"resolution: "<<resolution<<"\n";
    
    char input_file_name[100];
    cout<<"This file should be run from project root.\n";
    sprintf(input_file_name, "./resources/edt_grids/%s_%s/%s.edt", &CT_scan, &resolution, &structure, &resolution);
    
    char error_msg[100];
    sprintf(error_msg, "Reading %s", &input_file_name);
    cout << error_msg << endl;

    float *values_buffer;
    unsigned int res[3];

    Array3d<float> *edt_grid;
    edt_reader(input_file_name, &values_buffer, res);

    edt_grid = new Array3d<float>(values_buffer, res);

    cout << "Resolution:" << res[0] << ","  << res[1] << "," << res[2] << endl;

    unsigned width = res[0], height = res[1];
    std::vector<unsigned char> image;
    image.resize(width * height * 4);
    double max_edt = __DBL_MIN__;

    // // figure out the EDT range
    // double mx = __DBL_MIN__;
    // double mn = __DBL_MAX__;
    // for (unsigned k=0; k<res[2]; k++) {
    //     for (unsigned y=0; y<res[1]; y++) {
    //         for (unsigned x=0; x<res[0]; x++) {
    //             double tmp=(*edt_grid)(x,y,k);
    //             mx = max(tmp, mx);
    //             mn = min(tmp,mn);
    //         }
    //     }
    // }
    // std::cout<<"MAX "<< mx<<std::endl;
    // std::cout<<"MIN "<<mn<<std::endl;
    // int pos_scale = (int)mx+1;
    // int neg_scale = (-1*(int)mn)+1;
    // std::cout<<"+ "<<pos_scale<<std::endl;
    // std::cout<<"- "<<neg_scale<<std::endl;


    int scale=600;

    for (unsigned int z = 0; z < res[2]; z++){
        for(unsigned y = 0; y < height; y++){
            for(unsigned x = 0; x < width; x++) {
                double tmp = (*edt_grid)(x,y,z) * 255/scale;
                if (tmp > max_edt) max_edt =tmp/255 * scale;
                if (tmp > 255) cout << "[ERROR]edt distance over "<< scale  << " mm(" << max_edt << ")" << endl;

                if (tmp > 0) {
                    image[4 * width * y + 4 * x + 0] = tmp; //R
                }
                if (tmp < 0) image[4 * width * y + 4 * x + 2] = -tmp; //B
                // image[4 * width * y + 4 * x + 1] = 0; //G
                image[4 * width * y + 4 * x + 3] = 255;  //A
            }
        }

        // Create imgaes in the output file
        string index = to_string(z);
        char out_filename[200];
        sprintf(out_filename, "./resources/edt_grids/%s_%s/%s_%s/edtplane_%s.png", &CT_scan, &resolution, &structure, &resolution, &index[0]);
        encodeTwoSteps(out_filename, image, width, height);
    }


    // for (unsigned int z = 0; z < res[2]; z++){
    //     for(unsigned y = 0; y < height; y++){
    //         for(unsigned x = 0; x < width; x++) {
    //             double edt = (*edt_grid)(x,y,z);
    //             double pxl = edt * 255;
    //             if (edt>0) {
    //                 pxl = pxl / pos_scale;
    //                 image[4 * width * y + 4 * x + 0] = pxl; //R
    //             }
    //             else {
    //                 pxl = pxl / neg_scale;
    //                 image[4 * width * y + 4 * x + 2] = -pxl; //B
    //             }
    //             image[4 * width * y + 4 * x + 3] = 255;  //A
    //         }
    //     }

    //     // Create imgaes in the output file
    //     string index = to_string(z);
    //     char out_filename[200];
    //     sprintf(out_filename, "./resources/edt_grids/%s_%s/%s_%s/edtplane_%s.png", &CT_scan, &resolution, &structure, &resolution, &index[0]);
    //     encodeTwoSteps(out_filename, image, width, height);
    // }


    
    return 0;
}