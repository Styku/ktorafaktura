#!/usr/bin/env python

from config import Config
from classifier import DocumentClassifier
from pathlib import Path
import pdf
import argparse

def parse_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")

    parser.add_argument("-t", "--train", help="train document classifier",
                        action="store_true")
    parser.add_argument("-s", "--scan", help="scan and classify document",
                        action="store_true")
    parser.add_argument("--disable-ocr", help="disable automatic OCR",
                        action="store_true")
    
    args = parser.parse_args()
    args.path = Path(args.path)
    return args

def train(path):
    model = DocumentClassifier()
    model.train(path)
    model.save('model.pkl')

def predict_scan(path):
    scan_path = Path(path)
    pdf.scan(scan_path)
    model = DocumentClassifier.from_file('model.pkl')
    model.predict(scan_path)

def predict(path):
    model = DocumentClassifier.from_file('model.pkl')
    model.predict(path)

if __name__ == "__main__":
    Config.load()
    args = parse_cmdline_args()
    if args.train:
        train(args.path)
    elif args.scan:
        predict_scan(args.path)
    else:
        predict(args.path)



