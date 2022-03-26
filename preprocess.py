#%%
import numpy as np


# %%
# # inspect the COSZEN feature 
# for i in range(1,29):
#     s_in = np.load(f"Dataset/02_{str(i).zfill(2)}/s_feature.np")
#     print(i, np.min(s_in[:, 4]))

# # inspect the I_CLDFRAC feature 
# for i in range(9,10):
#     v_in = np.load(f"Dataset/02_{str(i).zfill(2)}/v_feature.np")
#     for j in range(v_in.shape[0]):
#         if np.max(v_in[j,4,:]) > 0:
#             print(i, j)


# %%
import os,re

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if re.match(r'.*(feature|target).*', f):
                fullname = os.path.join(root, f)
                yield fullname, f

def doProcess():
    base = './Dataset/'
    for fullName, fileName in findAllFile(base):
        print("Handling " + fullName)
        rawContents = np.load(fullName)
        if fileName == "s_feature.np":
            rawContents = rawContents[:,4:]
        elif fileName == "s_target.np":
            rawContents = rawContents[:,[0,1,4,5,6,7,8,9,10,11,14,15]]
        with open(fullName, 'wb') as f:
            np.save(f, rawContents)
            
    

doProcess()
# %%
