from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from PIL import Image
import os
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Nudity:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__));
        model_file = os.path.abspath(base_path + "/files/retrained_graph.pb")
        input_name = "import/input"
        output_name = "import/final_result"
        self.input_height = 224
        self.input_width = 224
        self.input_mean = 128
        self.input_std = 128
        self.graph = self.load_graph(model_file)
        self.input_operation = self.graph.get_operation_by_name(input_name);
        self.output_operation = self.graph.get_operation_by_name(output_name);

    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()
        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)
        return graph

    def score(self, file_name):
        t = file_name
        with tf.Session(graph=self.graph) as sess:
          results = sess.run(self.output_operation.outputs[0],
                            {self.input_operation.outputs[0]: t})
        results = np.squeeze(results)
        return results[1].item();

    def has(self, file_name):
        return self.score(file_name) >= 0.8

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    args = parser.parse_args()

    if not args.image:
        print("--image is missing. please set image to be processed with --image='path'")
        return;
    nudity = Nudity()
    print(nudity.has(args.image))

if __name__ == "__main__":
    main();
