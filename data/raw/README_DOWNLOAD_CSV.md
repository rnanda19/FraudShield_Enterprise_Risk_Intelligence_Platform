# creditcard.csv is delivered separately

Due to a 30 MB per-file upload limit in this chat, the 98 MB raw dataset
(`creditcard.csv`) could not be bundled directly into this zip.

It was delivered as split, gzip-compressed parts alongside this zip:
`creditcard.csv.gz.part-aa`, `creditcard.csv.gz.part-ab`, ...

To reassemble it into this folder:

**macOS / Linux:**
```bash
cat creditcard.csv.gz.part-* > creditcard.csv.gz
gunzip creditcard.csv.gz
mv creditcard.csv Fraud_Detection_Platform/data/raw/creditcard.csv
```

**Windows (PowerShell):**
```powershell
cmd /c copy /b creditcard.csv.gz.part-aa+creditcard.csv.gz.part-ab+... creditcard.csv.gz
# then use 7-Zip or a similar tool to gunzip creditcard.csv.gz
```

Alternatively, download the same dataset directly from Kaggle:
`mlg-ulb/creditcardfraud` — it should verify to exactly 284,807 rows,
492 fraud cases, 0.172749% fraud rate, 31 columns.
