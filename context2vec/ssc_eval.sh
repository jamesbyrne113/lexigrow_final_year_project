#!/bin/bash

if [ $# < 4 ]; then
    echo "first argument must be the path to the model params, second argument must be the path to the test questions, third argument must be the path to the test answers, fourth argument must be the results file path"
    exit 1
fi

results_file=${4}
model_file=${1}
questions=${2}
answers=${3}
echo "${results_file} : ${model_file}"
python3 context2vec/context2vec/eval/sentence_completion.py ${questions} ${answers} ${results_file} ${model_file}
