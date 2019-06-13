# mks66-final

## Names
Aleks Koroza, Matthew Kendall

## Team Name
Team Malleks

## Core Features
- Texture Maps
  - Mapping an image file to a rectangular prism
    - Possibly combine (R,G,B) value of texture map with lighting

## Important Information
- All textures currently need to be named TEXUTRE
- All textures need to have nice pixel dimensions: (multiple of 50 x multiple of 50)

### Required Packages
numpy: for inverse matrices

### Script Format
In the script, there must be the following line if there is a texture:
texture TEXTURE 0 0 0 0 0 0 0 0 0 0 0 0

If you want to apply TEXTURE to a box, add it as the second argument in the script, for example:
box TEXTURE 0 0 0 200 200 200

## Language
python3

## Stretch Goals
Texture maps to mesh

## TO-DO
- Implementation of multiple textures
- Lighting on texture
- Missing 3000 pixels from parser?
- Description of algorithm?
