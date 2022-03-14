# %%
import netCDF4 as nc
import numpy as np
import os

# %%
# read env variables
START_M = os.environ.get('START_M', "01")
START_D = os.environ.get('START_D', "01")
END_M = os.environ.get('END_M', "01")
END_D = os.environ.get('END_D', "02")
print(START_M, START_D, END_M, END_D)

# %%
ij_in_fields = [
    "I_O3",
    "I_QC",
    "I_QI",
    "I_QS",
    "I_COSZEN",
    "I_ALBEDO",
    "I_TSFC",
    "I_EMISS",
    "I_TOPO",
    "XLAT",
    "XLONG",
] 

ij_out_fields = [
    "O_SWUPT",
    "O_SWUPTC",
    "O_SWDNT",
    "O_SWDNTC",
    "O_SWUPB",
    "O_SWUPBC",
    "O_SWDNB",
    "O_SWDNBC",
    "O_LWUPT",
    "O_LWUPTC",
    "O_LWUPB",
    "O_LWUPBC",
    "O_LWDNT",
    "O_LWDNTC",
    "O_LWDNB",
    "O_LWDNBC",
]

ikj_in_fields = [
    "I_PLAY",
    "I_TLAY",
    "I_H2OVMR",
    "I_O3VMR",
    "I_CLDFRAC",
    "I_REI",
    "I_REL",
    "I_RES",
    "I_CLWPTH",
    "I_CIWPTH",
    "I_CSWPTH",
]

ikj_out_fields = [
    "O_RTHRATENSW",
    "O_RTHRATENLW",
]


# %%

# process one output file (all grid columns in one time step)
def process_wrfout(file_path):

    wrfout = nc.Dataset(file_path)

    vertical_layers = wrfout.dimensions["bottom_top"].size
    south_north = wrfout.dimensions["south_north"].size
    west_east = wrfout.dimensions["west_east"].size


    print(f"Processing output at {file_path}\n")

    scalar_features = [[] for _ in range(south_north*west_east)]
    vector_features = [[] for _ in range(south_north*west_east)]
    scalar_targets = [[] for _ in range(south_north*west_east)]
    vector_targets = [[] for _ in range(south_north*west_east)]

    # input fields
    for field in ij_in_fields:
        rawData = np.squeeze(wrfout[field][:])
        for i in range(south_north):
            for j in range(west_east):
                scalar_features[i*west_east+j].append(rawData[i,j])
    scalar_features = np.array(scalar_features)
    
    for field in ikj_in_fields:
        rawData = np.squeeze(wrfout[field][:])
        rawData = rawData.transpose(1,2,0)
        for i in range(south_north):
            for j in range(west_east):
                vector_features[i*west_east+j].append(rawData[i,j,:])
    vector_features = np.array(vector_features)
    
    # output fields
    for field in ij_out_fields:
        rawData = np.squeeze(wrfout[field][:])
        for i in range(south_north):
            for j in range(west_east):
                scalar_targets[i*west_east+j].append(rawData[i,j])
    
    for field in ikj_out_fields:
        rawData = np.squeeze(wrfout[field][:])
        rawData = rawData.transpose(1,2,0)
        for i in range(south_north):
            for j in range(west_east):
                vector_targets[i*west_east+j].append(rawData[i,j,:])
    
    wrfout.close()
    return scalar_features, vector_features, np.array(scalar_targets), np.array(vector_targets)

def save(s_feature, v_feature, s_target, v_target):
    output_path = f"Dataset/{START_M}_{START_D}"

    # Check whether the specified path exists or not
    isExist = os.path.exists(output_path)

    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(output_path)
        print("Output directory is created!")

    with open(f'{output_path}/s_feature.np', 'ab') as f:
        np.save(f, s_feature)
    with open(f'{output_path}/v_feature.np', 'ab') as f:
        np.save(f, v_feature)
    with open(f'{output_path}/s_target.np', 'ab') as f:
        np.save(f, s_target)
    with open(f'{output_path}/v_target.np', 'ab') as f:
        np.save(f, v_target)

# %%

input_folder = f"WRF_Output/{START_M}_{START_D}/"
for fileName in os.listdir(input_folder):
    s_feature, v_feature, s_target, v_target = process_wrfout(input_folder + fileName)
    save(s_feature, v_feature, s_target, v_target)


# to see the contents
# with open('test.np', 'wb') as f:
#     np.savetxt(f, s_feature)

