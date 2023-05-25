# Data analysis project

Our project is titled **Robotics across industries** and is about the development of robots in different industries and the resulting effect on productivity.

# \[Group: bpr871\]

***Group members:***
- Sissel Marie Andersen (bpr871)
- Hjalte Bisgaard (lfc749)
- Julie Skaarup Roesgaard (spr506)

The **results** of the project can be seen from running [dataproject.ipynb](dataproject.ipynb).

We apply the **following datasets**:

1. NP25.csv (*[source](https://www.statistikbanken.dk/np25)*) 
2. ifr_dk.csv (*source*)
3. NABB69 from Danmarks Statistik (*[source](https://www.statistikbanken.dk/statbank5a/SelectVarVal/Define.asp?MainTable=NABB69&PLanguage=0&PXSId=0&wsid=cftree)*)

We import the following dictionaries from the file **dict.py**:
1. **dict_crosswalk:** Contains a crosswalk file for converting the industry classifications from Danmarks Statistik in to the classification system from the Industrial Federation of Robotics.
2. **dict_legend:**    Translation for the industry classifications for IFR in to names suitable as legend titles.
