import powergama
import powergama.powergim as pgim
res_file="sto_doggerbank_smaller.csv"

grid_data = powergama.GridData()
grid_data.readSipData(nodes = "data/dog_nodes.csv",
                  branches = "data/dog_branches.csv",
                  generators = "data/dog_generators.csv",
                  consumers = "data/dog_consumers.csv")

# Profiles:
samplesize = 100
grid_data.readProfileData(filename= "data/timeseries_sample_100_rnd2016.csv",
                          timerange=range(samplesize), timedelta=1.0)



sip = pgim.SipModel()
dict_data = sip.createModelData(grid_data,
                                datafile='data/dog_data_irpwind.xml',
                                maxNewBranchNum=5,maxNewBranchCap=5000)





grid_res = sip.extractResultingGridData(grid_data=grid_data,
                                    file_ph=res_file,stage=1)
