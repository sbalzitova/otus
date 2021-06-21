#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.analyzer import LogAnalyzer
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='default_config.json', help='Config file for your log analyzer')
args = parser.parse_args()


def main():
    analyzer = LogAnalyzer(args.config)
    analyzer.start()


if __name__ == '__main__':
    main()
