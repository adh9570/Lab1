import sys

OPEN_LAND_COLOR = '#F89412'
ROUGH_MEADOW_COLOR = '#FFC000'
EASY_MOVE_FOREST_COLOR = '#FFFFFF'
SLOW_RUN_FOREST_COLOR = '#02D03C'
WALK_FOREST_COLOR = '#028828'
IMPASS_VEG_COLOR = '#054918'
WATER_COLOR = '#0000FF'
ROAD_COLOR = '#473303'
FOOTPATH_COLOR = '#000000'
OOB_COLOR = '#CD0065'

if __name__ == "__main__":
    try:
        terrain_image = sys.argv[1]
        elevation_file = sys.argv[2]
        path_file = sys.argv[3]
        season = sys.argv[4]
        output_image_filename = sys.argv[5] 
    except:
        print("wiggle woogle")
