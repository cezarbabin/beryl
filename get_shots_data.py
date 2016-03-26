import parse 
import compare

MOTION_ARRAY = parse.motion_data('motion_files/fahim_11_Char00', "")

FILTERED_ARRAYS = compare.main(MOTION_ARRAY, compare.FT_JOINT_LIST)[1]

#compare.plot_data(FILTERED_ARRAYS)


