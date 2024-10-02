import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load data
df = pd.read_csv("../../data/processed/expansions.csv")

# filter data by expansion types
pre = df[df["expansion_type"] == "pre_expansion"]
insert = df[df["expansion_type"] == "insertion_expansion"]
post = df[df["expansion_type"] == "post_expansion"]

# filter out naked and non-naked expansions
naked = df[df["naked"] == True]
not_naked = df[df["naked"] == False]

expansions = [pre, insert, post]

# absolute count and relative frequency plots
for expansion in expansions:
    sorted_values = expansion["expansion_value"].value_counts().index

    fig, ax1 = plt.subplots(figsize=(30, 10))

    # assign red color to naked values
    colors = ["tab:red" if value == "naked" else "tab:blue" for value in sorted_values]

    # plot absolute counts on the left y-axis
    sns.countplot(
        x="expansion_value", data=expansion, order=sorted_values, ax=ax1, palette=colors
    )

    ax1.set_ylabel("Absolute count", fontsize=20)
    ax1.set_title(
        f'Combined count and relative frequency plot for {expansion["expansion_type"].iloc[0]}'.replace(
            "_", " "
        ),
        fontsize=25,
    )
    ax1.set_xlabel("Expansion value", fontsize=20)
    ax1.tick_params(axis="y", labelsize=20)
    ax1.tick_params(axis="x", labelsize=20)
    plt.xticks(rotation=45)

    # calculate relative frequencies for the right y-axis
    relative_freq = expansion["expansion_value"].value_counts(normalize=True)
    relative_freq_df = relative_freq.reset_index()
    relative_freq_df.columns = ["expansion_value", "relative_frequency"]

    # plot relative frequencies on the right y-axis
    ax2 = ax1.twinx()

    sns.barplot(
        x="expansion_value",
        y="relative_frequency",
        data=relative_freq_df,
        order=sorted_values,
        ax=ax2,
        palette=colors,
    )

    ax2.set_ylabel("Relative frequency", fontsize=20)
    ax2.tick_params(axis="y", labelsize=20)

    plt.show()

# stacked bar chart for all CTs
counts = df.groupby(["expansion_type", "naked"]).size().unstack(fill_value=0)

# reindex counts
expansion_types = ["pre_expansion", "insertion_expansion", "post_expansion"]
counts = counts.reindex(expansion_types)

# convert counts to relative frequencies
relative_counts = counts.div(counts.sum(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(10, 7))

# plot stacked bars
ax.bar(expansion_types, relative_counts[False], label="naked=False", color="tab:blue")
ax.bar(
    expansion_types,
    relative_counts[True],
    bottom=relative_counts[False],
    label="naked=True",
    color="tab:red",
)

plt.title("Relative stacked bar plot of naked expansions by expansion type")
plt.xlabel("Expansion type")
plt.ylabel("Relative frequency")
plt.legend()

plt.show()

# relative frequency plot
# calculate grouped counts
counts = not_naked.groupby(["CT", "expansion_type"]).size().reset_index(name="counts")

# get relative frequencies
counts["relative_freq"] = counts.groupby("CT")["counts"].transform(
    lambda x: x / x.sum()
)

# calculate the mean relative frequencies across all CTs for each expansion type
mean_relative_freqs = counts.groupby("expansion_type")["relative_freq"].mean()

# set the color palette to match the expansion types
colors = sns.color_palette("tab10", 3)

plt.figure(figsize=(30, 10))

# plot relative frequencies
sns.barplot(
    x="CT",
    y="relative_freq",
    hue="expansion_type",
    hue_order=expansion_types,
    data=counts,
)

# add dashed lines for the mean relative frequencies of each expansion type
plt.axhline(
    y=mean_relative_freqs["pre_expansion"], linestyle="--", color=colors[0], label=None
)
plt.axhline(
    y=mean_relative_freqs["insertion_expansion"],
    linestyle="--",
    color=colors[1],
    label=None,
)
plt.axhline(
    y=mean_relative_freqs["post_expansion"], linestyle="--", color=colors[2], label=None
)

plt.title(
    "Relative frequency plot of non-naked expansions by expansion type and CT",
    fontsize=20,
)
plt.xlabel("CT", fontsize=20)
plt.ylabel("Relative frequency (naked=False)", fontsize=20)
plt.xticks(rotation=45, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=15)

plt.show()

# aggregated count plots by CT for naked expansions
# compute the sum of the three expansion types
total_expansions = naked.groupby("CT")["expansion_type"].transform(
    lambda x: x.value_counts().sum()
)

# merge the total expansions with the original DataFrame
total_expansions_df = pd.DataFrame(
    {"total_expansions": total_expansions}, index=naked.index
)
naked_concat = pd.concat([naked, total_expansions_df], axis=1)

# sort by the sum of expansion types
sorted_df = (
    pd.crosstab(naked_concat["CT"], naked_concat["expansion_type"])
    .sum(axis=1)
    .sort_values()
)
sorted_df_index = sorted_df.index
sorted_df = pd.crosstab(naked_concat["CT"], naked_concat["expansion_type"]).loc[
    sorted_df_index
]

# reorder columns based on desired expansion type order
desired_order = ["pre_expansion", "insertion_expansion", "post_expansion"]
sorted_df = sorted_df[desired_order]

# plot the sorted DataFrame
sorted_df.plot.bar(
    stacked=True,
    figsize=(20, 20),
    color=["#1f77b4", "#ff7f0e", "#2ca02c"],
    title="Aggregated count plot of naked expansions by expansion type and CT",
)

plt.show()

# aggregated count plots by case for naked expansions
# compute the sum of the three expansion types
total_expansions = naked.groupby("case")["expansion_type"].transform(
    lambda x: x.value_counts().sum()
)

# merge with the original DataFrame
total_expansions_df = pd.DataFrame(
    {"total_expansions": total_expansions}, index=naked.index
)
naked_concat = pd.concat([naked, total_expansions_df], axis=1)

# sort by the sum of expansion types
sorted_df = (
    pd.crosstab(naked_concat["case"], naked_concat["expansion_type"])
    .sum(axis=1)
    .sort_values()
)
sorted_df_index = sorted_df.index
sorted_df = pd.crosstab(naked_concat["case"], naked_concat["expansion_type"]).loc[
    sorted_df_index
]

# reorder columns
sorted_df = sorted_df[desired_order]

# plot the sorted DataFrame
sorted_df.plot.bar(
    stacked=True,
    figsize=(20, 20),
    title="Aggregated count plot of naked expansions by expansion type and case",
)

plt.show()

# aggregated count plots by CT for non-naked expansions
# compute the sum of the three expansion types
total_expansions = not_naked.groupby("CT")["expansion_type"].transform(
    lambda x: x.value_counts().sum()
)

# merge the total expansions with the original DataFrame
total_expansions_df = pd.DataFrame(
    {"total_expansions": total_expansions}, index=not_naked.index
)
not_naked_concat = pd.concat([not_naked, total_expansions_df], axis=1)

# sort by the sum of expansion types
sorted_df = (
    pd.crosstab(not_naked_concat["CT"], not_naked_concat["expansion_type"])
    .sum(axis=1)
    .sort_values()
)
sorted_df_index = sorted_df.index
sorted_df = pd.crosstab(not_naked_concat["CT"], not_naked_concat["expansion_type"]).loc[
    sorted_df_index
]

# reorder columns
sorted_df = sorted_df[desired_order]

# plot the sorted DataFrame
sorted_df.plot.bar(
    stacked=True,
    figsize=(20, 20),
    title="Aggregated count plot of non-naked expansions by expansion type and CT",
)

plt.show()

# aggregated count plots by case for non-naked expansions
total_expansions = not_naked.groupby("case")["expansion_type"].transform(
    lambda x: x.value_counts().sum()
)

# merge with the original DataFrame
total_expansions_df = pd.DataFrame(
    {"total_expansions": total_expansions}, index=not_naked.index
)
not_naked_concat = pd.concat([not_naked, total_expansions_df], axis=1)

# sort by the sum of expansion types
sorted_df = (
    pd.crosstab(not_naked_concat["case"], not_naked_concat["expansion_type"])
    .sum(axis=1)
    .sort_values()
)
sorted_df_index = sorted_df.index
sorted_df = pd.crosstab(
    not_naked_concat["case"], not_naked_concat["expansion_type"]
).loc[sorted_df_index]

# reorder columns
sorted_df = sorted_df[desired_order]

# plot the sorted DataFrame
sorted_df.plot.bar(
    stacked=True,
    figsize=(20, 20),
    title="Aggregated count plot of non-naked expansions by expansion type and case",
)

plt.show()
