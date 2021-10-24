# Without_data_augmentation Folder
* **Filename**: 1 - load_original_delete_unnecessary_variables

  **Description**: This script delete variables written in names_to_delete.txt file (this variables names were discarded in the initial phase according to the context of the problem) and variables with the same value for each patient (as those does not apport anything).

  **Output**: The initial dataset with the desired variables.


*  **Filename**: 1.1 Rename-English-Dataset

    **Description**: This script translate and rename variables from spanish to english.

    **Output**: The initial dataset with the desired variables in english.


*  **Filename**: 2 - cleaned_data_overview

    **Description**: This script generate plots and table that help to describe the dataset.

    **Output**: By using the generated information a preprocessing plan is designed.


*  **Filename**: 3 - preprocessing plan execution

    **Description**: This script apply the preprocessing plan.

    **Output**: Preprocessed dataset,


*  **Filename**: 4 - First Experiment ML

    **Description**: This script run first machine learning experiment (without data augmentation)

    **Output**: Preprocessed dataset.









