"""
DGL-KE交叉验证与预测
@author: zhang shilong
@date: 2022/05/05
"""
import numpy as np
import spacy
import scispacy
import os


class DGLKEModel:

    def __init__(self):
        self.triple_dict = dict()
        self.qc_passed_triples = 0
        self.nlp = None

    def read_triples(self, triple_path, quality_control=True):
        if quality_control:
            self.nlp = spacy.load("en_core_sci_sm")

        too_short_triples = 0
        non_verb_triples = 0

        with open(triple_path, "r") as file:
            for line in file.readlines():
                line = line.strip()
                if not line:
                    continue
                h, r, t = line.split("\t")
                if quality_control:
                    if len(r) < 4:
                        too_short_triples += 1
                        continue
                    r = r.replace('"', " ").strip()
                    r_nlp = self.nlp(r)
                    if len([token.lemma_ for token in r_nlp if token.pos_ == "VERB"]) == 0:
                        non_verb_triples += 1
                        continue
                self.triple_dict[self.qc_passed_triples] = {"h": h, "r": r, "t": t}
                self.qc_passed_triples += 1

        if quality_control:
            print("# of too short triples: {}".format(too_short_triples))
            print("# of non-verb triples: {}".format(non_verb_triples))
            print("# of qc-passed triples: {}".format(self.qc_passed_triples))
        print("# of total triples: {}".format(too_short_triples + non_verb_triples + self.qc_passed_triples))

    def k_fold_cross_validation(self, k=5, test_set=0.2):
        command = """
            DGLBACKEND=pytorch dglke_train \
            --model_name TransE_l2 \
            --dataset covid-19 \
            --data_path data/ \
            --data_files train.txt valid.txt test.txt \
            --format raw_udd_hrt \
            --batch_size 100 \
            --neg_sample_size 30 \
            --hidden_dim 300 \
            --gamma 19.9 \
            --lr 0.2 \
            --max_step 500 \
            --log_interval 100 \
            --batch_size_eval 16 \
            -adv \
            --regularization_coef 1.00E-09 \
            --test \
            --num_thread 1 \
            --num_proc 12 \
            --save_path model/
            """

        metrics = []

        perm = list(np.random.permutation(self.qc_passed_triples))
        test_split_num = int(self.qc_passed_triples * (1 - test_set))
        split_num = int(test_split_num / k)

        self.write_dataset("test.txt", perm, test_split_num, self.qc_passed_triples)
        for i in range(k):
            self.write_dataset("train.txt", perm, 0, i * split_num, (i + 1) * split_num, test_split_num)
            self.write_dataset("valid.txt", perm, i * split_num, (i + 1) * split_num)

            return_text = os.popen(command).read()
            test_result = os.popen("echo '{}' | grep 'Test average'".format(return_text)).read()
            for metric in [line.strip().split(" : ")[1] for line in test_result.split("\n", 4)]:
                metrics.append(float(metric))

        print("-----------{}-fold Cross Validation-----------".format(k))
        for i, metric in zip(range(5), ["MR", "MRR", "Hits@1", "Hits@3", "Hits@10"]):
            print("Test average {} : {}".format(metric, np.mean(metrics[i::5])))
        print("---------------------------------------------")

    def write_dataset(self, file_name, perm, start_pos1, end_pos1, start_pos2=0, end_pos2=0):
        output_prefix = "data/"
        with open(output_prefix + file_name, "w") as f:
            for i in perm[start_pos1:end_pos1] + perm[start_pos2:end_pos2]:
                tri = self.triple_dict[i]
                f.write("{}\t{}\t{}\n".format(tri["h"], tri["r"], tri["t"]))

    @staticmethod
    def predict(model_path, format_, head_list="", relation_list="", tail_list=""):
        command = """
        DGLBACKEND=pytorch dglke_predict \
        --model_path {} \
        --format '{}' \
        --data_files {} {} {} \
        --topK 20 \
        --raw_data \
            --entity_mfile data/entities.tsv \
            --rel_mfile data/relations.tsv
        """
        os.system(command.format(model_path, format_, head_list, relation_list, tail_list))


if __name__ == "__main__":
    input_path = "data/qc_passed_triples.txt"

    model = DGLKEModel()
    model.read_triples(input_path, quality_control=False)
    model.k_fold_cross_validation()

    model.predict("model/TransE_l2_covid-19_0", "h_*_t", head_list="data/head.list", tail_list="data/tail.list")
