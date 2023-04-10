#include <iostream>
#include <vector>
#include "EdtReader/EdtReader.h"
#include <unordered_map>

// To display color
#include <algorithm>
#include <sstream>
#include <iterator>

#define number_of_edt 1

using std::string;
using std::vector;

class EdtContainer
{
public:
    float m_dist_object;
    string path;
    string name;
    Array3d<float> *edt_grid;
    vector<int> rgb;
    float force_thres;
    float audio_thres;

    EdtContainer() {}
    EdtContainer(string p, string name, const vector<int> &rgb, const float force_thres=1.0, const float audio_thres=1.0)
    {
        this->name = name;
        this->path = p;
        this->m_dist_object = 0.0;
        this->rgb = std::vector<int>(rgb.begin(), rgb.end());
        this->force_thres = force_thres;
        this->audio_thres = audio_thres;
    }

    void load_grid(string edt_root)
    {
        string complete_path = edt_root+this->path;

        float *values_buffer;
        unsigned int res[3];
        edt_reader(complete_path, &values_buffer, res);
        this->edt_grid = new Array3d<float>(values_buffer, res);

        // I will keep this error here to remember the importance of learning how to allocate memory in c++.
        //        Array3d<float> edtGrid(values_buffer, res);
        //        this->edt_grid = edtGrid;
    }
    void get_resolution(unsigned int *resolution)
    {
        *resolution = (this->edt_grid)->res[0];
        *(resolution + 1) = (this->edt_grid)->res[1];
        *(resolution + 2) = (this->edt_grid)->res[2];
    }
    void print_info()
    {
        // RGB vect to string
        std::ostringstream vts;
        std::copy(this->rgb.begin(), this->rgb.end(),
                  std::ostream_iterator<int>(vts, ", "));

        printf("name: %s || path: %s || color: %s \n", this->name.c_str(), this->path.c_str(), vts.str().c_str());
    }
    void setThreshold(float force_thres, float audio_thres)
    {
        this->force_thres = force_thres;
        this->audio_thres = audio_thres;
    }
};

// std::string edt_paths[number_of_edt] = {"SpinalCord.edt"};
//                                         // "./edt_grids/Bone.edt"};

// std::string edt_names[number_of_edt] = {"SpinalCord"};
//                                         // "Bone"};
std::string edt_paths[number_of_edt] = {"Vertebral_foramen.edt"};
// std::string edt_paths[number_of_edt] = {"L1_minus_drilling.edt"};
                                        // "./edt_grids/Bone.edt"};

std::string edt_names[number_of_edt] = {"Vertebral_foramen"};
// std::string edt_names[number_of_edt] = {"L1_minus_drilling"};
                                        // "Bone"};

// std::string edt_paths[number_of_edt] = {"L1_minus_drilling.edt"};
// std::string edt_names[number_of_edt] = {"L1_minus_drilling"};

// Save colors
class EdtList
{
public:
    EdtContainer list[number_of_edt];
    std::unordered_map<string, vector<int>> color_map;
    std::unordered_map<string, vector<double>> thres_map;
    int size = number_of_edt;

    EdtList()
    {
        color_map["Vertebral_foramen"] = vector<int>{84, 188, 255};
        thres_map["Vertebral_foramen"] = vector<double>{1.0,1.0};

        // color_map["L1_minus_drilling"] = vector<int>{84, 188, 255};
        // color_map["Bone"] = vector<int>{255, 249, 219};//16
        // thres_map["L1_minus_drilling"] = vector<double>{1.0,1.0};

       

        

        printf("constructor\n");
        for (int i = 0; i < number_of_edt; i++)
        {
            printf("loading %d edt\n", i);
            cout << edt_paths[i] << endl;
            EdtContainer cont(edt_paths[i], edt_names[i], color_map[edt_names[i]], thres_map[edt_names[i]][0], thres_map[edt_names[i]][1]);

            list[i] = cont;
        }
    }

    void load_all_grids(string edt_root)
    {
        for (int i = 0; i < number_of_edt; i++)
        {   
            std::cout << (edt_root) << std::endl;
            this->list[i].load_grid(edt_root);
        }
    }
    void print_info()
    {
        printf("------------------------\n");
        printf("Printing edt information\n");
        printf("------------------------\n");
        for (int i = 0; i < number_of_edt; i++)
        {
            this->list[i].print_info();
        }
    }
};
