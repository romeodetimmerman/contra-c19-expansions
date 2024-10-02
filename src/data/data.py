import pandas as pd

codes = pd.read_csv("../../data/raw/contra-c19-codes.csv")

# drop redundant codes
codes = codes.drop(
    columns=[
        "Color",
        "Weight score",
        "Created by",
        "Created",
        "Comment",
        "Document group",
        "Area",
        "Coverage %",
        "Beginning",
        "End",
    ]
)

# set keys to lowercase
codes.columns = codes.columns.str.lower()

# extract case, ct and ib variables
df = (
    codes["document name"]
    .astype(str)
    .str.extract(r"([ABC]\d\d\d)_(CT\d\d\d)_(IB\d\d\d)")
)
codes["case"] = df[0]
codes["CT"] = df[1]
codes["IB"] = df[2]
codes = codes.drop(columns="document name").sort_values("CT")

# extract questions
questions = codes[codes["code"].str.startswith("turn_taking > questions")].copy()
questions["question"] = pd.factorize(questions.segment)[0] + 1

# extract expansions
expansions = questions[questions["code"].str.contains("expansion")].copy()
temp = expansions["code"].str.split(" > ")
expansions["expansion_type"] = temp.str[-2]
expansions["expansion_value"] = temp.str[-1]
expansions.drop(columns="code", inplace=True)
expansions["naked"] = expansions["expansion_value"].str.contains("naked")
expansions["expansion_type"] = expansions["expansion_type"].replace(
    {
        "prefacing": "pre_expansion",
        "insertions": "insertion_expansion",
        "post_sequences": "post_expansion",
    }
)

expansions.to_csv("../../data/processed/expansions.csv", index=False)
