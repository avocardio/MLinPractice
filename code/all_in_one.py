import argparse, pdb, csv, pickle


# feature_extraction
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer, TfidfVectorizer

# feature_selection
from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2

# dim_reduction
from sklearn.decomposition import PCA, TruncatedSVD, NMF

# classifier 
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion

# metrics
from sklearn.metrics import classification_report, cohen_kappa_score, accuracy_score, balanced_accuracy_score

import pandas as pd
import numpy as np

# balancing
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split

from collections import Counter

parser = argparse.ArgumentParser(description="all in one")
parser.add_argument("input_file", help="path to the input file")
parser.add_argument("-e", "--export_file",
                    help="export the trained classifier to the given location", default=None)

# evaluate:
parser.add_argument("-a", "--accuracy", action="store_true",
                    help="evaluate using accuracy")
parser.add_argument("-k", "--kappa", action="store_true",
                    help="evaluate using Cohen's kappa")
parser.add_argument("--balanced_accuracy", action="store_true",
                    help="evaluate using balanced_accuracy")
parser.add_argument("--classification_report", action="store_true",
                    help="evaluate using classification_report")

# balance dataset
parser.add_argument("--balance", type=str,
                    help="choose btw under and oversampling", default=None)
# feature_extraction
parser.add_argument("--feature_extraction", type=str,
                    help="choose a feature_extraction algo", default=None)
# dim_red
parser.add_argument("--dim_red", type=str,
                    help="choose a dim_red algo", default=None)
# classifier
parser.add_argument("--classifier", type=str,
                    help="choose a classifier", default=None)

args = parser.parse_args()
#args, unk = parser.parse_known_args()

# load data
# with open(args.input_file, 'rb') as f_in:
#    data = pickle.load(f_in)

# load data
df = pd.read_csv(args.input_file, quoting=csv.QUOTE_NONNUMERIC,
                 lineterminator="\n")

# split data
X = df['tweet'].array.reshape(-1, 1)
y = df["label"].ravel()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.05, random_state=100)

# balance data
if args.balance == 'over_sampler':
    over_sampler = RandomOverSampler(random_state=42)
    X_res, y_res = over_sampler.fit_resample(X_train, y_train)
elif args.balance == 'under_sampler':
    under_sampler = RandomUnderSampler(random_state=42)
    X_res, y_res = under_sampler.fit_resample(X_train, y_train)
else:
    X_res, y_res = X_train, y_train

print(f"Training target statistics: {Counter(y_res)}")
print(f"Testing target statistics: {Counter(y_test)}")


my_pipeline = []

# feature_extraction
if args.feature_extraction == 'HashingVectorizer':
    my_pipeline.append(('hashvec', HashingVectorizer(n_features=2**22,
                                                     strip_accents='ascii', stop_words='english', ngram_range=(1, 3))))
elif args.feature_extraction == 'TfidfVectorizer':
    my_pipeline.append(('tfidf', TfidfVectorizer(stop_words = 'english', ngram_range=(1, 3))))

# dimension reduction
if args.dim_red == 'SelectKBest(chi2)':
    my_pipeline.append(('dim_red', SelectKBest(chi2)))
elif args.dim_red == 'NMF':
    my_pipeline.append(('nmf', NMF()))


# classifier
if args.classifier == 'MultinomialNB':
    my_pipeline.append(('clf', MultinomialNB()))
elif args.classifier == 'SGDClassifier':
    my_pipeline.append(('clf', SGDClassifier(class_weight="balanced", n_jobs=-1,
                                             random_state=42, alpha=1e-06, verbose=1)))

classifier = Pipeline(my_pipeline)
"""
if args.small is not None:
    # if limit is given
    max_length = len(data['features'])
    limit = min(args.small, max_length)
    # go through data and limit it
    for key, value in data.items():
        data[key] = value[:limit]
"""

classifier.fit(X_res.ravel(), y_res)
# pdb.set_trace()

# now classify the given data
prediction = classifier.predict(X_test.ravel())


# pdb.set_trace()
# collect all evaluation metrics
evaluation_metrics = []
if args.accuracy:
    evaluation_metrics.append(("accuracy", accuracy_score))
if args.kappa:
    evaluation_metrics.append(("Cohen's kappa", cohen_kappa_score))
if args.balanced_accuracy:
    evaluation_metrics.append(("balanced accuracy", balanced_accuracy_score))
# compute and print them
for metric_name, metric in evaluation_metrics:

    print("    {0}: {1}".format(metric_name,
          metric(y_test, prediction)))

if args.classification_report:
    categories = ["Flop", "Viral"]
    print(classification_report(y_test.ravel(), prediction,
                                target_names=categories))


# export the trained classifier if the user wants us to do so
if args.export_file is not None:
    with open(args.export_file, 'wb') as f_out:
        pickle.dump(classifier, f_out)