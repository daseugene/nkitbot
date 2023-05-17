import pandas as pd
import glob
import tabula

pdf_files = glob.glob('*.pdf')

print(pdf_files)

pdf_tables = tabula.read_pdf(pdf_files[0],
                             pages='all',
                             multiple_tables=True,
                             encoding='windows-1251',
                             lattice=True)


print(pdf_tables[0].columns[5])
print(pdf_tables[0].iloc[5])

sample_table = pdf_tables[0][:80]

sample_table.columns = sample_table.iloc[-10]

print(sample_table.columns)

print(sample_table)

