import visual_genome.local as vg
 
 # Convert full .json files to image-specific .jsons, save these to 'data/by-id'.
 # These files will take up a total ~1.1G space on disk.
vg.save_scene_graphs_by_id(data_dir='data/visual_genome/', image_data_dir='data/visual_genome/by-id/')

# Load scene graphs in 'data/by-id', from index 0 to 200.
# We'll only keep scene graphs with at least 1 relationship.
# scene_graphs = vg.get_scene_graphs(start_index=0, end_index=-1, min_rels=1,
#                                    data_dir='data/visual_genome/', image_data_dir='data/visual_genome/by-id/')