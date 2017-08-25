
# coding: utf-8

# # Read data from files and prepare data structures
# 

# In[203]:

import ujson as json
import pandas as pd
from IPython.display import display

filename = "source_data.json"

doc_data = []
prac_data = []

# Open file and read data quickly
with open(filename, 'r') as f:
    for i,line in enumerate(f):
        object_ = json.loads(line)    
        doc_data.append(object_["doctor"].values())
        
        # Get all practices for each doctor (different rows in the table but common index that references the doctor)
        for prac in object_["practices"]:
            prac_data.append([i] + list(prac.values()))

# Get attributes name to insert in dataframe
doc_cols = list(object_["doctor"].keys())
prac_cols = ["index"]+ (list(object_["practices"][0].keys()))

# Create dataframes and convert to lower case
docs = pd.DataFrame(doc_data, columns=doc_cols )
pracs = pd.DataFrame(prac_data, columns=prac_cols).apply(lambda x: x.astype(str).str.lower())

# Necessary to convert index col to integer 
pracs['index'] = pd.to_numeric(pracs['index'])

# Read csv file
raw_data = pd.read_csv("match_file.csv")

# Add index col to simplify operations
docs['index'] = docs.index
raw_data['index'] = raw_data.index



# # # of total documents scanned

# In[204]:

print ("Total number of documents scanned in source_data.json file is: ", len(docs))
print ("Total number of documents scanned in match_file.csv file is: ", len(raw_data))


# # # of Doctors matched with NPI

# In[205]:

npi_match = raw_data.merge(docs, on=['npi'])

print("Number of doctors matched with NPI is: ",len(npi_match))
# display(npi_match)


# # # of Practice matched with address

# In[206]:

# Same address
values = ['street','street_2','city','state', 'zip']
same_add = raw_data.merge(pracs, on=values)
# display(same_add)
print("Number of practices matched with same address is: ",len(same_add))


# # # of Doctors matched with name and address

# In[207]:

# Same address tables
raw_ = raw_data.loc[same_add['index_x']]
docs_= docs.loc[same_add['index_y']]


# #Same address and name
same_add_name = raw_.merge(docs_, on=['first_name', 'last_name'])
# display(same_add_name)
print("Number of doctors matched with same name and address is: ",len(same_add_name))


# We must note that in all cases we got an address matching we also obtained a name matching.

# # # of documents that could not be matched

# In[208]:

# Append indexes of matched docs
matched_elements =  npi_match['index_x'].append(same_add['index_x']).unique()

matched = raw_data.index.isin(matched_elements)
unmatched = raw_data[~matched]

print("The number of documents in match_file.csv that could no be matched is: ", len(unmatched))

