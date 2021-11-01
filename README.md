# Journal Abbreviation Generator

A simple program for quickly and accurately abbreviating all the journals and conferences inside of a .bib file. All abbreviations follow the guidelines of Standard Journal Abbreviation [(ISO4)](https://en.wikipedia.org/wiki/ISO_4). What is required is that the bibliographies contained within the target .bib file follow BibTex format. Consider the example below.

```bibtex
@article{flamino2021creation,
  title={Creation, evolution, and dissolution of social groups},
  author={Flamino, James and Szymanski, Boleslaw K and Bahulkar, Ashwin and Chan, Kevin and Lizardo, Omar},
  journal={Scientific Reports},
  volume={11},
  number={1},
  pages={1--11},
  year={2021},
  publisher={Nature Publishing Group}
}
```

This program will swap **Scientific Reports** with **Sci. Rep.** and output the BibTex reference with the changes made. This can be done automatically for as many items as needed, and covers both `journal={}` and `booktitle={}` calls.

## Setup

After cloning the repository call

```bash
pip install -r requirements.txt
python -m spacy download en
```

This will install all required dependencies. To run the abbreviation program, call

```bash
python abbreviate_journals.py <fname>
```

Where `<fname>` is the name of the input file. The program will automatically abbreviate all entries within and output the results to the same directory with an added **_abbrev** descriptor to the outputted filename. Note that the input file does not actually need to have a `.bib` file extension for the program to work.

## Updating Abbreviations

After the abbreviations have been made, the program will alert you to words that had no clear abbreviation, as well as journals that could not be correctly abbreviated. For the former problem, you can add additional abbreviations to the YAML file found at `abbreviations/abbrevs.yml` to help the program find the correct abbreviations. For the latter problem, manual abbreviations are required.

To update the YAML file, follow the example below.

```yaml
Full word: Abbreviation.
```

The full word must be a singular word with the first letter capitalized, and the abbreviation must end in a period and also have its first letter capitalized.
