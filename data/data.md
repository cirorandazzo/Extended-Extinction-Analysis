# Extended Extinction Data
data.md, created 2023.03.07

## Dates

EE1 and EE2 were scored by Melissa in summer 2022. To account for any updates that were corrected following discrepancy with second scorer (Harshi), these files have been replaced with updated copies (2023.03.07).

## Files & Formats

Folder `Scoring Sheets` contains the original scorer's sheets. These contain scored freezing times as well as observations or other issues with behavioral session, video recording, etc.

Raw scoring sheets have been cleaned and organized into files by group and scorer (formerly, in folder `2022.07`: separate csv for each behavioral session. fortunately, someone learned about `pd.read_excel`). These separated and cleaned files are named GROUP CODE + SCORER INTIALS.xlsx (eg, `ee1-mk.xlsx`), and have as many sheets as behavior sessions in that group's experimental paradigm.

## Notes

- Second scorer on `ee2-cdr.xlsx` was CDR for some behavior sessions, HP for other sessions.
- `ee1_2-mk-pivoted.csv` is a sample df after pivoting for pinguoin input (see `stats.py` function `_pivot_df`)
- EET A3 excluded for insufficient conditioned fear response directly following AFC (D2, conditioned fear response test/Fear Recall)