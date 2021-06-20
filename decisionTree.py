from IPython.display import Image, display
import pydotplus
from scipy import misc
from sklearn import tree
import graphviz

def renderTree(my_tree, features):
    # hacky solution of writing to files and reading again
    # necessary due to library bugs
    filename = "temp.dot"
    with open(filename, 'w') as f:
        f = tree.export_graphviz(my_tree,
                                 out_file=f,
                                 feature_names=features,
                                 class_names=["Perished", "Survived"],
                                 filled=True,
                                 rounded=True,
                                 special_characters=True)

    dot_data = ""
    with open(filename, 'r') as f:
        dot_data = f.read()

    graph = pydotplus.graph_from_dot_data(dot_data)
    image_name = "temp.png"
    graph.write_png(image_name)
    display(Image(filename=image_name))