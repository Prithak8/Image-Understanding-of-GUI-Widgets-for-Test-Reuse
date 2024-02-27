# Getting Started
This artifact evaluates different configurations of semantic matching in the test reuse context.
Configurations include those which are used by two stat-of-art  approaches (ATM, Craftdroid) as well as new configurations introduced by this study.
There are 253 configurations in total.
Each configuration is evaluated by two metrics: MRR and Top1.
 
### Requirements
- python 3.7
- pip3
- python3.7-dev
- 8 GB RAM
 
> Note: You need 20 GB RAM to use FAST embedding approach with the standard train set
 
> Note: Required os packages can be install by following command:
```
sudo apt-get install python3.7 pip3 python3.7-dev
```
 
### Python Packages
First you need to setup a new virtual environment
1. Update pip
   ```
   pip3 install --upgrade pip
   ```
1. Install the virtualenv package
   ```
   pip3 install virtualenv
   ```
1. Create a virtual environment
   ```
   virtualenv --python=python3.7 venv
   ```
1. Activate the environment (If it is not activated automatically)
   ```
   source venv/bin/activate
   ```
1. Now you can install required packages
    ```
    pip install -r requirements.txt
    ```
1. Run text_pre_process.py to download few packages:
    ```
    python -m text_pre_process
    ```
    You should see:
    
    ```
    download is completed!
    ```
 
  > Note: You can use any other virtual environment of your choice
 
> Note: You can skip the below section if you don't want to run the configurations that include BERT technique. 
 
For using BERT technique you need to setup a bert service first.
1. Create an additional python environment and activate it.
1. Use `requirements_bert.txt` to install required packages.
1. Run a bert server as follow:
    ```
    bert-serving-start -model_dir [path to the model in here] -num_worker=1
    ```
When the service is ready you see the following output:
 
```
I:WORKER-0:[__i:gen:559]:ready and listening!
I:VENTILATOR:[__i:_ru:164]:all set, ready to serve request!
```
 
> Note: We used the [bert_as_service](https://github.com/hanxiao/bert-as-service) implementation of bert embedding technique
 
 
 
## Terminology
We define the terms that we use in the rest of the document as follow:
- **Semantic Matching Components**: Semantic matching has four components a) algorithm b) descriptors c) word embedding d) train set. Components work together to match a source event to a target event among multiple target candidates.
 
- **Component Instance**: A concrete implementation of a component is an instance of that component. For example `SemFinder` is an instance of the algorithm component.
 
- **Matching Configuration**: A combination of component instances is a semantic matching configuration.
For example: (SemFinder, Union, w2v, googleplay) is a configuration.
 
- **Descriptor**: Set of attributes that describe the widget that an event executes on it
 
> Note: The code refers to `SemFinder` with the alias `custom`.
 
 
 
## Run
 
1. Activate virtual environment(s)
 
1. Set the directory of the word embedding models inside `config.yml` under `model_dir` key. This directory should have a structure similar to the `model_path` section in the `config.yml` file.
 
1. In the `config.yml` file un-comment instances you like to be considered for the semantic matching configuration. Components are active_techniques, train_set, algorithm and descriptors. active_techniques refers to embedding techniques.
 
1. Execute the below command to start the evaluation. The framework starts evaluating all the possible configurations, given the desired instances (instances that are not commented).
 
   ```
   python run_all_combinations.py
   ```
1. Results are saved in the `results_rank.csv` file.
 
> Note: if you stop the framework while it is evaluating configurations, in the next run it will resume from the last evaluated configuration.
 
> Note:  The amount of time required for evaluating a configuration depends on the embedding approach and. It may vary from 5 min (w2v) to 1 hours (USE).
 
 
 
When evaluation of configurations are successful you should see following output
 
```
atm_0-union-android-wm Top1: 147 MRR: 0.6758521597097267
atm_0-intersection-android-wm Top1: 179 MRR: 0.7267089012475919
craftdroid-union-blogs-wm Top1: 168 MRR: 0.6797442714574846
```
 
For configurations that already have been evaluated and results have been saved you should see following output:
 
```
craftdroid-union-android-wm already exist
craftdroid-intersection-android-wm already exist
custom-union-android-wm already exist
custom-intersection-android-wm already exist
```
 
>Note: You can run the framework only for one (or more) configuration.
To do so you should comment all the instances of the four components in the config file except the one you like to evaluate.
Remove the intermediary and the final result related to the configuration. Then run the framework.
 
 
 
 
# Detailed Description
 
### Reproducing the experiment
If you like to calculate everything from scratch you have to take following steps:
1. Remove intermediary and final results first.
   That include following files:
   - Any csv file inside the `sim_score` directory
   - `total_map.csv` inside the `events` directory
   - `results_rank.csv` in the root directory
1. Uncomment all the instance of the four components from `config.yml`
 
1. Activate the environments
 
1. Run the framework
 
> Note: It take approximately 24hrs to evaluate all of 253 configurations
 
In the result file you have the following columns:
 
- **algorithm,descriptors,training_set,word_embedding:** They indicate the configuration.
- **topN:** Indicates for how many of source events, the correct target candidate is among the top N candidates, based on their similarity scores.
- **MRR:** MRR score of the configuration.
- **time:** Execution time for evaluating the configuration.
- **zeros:** Number of times the embedding approach returns a similarity score of zero. This value can only be calculated when the intermediary result of the configuration does not exist from previous run. Otherwise it will be -1.
 
### Links to pre-trained models
You should provide models for embedding techniques that you are going to use.
Here we share links of the models.
You can use them for reference or download them directly if you don't have access to them from the replication package.
You can download pre-trained models [The code refers to them as standard] from provided links below.
- w2v: [GoogleNews]( https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz )
- USE: [universal-sentence-encoder]( https://tfhub.dev/google/universal-sentence-encoder/4 )
- NNLM: [nnlm-en-dim128
]( https://tfhub.dev/google/nnlm-en-dim128/2 )
- BERT: [uncased_L-12_H-768_A-12](https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip)
- GloVe: [glove.6B](http://nlp.stanford.edu/data/glove.6B.zip)
- FAST: [cc.en.300](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz)
 
You can download pre-trained word embedding models that we trained for this study from the below. The zip file
includes W2V, Fast, GloVe models for Google Play, Manuals and Blog corpora. Additionally it includes the GloVe
model of the standard corpus. Since the standard model of GloVe requires a preprocessing step to make it
readable by the NLP python package (Gensim) we used, We uploaded the preprocessed model to facilitate
usage of our codes.
 
- Constructed models for the study: [embedding-models](https://drive.google.com/file/d/1e-6LSBAJC_VdgMM_16Adf9JvKXr_saQb/view)
 
# Packages Introduction
Our framework consists of 5 python packages that we introduce below.
 
## <a name="events"></a> events
Events package contains inputs of the framework.
We used the [Appium](https://appium.io/) to run test cases of ATM and Craftdroid and extract descriptors of events.
We saved descriptors into csv files to create inputs of the framework.
In this package, there are two sub directories and a file named `index_map`.
Subdirectories are: a) src_events b) target_events.
Each file of subdirectories is corresponding to one test case.
`index_map` includes mapping of events between test cases.
### Events File Naming Convention
We have introduced following convention:
- `src_event` files have the name of the source application
- `target_event` files consist of combining source and target application names.  Names of source and target are combined by a dash.
- If there are more than one test case for an application we add a post fix to the name of applications. The postfix that we used is `bX` where X is the number of test cases.
 
> **Example**: Let's assume we have the migration of `AppA` to `AppB`. Then we have a file in src_events named `AppA` and a file in target_events named `AppA-AppB`. For the second migration of `AppA` to `AppB` we have a file in src_events named `AppAb2` and a file in target_events named `AppAb2-AppBb2`.
 
 
### Events Files Content
Each file contains event_index, label, type and attributes columns.
Each row represents a possible event in the GUI.
 
- `event_index`: Rows that have the same event_index belong to the same GUI state.
- `label`: Indicates if that event has been executed by the test case. If the event is executed the value is `correct` otherwise `wrong`.
- `type`: Indicates type of the event.
- `attributes`: attribute columns have textual information about the event.
 
 
> Note: When the framework starts working it will merge all the event files together.
It merges them based on the `index_map.csv` and it will save the results in a file named `total_map.csv`.
 
>Note: Our framework considers `total_map.csv` as an intermediary results. Therefore, each time you change any files in the events package you should remove the `total_map.csv` file.
 
> Note: Descriptors in the `total_map.csv` are preprocessed by NLP text preprocess approaches.
 
## evaluators
Evaluators are the core part of the framework.
They interact with other packages to evaluate a given semantic configuration.
Each matching algorithm has its own evaluator.
Evaluators are responsible for following tasks:
- Fetching the input data from the event package
- Apply the semantic matching configuration on the input data
- Save semantic similarity scores of candidate events
- Calculate performance of a given semantic matching configuration
 
## descriptors_processes
This package prepares the input data to be used by evaluators.
The package is responsible for the following tasks:
 
- Merge the event files and create `total_map.csv`
- Preprocess the descriptors
- Remove redundant events
- Select subset for descriptors based on the configuration
 
 
 
## embedding
This package loads word embedding models.
It also includes the necessary adaptor for using word level embedding approaches at the sentence level.
 
## sim_scores
In the package there is a file for each configuration.
Each file contains semantic similarity of source events to the target candidates.
The framework creates the files when it evaluates a semantic configuration.
> Note that the framework considers the files as intermediary results.
Therefore, when you change any file inside  previous packages the affected intermediary result files should be removed.
For example, when you change the ATM evaluator you should remove any file that uses the ATM algorithm in its configuration.
It is not necessary to remove unaffected files.
 
 
# <a name="new_subjects"></a>How to add new subjects
You should take the following steps for adding new subjects to the input files:
 
1. Run your test cases by Appium framework (or any other preferred framework)
 
1. Extract the descriptor of each possible events in each window that the test case goes through
 
1. Add index and label for each event.
For example all the events in the first window get the index of `0` and the executed event gets the `correct` label.
Rest of the events in the first window get the `wrong` label.
 
1. Save the descriptor and other information in the same format as described in the [events](#events) section.
   - Each file in the `src_events` or `target_events` should have following non empty values for following columns:
       - event_index, label, type
   - Each file in the `src_events` or `target_events` should have following columns but they can be empty
       - text, id, content_desc, hint, parent_text, sibling_text, activity,atm_neighbor, file_name
 
1. Update `index_map.csv` file as follow:
   - src_app: Name of the source test file that exist in the `src_events` directory
   - target_app: It should be filled by the second part of the filename after dash in the `target_events` directory.
   For example `Expense2-Expense4` will be `Expense4`.
   - src_index: Index of the event in the source test
   - target_index: Index of the semantically equivalent even in the target test case
1. Remove all the intermediary results from past executions of the framework
 
 
# How to add new semantic matching configurations
You can extend our framework to consider new configurations.
This is equal to modifying or adding new instances to components.
Each of the components are implemented independently.
Therefore, you can add/modify an instance of a component and leave the other components as they are.
 
Below we discuss how you can add new instance(s) to each component.
 
## Descriptors
1. If you add a new descriptor that include a new attribute you need to follow instructions for [adding new subjects](#new_subjects).
Otherwise you skip this step and go to step 2.
 
1. Add your new descriptor to following classes:
   - from `load_data.py`: `ApproachDescriptors`
   - from `load_data.py`:  `DescriptorTypes`
 
1. Make sure evaluators are using your descriptors properly.
You can do that by reviewing `make_descriptors_compatible` functions of each evaluator.
 
1. Add the new descriptor to the `config.yml` file.
 
## Algorithm
1. Create a new class that extends `AbstractEvaluator` class
 
1. Implement the abstract methods
 
1. Add the new  algorithm to the `config.yml` file.
 
1. Add the new algorithm to the `find_evaluator` function from `EvaluatorBuilder`
 
## Embedding
1. If you are adding an approach that is sentence level extend `WordEmbedding` class form `word_embedding.py`. Otherwise extend `Word2VecS` class from the same file.
 
1. Implement abstract methods.
 
1. Add your model to the `embeddings` dictionary and `EmbedTypes` Enum from `word_embedding.py` file.
 
1. If your technique does not require a model to load; add the technique to the `no_model_techniques` list in the `get_model_path` function.
 
1. Add the new embedding technique to the `config.yml` file.
 
1. Update the `forbid_config` function from `run_all_combinations.py`. This function checks if a given train set is applicable to a given embedding approach. For instance, the `w2v` approach cannot have the `empty` train set.
 
1. Add the model/s of your new approach to the `model_path` element in the `config.yml` file.
Key of the new entry should have two parts separated by an underscore.
First part is the embedding approach name as stated in the `EmbedTypes` of the `word_embedding.py`.
The second part is the train set name.
 
## Train Set
First you need to train a model for your desired embedding approach based on the train set.
Then you add the model to the framework as follow:
 
1. Add the model/s of your new train set to the `model_path` element in the `config.yml` file.
Key of the new entry should have two parts separated by an underscore.
First part is the embedding approach name as stated in the `EmbedTypes` of the `word_embedding.py`.
The second part is the train set name.
 
1. Put the model in the path you stated in the previous step.
 
1. Update the `forbid_config` function from `run_all_combinations.py`. This function checks if a given train set is applicable to a given embedding approach. For instance, the `w2v` approach cannot have the `empty` train set.


