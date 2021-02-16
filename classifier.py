from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

import pdf

class DocumentClassifier:
    @classmethod
    def from_file(cls, path):
        return joblib.load(path)

    def __init__(self):
        self._clf = None

    def parse_categories(self, path):
        categories = set()
        for p in path.glob('*.pdf'):
            categories.add(p.stem.split('_', 1)[0])
        self._categories = list(categories)

    def get_category(self, s : str):
        for idx, cat in enumerate(self._categories):
            if s.find(cat) == 0:
                return idx

    def read_dataset(self, path) -> dict:
        path_obj = Path(path)
        pdfs = path_obj.glob('*.pdf')
        X = []
        Y = []
        names = []
        for pdf_path in pdfs:
            file_name = pdf_path.stem
            text = pdf.read_any(pdf_path)
            if text:
                Y.append(self.get_category(file_name))
                X.append(text)
                names.append(file_name)
        return X, Y, names

    def train(self, path):
        path_obj = Path(path)
        self.parse_categories(path_obj)
        X, Y, names = self.read_dataset(path_obj)

        self._clf = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=1000, random_state=42))
                        ])
        self._clf.fit(X, Y)

    def predict(self, path):
        X = []
        if path.is_dir():
            for p in path.glob('*.pdf'):
                text = pdf.read_any(p)
                if text:
                    X.append(text)
        else:
            X.append(pdf.read_any(path))

        res = self._clf.predict(X)
        [print(self._categories[item]) for item in res]

    def save(self, path):
        if not self._clf:
            print('Model is not trained')
        joblib.dump(self, path)