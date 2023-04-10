uniform vec3 uMinCorner;
uniform vec3 uMaxCorner;
uniform vec3 uTextureScale;
uniform vec3 uGradientDelta;
uniform sampler3D uVolume;
uniform sampler3D sdfVolume;
uniform sampler3D sdfVolume1;
uniform sampler2DShadow shadowMap;
uniform float uIsosurface;
uniform float uResolution;

varying vec4 vPosition;
uniform bool uSmoothVolume;
uniform int uSmoothingLevel;
uniform int uEnableShadow;

uniform vec3 uL_13;
uniform vec3 uL_2;
uniform vec3 uL_46;
uniform vec3 uL_5;

uniform vec3 uUnit;
uniform vec3 uThres;


vec3 dx = vec3(uGradientDelta.x, 0.0, 0.0);
vec3 dy = vec3(0.0, uGradientDelta.y, 0.0);
vec3 dz = vec3(0.0, 0.0, uGradientDelta.z);

float c_value = 0.4;

//----------------------------------------------------------------------
// Finds the entering intersection between a ray e1+d and the volume's
// bounding box.
//----------------------------------------------------------------------

float entry(vec3 e1, vec3 d)
{
    float t = distance(uMinCorner, uMaxCorner);

    vec3 a = (uMinCorner - e1) / d;
    vec3 b = (uMaxCorner - e1) / d;
    vec3 u = min(a, b);

    return max( max(-t, u.x), max(u.y, u.z) );
}


float isoValue(vec3 tc){
  return texture3D(uVolume, tc).a;
}

//----------------------------------------------------------------------
// Estimates the intensity gradient of the volume in model space
//----------------------------------------------------------------------

vec3 gradient(vec3 tc)
{
    vec3 nabla = vec3(
        isoValue(tc + dx) - isoValue(tc - dx),
        isoValue(tc + dy) - isoValue(tc - dy),
        isoValue(tc + dz) - isoValue(tc - dz)
    );

    return (nabla / uGradientDelta) * uTextureScale;
}


//----------------------------------------------------------------------
//  Performs interval bisection and returns the value between a and b
//  closest to isosurface. When s(b) > s(a), direction should be +1.0,
//  and -1.0 otherwise.
//----------------------------------------------------------------------

vec3 refine(vec3 a, vec3 b, float isosurface, float direction)
{
    for (int i = 0; i < 6; ++i)
    {
        vec3 m = 0.5 * (a + b);
        float v = (texture3D(uVolume, m).a - isosurface) * direction;
        if (v >= 0.0)   b = m;
        else            a = m;
    }
    return b;
}

vec4 remove_segment(vec4 color, float sdf_distance, float sdf_distance1, float thres_red, float thres_green)
{   
    if (sdf_distance > thres_green && sdf_distance1 > thres_green)
    {
      color.a = 0.0;
    }

    else if ((sdf_distance < thres_green && sdf_distance > thres_red) || (sdf_distance1 < thres_green && sdf_distance1 > thres_red))
    {
      color.a = 0.0;

    }

    else
    {   
      color.r = 0.5 * 240.0/255;
      color.g = 0.5 * 214.0/255;
      color.b = 0.5 * 144.0/255;
    }
    
    return color;

}

vec4 color_overlay(vec4 color, float sdf_distance, float sdf_distance1, float thres_red, float thres_green, bool verbose)
{   
    if (verbose){
      vec4 sum;
      if (sdf_distance > thres_green && sdf_distance1 > thres_green)
      {
        sum.r = 0.0;
        sum.g = c_value;
        sum.b = 0.0;
      }

      else if ((sdf_distance < thres_green && sdf_distance > thres_red) || (sdf_distance1 < thres_green && sdf_distance1 > thres_red))
      {
        sum.r = c_value;
        sum.g = c_value;
        sum.b = 0.0;
      }
      else if ((sdf_distance < thres_red && sdf_distance > 0.0) || (sdf_distance1 < thres_red && sdf_distance1 > 0.0))
      {
        sum.r = c_value;
        sum.g = 0.0;
        sum.b = 0.0;
      }

      sum.a = 1.0;

      return sum;

    }
    else{
      return remove_segment(color,sdf_distance,sdf_distance1, thres_red, thres_green);
    }

}



vec3 color_overlay_inner(vec4 color, float sdf_distance, float thres_red, float thres_green)
{ 
  vec3 sum;
  if ((sdf_distance < thres_red && sdf_distance > 0.0))
  {
    sum.r = c_value;
    sum.g = 0.0;
    sum.b = 0.0;
  }
  else if ((sdf_distance < thres_green && sdf_distance > thres_red))
  {
    sum.r = c_value;
    sum.g = c_value;
    sum.b = 0.0;
  }
  else if ((sdf_distance > thres_green))
  {
    sum.r = 0.0;
    sum.g = c_value;
    sum.b = 0.0;
  }
  return sum;

}

//----------------------------------------------------------------------
//  Computes phong shading based on current light and material
//  properties.
//---------------------------------------------------------------------- 

vec3 shade(vec3 p, vec3 v, vec3 n)
{
    vec4 lp = gl_ModelViewMatrixInverse * gl_LightSource[0].position;
    vec3 l = normalize(lp.xyz - p * lp.w);
    vec3 h = normalize(l+v);
    float cos_i = max(dot(n, l), 0.0);
    float cos_h = max(dot(n, h), 0.0);

    vec3 Ia = gl_FrontLightProduct[0].ambient.rgb;
    vec3 Id = gl_FrontLightProduct[0].diffuse.rgb * cos_i;
    vec3 Is = gl_FrontLightProduct[0].specular.rgb * pow(cos_h, gl_FrontMaterial.shininess);

    return (Ia + Id + Is);
}


//----------------------------------------------------------------------
//  Main fragment shader code.
//----------------------------------------------------------------------

void main(void)
{
    vec4 camera = gl_ModelViewMatrixInverse * vec4(0.0, 0.0, 0.0, 1.0);
    vec3 raydir = normalize(vPosition.xyz - camera.xyz);

    float t_entry = entry(vPosition.xyz, raydir);
    t_entry = max(t_entry, -distance(camera.xyz, vPosition.xyz));

    // estimate a reasonable step size
    float t_step = distance(uMinCorner, uMaxCorner) / uResolution;
    vec3 tc_step = uTextureScale * (t_step * raydir);

    // cast the ray (in model space)
    vec4 sum = vec4(0.0);
    vec3 tc = gl_TexCoord[0].stp + t_entry * tc_step / t_step;

    vec4 dpos = vPosition;


    for (float t = t_entry; t < 0.0; t += t_step, tc += tc_step)
    {
        // sample the volume for intensity (red channel)
        float intensity = isoValue(tc);
        vec3 nabla;
        if (intensity > uIsosurface)
        {
            vec3 tcr = refine(tc - tc_step, tc, uIsosurface, 1.0);

            if (uSmoothVolume){
              // //Smoothing
              nabla = vec3(0., 0., 0.);
              vec3 tr;
              int cnt = uSmoothingLevel;
              vec3 half_i = vec3(1., 1., 1.) * float(cnt)/2.0;
              // vec3 tcr = tc;
              for (int x = 0 ; x < cnt ; x++){
                for (int y = 0 ; y < cnt ; y++){
                  for (int z = 0 ; z < cnt ; z++){
                    tr[0] = tcr[0] + (float(x) - half_i[0]) * uGradientDelta[0];
                    tr[1] = tcr[1] + (float(y) - half_i[1]) * uGradientDelta[1];
                    tr[2] = tcr[2] + (float(z) - half_i[2]) * uGradientDelta[2];
                    nabla += gradient(tr);
                  }
                }
              }
            }
            else{
              nabla = gradient(tcr);
            }

            float dt = length(tcr - tc) / length(tc_step);
            vec3 position = vPosition.xyz + (t - dt * t_step) * raydir;
            vec3 normal = -normalize(nabla);
            vec3 view = -raydir;


            vec3 sdf_t = tcr;
            // float sdf_distance = texture3D(sdfVolume, tcr).r - texture3D(sdfVolume, tcr).b;
            float sdf_distance = (texture3D(sdfVolume, sdf_t).r - texture3D(sdfVolume, sdf_t).b) * 600.0 * uUnit[1];
            float sdf_distance1 = (texture3D(sdfVolume1, sdf_t).r - texture3D(sdfVolume1, sdf_t).b) * 600.0 * uUnit[1];

            // VF
            // float sdf_distance = (194.0 * texture3D(sdfVolume, sdf_t).r - 19.0 * texture3D(sdfVolume, sdf_t).b) * uUnit[1];
            // bone
            // float sdf_distance1 = (293.0 * texture3D(sdfVolume1, sdf_t).r - 31.0 * texture3D(sdfVolume1, sdf_t).b) * uUnit[1];


            ///////////////////////////
            // Color Map
            //////////////////////////
            // Segmentation1: (128, 174, 128)
            // Segmentation2: (241, 214, 145)
            // Segmentation3: (177, 122, 101)
            // Segmentation4: (111, 184, 210)
            // Segmentation5: (216, 101,  79)
            // Lam seg3 full: (241, 214, 145)
            // Lam seg3 full: (241, 214, 145)
            // Lam seg3 full: (241, 214, 145)
            // section 1 & 3: (183, 156, 220)
            // section 2    : (221, 130, 101)
            // section 4 & 6: (144, 238, 144)
            // section 5    : ( 14,  37, 245)

            // vec3 L1_13 = vec3(0.4235, 0.196,  0.155);
            // vec3 L1_2  = vec3(0.4335, 0.255,  0.196);
            // vec3 L1_46 = vec3(0.2825, 0.4645, 0.2825);
            // vec3 L1_5  = vec3(0.3745, 0.202, 0.1705);
            
            vec3 L1_13 = uL_13;
            vec3 L1_2  = uL_2;
            vec3 L1_46 = uL_46;
            vec3 L1_5  = uL_5;

            

            // Indicates the simulation mm distance thresholds for red, yellow, and green (the scalar is in mm)
            // float thres_red = 2.0 * uUnit[1];   // < thres_red is colored red
            // float thres_green = 4.0 * uUnit[1]; // > thres_green is colored green
            // float thres_red = 2.0 / uUnit[0];   // < thres_red is colored red
            // float thres_green = 4.0 / uUnit[0]; // > thres_green is colored green


            float thres_red = uThres[0];
            float thres_green = uThres[1];

            float dis = 0.04;

            vec4 color_sdf;
            bool flag_keep = true;
            // For section 1 & 3
            if (texture3D(uVolume, tcr).r > L1_13[0] - dis && texture3D(uVolume, tcr).r < L1_13[0] + dis && texture3D(uVolume, tcr).g > L1_13[1] - dis && texture3D(uVolume, tcr).g < L1_13[1] + dis && texture3D(uVolume, tcr).b > L1_13[2] - dis && texture3D(uVolume, tcr).b < L1_13[2] + dis){
              color_sdf = color_overlay(texture3D(uVolume, tcr), sdf_distance, sdf_distance1, thres_red, thres_green, flag_keep);
            }

            // For section 2 
            else if (texture3D(uVolume, tcr).r > L1_2[0] - dis && texture3D(uVolume, tcr).r < L1_2[0] + dis && texture3D(uVolume, tcr).g > L1_2[1] - dis && texture3D(uVolume, tcr).g < L1_2[1] + dis && texture3D(uVolume, tcr).b > L1_2[2] - dis && texture3D(uVolume, tcr).b < L1_2[2] + dis){
              color_sdf = vec4(0.0, 0.296, 0.5, 0.0);
            }

            // For section 4 & 6
            else if (texture3D(uVolume, tcr).r > L1_46[0] - dis && texture3D(uVolume, tcr).r < L1_46[0] + dis && texture3D(uVolume, tcr).g > L1_46[1] - dis && texture3D(uVolume, tcr).g < L1_46[1] + dis && texture3D(uVolume, tcr).b > L1_46[2] - dis && texture3D(uVolume, tcr).b < L1_46[2] + dis){
              color_sdf = color_overlay(texture3D(uVolume, tcr), sdf_distance, sdf_distance1, thres_red, thres_green, flag_keep);
            }
            
            // For section 5 
            else if (texture3D(uVolume, tcr).r > L1_5[0] - dis && texture3D(uVolume, tcr).r < L1_5[0] + dis && texture3D(uVolume, tcr).g > L1_5[1] - dis && texture3D(uVolume, tcr).g < L1_5[1] + dis && texture3D(uVolume, tcr).b > L1_5[2] - dis && texture3D(uVolume, tcr).b < L1_5[2] + dis){
              color_sdf = vec4(0.0, 0.296, 0.5, 0.0);
            }

            else{
              color_sdf.rgb = texture3D(uVolume, tcr).rgb;
              color_sdf.a = 1.0;
            }

            vec3 colour = shade(position, view, normal) * color_sdf.rgb / uIsosurface;
            sum = vec4(colour, color_sdf.a);

            // calculate fragment depth
            vec4 clip = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
            gl_FragDepth = (gl_DepthRange.diff * clip.z / clip.w + gl_DepthRange.near + gl_DepthRange.far) * 0.5;
  
            

            break;
        }
    }

    // discard the fragment if no geometry was intersected
    if (sum.a <= 0.0) discard;
    if (uEnableShadow == 1){
      dpos = gl_ModelViewMatrix * dpos;
      float s = dot(gl_EyePlaneS[1], dpos);
      float t = dot(gl_EyePlaneT[1], dpos);
      float r = dot(gl_EyePlaneR[1], dpos);
      float q = dot(gl_EyePlaneQ[1], dpos);
      vec4 depos = vec4(s, t, r, q);
      vec4 shadow = shadow2DProj(shadowMap, depos);
      gl_FragColor = vec4(sum.rgb, shadow.a);
    }
    else{
      gl_FragColor = sum;
    }
}
