# Files Guide

- **semantic_matching.zip:** The semantic matching framework. This is the main artefact.
- **models.zip:** embedding models that the framework uses.
- **sm-image.ova:** Image of a virtual machine. The VM contains a ready to use environment of the frame work.
- **train-datasets:** Train set that we used to create embedding models

## VM

The framework and all the models are provided in the VM. All the necessary packages are installed in the VM. To use the VM take the following steps

1. login 
    ``` 
    user: ubuntu
    pass: issta2021semanticmatching
    ```
1. Go to the framework directory
    ```
    cd ~/Desktop/semantic_matching
    ```
1. Activate `venv_bert` if you like to use BERT. Run the BERT service:
    ```
     bert-serving-start -model_dir ../models/bert/uncased_L-12_H-768_A-12/ -num_worker=1

    ```
1. Activate the `venv` environment.

1. Remove the intermediary result as you want. If you have a limited time for test we suggest to remove few lines from the `results_rank.csv`. 




