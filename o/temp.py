'''import os
import json
import csv

# Specify the CSV and directory paths
ui_details_file = "C:/Users/dell/Downloads/ui_details.csv"
app_details_file = "C:/Users/dell/Downloads/app_details.csv"
filtered_traces_dir = "C:/Users/dell/Downloads/traces/filtered_traces"
semantic_annotations_dir = "C:/Users/dell/Downloads/rico_dataset_v0.1_semantic_annotations/semantic_annotations"

# Specify the app package name and interaction trace number
app_package_name = "com.finicity.mvelopes"
interaction_trace_number = "0"

# Function to extract the leaf nodes from a JSON hierarchy
def extract_leaf_nodes(json_data, leaf_nodes):
    if "children" in json_data:
        for child in json_data["children"]:
            extract_leaf_nodes(child, leaf_nodes)
    else:
        if any(key in json_data for key in ("resource-id", "class", "clickable", "content-desc", "componentLabel")):
            leaf_nodes.append(json_data)


def extract_leaf_nodes_sem(json_data, leaf_nodes):
    if "children" in json_data:
        for child in json_data["children"]:
            extract_leaf_nodes_sem(child, leaf_nodes)
    else:
        if any(key in json_data for key in ("iconClass", "textButtonClass", "componentLabel")):
            leaf_nodes.append(json_data)

# Open the UI details CSV file and read the relevant rows
with open(ui_details_file, "r") as ui_file:
    ui_reader = csv.DictReader(ui_file)
    relevant_rows = []
    for row in ui_reader:
        if row["App Package Name"] == app_package_name and row["Interaction Trace Number"] == interaction_trace_number:
            relevant_rows.append(row)

# Create a new CSV file and write the header row
output_file_name = f"{app_package_name}_interaction{interaction_trace_number}.csv"
with open(output_file_name, "w", newline="", encoding="utf-8") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["event_index","id","text","semantic_rep","file_name","class","type","content_desc","hint","parent_text","sibling_text","fillable_neighbor","neighbors","label","activity","atm_neighbor"])
    count = 0
    
    # Loop over the relevant rows from the UI details CSV file and read the JSON files
    for row in relevant_rows:
        ui_number = row["UI Number"]
        ui_number_in_trace = row["UI Number in Trace"]
        ui_trace_dir = filtered_traces_dir + "/" + app_package_name + "/trace_" + row["Interaction Trace Number"]
        view_hierarchies_dir = ui_trace_dir + "/view_hierarchies"
        gestures_file = ui_trace_dir + "/gestures.json"
        
        # Read the view hierarchy JSON file
        view_hierarchy_file = view_hierarchies_dir + "/" + f"{ui_number_in_trace}.json"
        with open(gestures_file, "r") as gestures:
            gesture = json.load(gestures)
            click = gesture.get(f"{ui_number_in_trace}")
            click[0][0] *= 1440
            click[0][1] *= 2560

        with open(view_hierarchy_file, "r") as json_file:
            view_hierarchy = json.load(json_file)
            
            # Extract the leaf nodes from the JSON hierarchy
            leaf_nodes1 = []
            act = view_hierarchy.get("activity","")
            extract_leaf_nodes(act.get("root",""), leaf_nodes1)
            
            # Read the semantic annotation JSON file
            semantic_annotation_file = semantic_annotations_dir + "/" + f"{ui_number}.json"
            
            with open(semantic_annotation_file, "r", encoding="utf-8") as json_file:
                semantic_annotation = json.load(json_file)
                
                # Extract the leaf nodes from the JSON hierarchy
                leaf_nodes2 = []
                extract_leaf_nodes_sem(semantic_annotation, leaf_nodes2)
                min_bound = [0, 0, 1440, 2560]
                for node1 in leaf_nodes1:
                    for node2 in leaf_nodes2:
                        semantic_rep = node2.get("iconClass") or node2.get("textButtonClass") or node2.get("componentLabel", "")
                        if semantic_rep != "":
                            if node1.get("bounds", "") == node2.get("bounds", ""):
                                bound = node1.get("bounds")
                                if(click[0][0] > bound[0] and click[0][1] > bound[1] and click[0][0] < bound[2] and click[0][1] < bound[3]) and (min_bound[0] <= bound[0] and min_bound[1] <= bound[1] and min_bound[2] >= bound[2] and min_bound[3] >= bound[3]):
                                    min_bound = bound
                
                # Loop over the leaf nodes and extract the required fields
                for node1 in leaf_nodes1:
                    for node2 in leaf_nodes2:
                        semantic_rep = node2.get("iconClass") or node2.get("textButtonClass") or node2.get("componentLabel", "")
                        if semantic_rep != "":
                            if node1.get("bounds", "") == node2.get("bounds", ""):
                                bound = node1.get("bounds")
                                if(min_bound == bound):
                                    label = "correct"
                                else:
                                    label = "wrong"
                                id = node1.get("resource-id", "")
                                text = node1.get("text", "")
                                class_ = node1.get("class", "")
                                type_ = node1.get("clickable", False) and "clickable" or "label"
                                content_desc = node2.get("content-desc", "")
                                activity = view_hierarchy.get("activity_name", "")
                                output_row = [count, id, text, semantic_rep, "", class_, type_, content_desc, "", "", "", "", "", label, activity, ""]
                                writer.writerow(output_row)

        # Write the output row to the CSV file
        count += 1
print(f"Output CSV file created: {output_file_name}")

'''
import pandas as pd

# Load CSV files into dataframes
df1 = pd.read_csv("results_rank_s.csv")
df2 = pd.read_csv("results_rank_t.csv")

z = 0
p = 0
n = 0

# Select MRR column in both dataframes
mrr1 = df1['MRR']
mrr2 = df2['MRR']
top11 = df1['top1']
top12 = df2['top1']
top21 = df1['top2']
top22 = df2['top2']
top31 = df1['top3']
top32 = df2['top3']
top41 = df1['top4']
top42 = df2['top4']
top51 = df1['top5']
top52 = df2['top5']
# Compute difference between the two MRR columns
mrr_diff = mrr1.sub(mrr2)
top1_diff = top11.sub(top12)
top2_diff = top21.sub(top22)
top3_diff = top31.sub(top32)
top4_diff = top41.sub(top42)
top5_diff = top51.sub(top52)

# Assign the difference to a new column in df1
df1['MRR2'] = mrr2
df1['top12'] = top12
df1['top22'] = top22
df1['top32'] = top32
df1['top42'] = top42
df1['top52'] = top52
df1['MRR_diff'] = mrr_diff
df1['top1_diff'] = top1_diff
df1['top2_diff'] = top2_diff
df1['top3_diff'] = top3_diff
df1['top4_diff'] = top4_diff
df1['top5_diff'] = top5_diff

print(df1['MRR_diff'].values.tolist())
# Print the resulting dataframe
for i in(df1['MRR_diff'].values.tolist()):
    if i == 0:
        z += 1
    elif i > 0:
        p += 1
    else:
        n += 1
print(p)
print(z)
print(n)
df1.to_csv('a.csv')
