import microdf as mdf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib as mpl

# Reform 1 % coming out ahead/behind
df = pd.read_csv("analyses\household_results.csv")

EI_BIN_LABELS = list(map(str, range(10)))
df["ei_bin"] = pd.cut(
    df["baseline_equiv_household_net_income_bhc"].astype("int"),
    pd.Series([0, 212, 307, 396, 495, 596, 704, 839, 1025, 1351, np.inf]),
    labels=EI_BIN_LABELS,
)
df["pct_change"] = (
    df["reform_1_equiv_household_net_income_bhc"]
    - df["baseline_equiv_household_net_income_bhc"]
) / df["baseline_equiv_household_net_income_bhc"]
DI_PCTCHG_BIN_LABELS = [
    "Decrease greater than 5%",
    "Decrease less than 5%",
    "Increase less than 5%",
    "Increase greater than 5%",
]
df["pct_chg_bin"] = pd.cut(
    df["pct_change"],
    [-np.inf, -0.05, 0, 0.05, np.inf],
    include_lowest=True,  # For -np.inf.
    labels=DI_PCTCHG_BIN_LABELS,
).astype(
    str
)  # Groupby screws up categoricals.


def reversed_list(l):
    return l[::-1]


def combined_pivot(group_bin, chg_bin, weight):
    pivot = df.pivot_table(
        index=group_bin,
        columns=chg_bin,
        values=weight,
        aggfunc=sum,
        fill_value=0,
    )
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0)
    pivot_total = df.pivot_table(
        columns=chg_bin, values=weight, aggfunc=sum, fill_value=0
    )
    pivot_total_pct = pivot_total.div(pivot_total.sum(axis=1), axis=0)
    pivot_total_pct.index = ["Total"]
    # Create empty row to distinguish total row.
    pivot_empty = pivot_total_pct.copy()
    pivot_empty.loc[:] = None
    pivot_empty.index = [""]
    # Can't concat in the correct order:
    # TypeError: cannot append a non-category item to a CategoricalIndex
    # Instead reorder in a separate step.
    pivot_combined_pct = pd.concat([pivot_total_pct, pivot_pct, pivot_empty])
    res = (
        pivot_combined_pct.iloc[1:]
        .append(pivot_combined_pct.iloc[0])
        .iloc[:, ::-1]
    )
    # Have column order work for table.
    return res[reversed_list(DI_PCTCHG_BIN_LABELS)]


print(combined_pivot("ei_bin", "pct_chg_bin", "household_weight"))

COLORS = [
    "#004ba0",  # Dark blue.
    "#63a4ff",  # Light blue.
    "#ffc046",  # Light amber.
    "#c56000",
]  # Medium amber.


def dist_plot(income_bin, chg_bin, weight):
    ax = combined_pivot(income_bin, chg_bin, weight).plot.barh(
        stacked=True, color=COLORS, width=0.97, figsize=(11, 8)
    )
    legend = plt.legend(
        bbox_to_anchor=(-0.005, 1.0, 0.96, 0.102),
        loc=3,
        ncol=4,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    plt.setp(plt.gca().get_legend().get_texts(), fontsize=10)
    sns.despine(left=True, bottom=True)
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda y, _: "{:.0%}".format(y))
    )
    ax.set(xlabel="", ylabel="Household income")
    plt.title(
        "Distribution of "
        + ("tax returns" if weight == "s006" else "people")
        + " by "
        + (
            "size of tax change"
            if chg_bin == "tax_chg_bin"
            else "effect on disposable income"
        ),
        loc="left",
        y=1.05,
        fontsize=24,
    )
    return ax


ax = dist_plot("ei_bin", "pct_chg_bin", "household_weight")
plt.show()

# Reform 2 % coming out ahead/behind
df = pd.read_csv("analyses\household_results.csv")
EI_BIN_LABELS = list(map(str, range(10)))
df["ei_bin"] = pd.cut(
    df["baseline_equiv_household_net_income_bhc"].astype("int"),
    pd.Series([0, 212, 307, 396, 495, 596, 704, 839, 1025, 1351, np.inf]),
    labels=EI_BIN_LABELS,
)
df["pct_change"] = (
    df["reform_2_equiv_household_net_income_bhc"]
    - df["baseline_equiv_household_net_income_bhc"]
) / df["baseline_equiv_household_net_income_bhc"]
DI_PCTCHG_BIN_LABELS = [
    "Decrease greater than 5%",
    "Decrease less than 5%",
    "Increase less than 5%",
    "Increase greater than 5%",
]
df["pct_chg_bin"] = pd.cut(
    df["pct_change"],
    [-np.inf, -0.05, 0, 0.05, np.inf],
    include_lowest=True,  # For -np.inf.
    labels=DI_PCTCHG_BIN_LABELS,
).astype(
    str
)  # Groupby screws up categoricals.


def reversed_list(l):
    return l[::-1]


def combined_pivot(group_bin, chg_bin, weight):
    pivot = df.pivot_table(
        index=group_bin,
        columns=chg_bin,
        values=weight,
        aggfunc=sum,
        fill_value=0,
    )
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0)
    pivot_total = df.pivot_table(
        columns=chg_bin, values=weight, aggfunc=sum, fill_value=0
    )
    pivot_total_pct = pivot_total.div(pivot_total.sum(axis=1), axis=0)
    pivot_total_pct.index = ["Total"]
    # Create empty row to distinguish total row.
    pivot_empty = pivot_total_pct.copy()
    pivot_empty.loc[:] = None
    pivot_empty.index = [""]
    # Can't concat in the correct order:
    # TypeError: cannot append a non-category item to a CategoricalIndex
    # Instead reorder in a separate step.
    pivot_combined_pct = pd.concat([pivot_total_pct, pivot_pct, pivot_empty])
    res = (
        pivot_combined_pct.iloc[1:]
        .append(pivot_combined_pct.iloc[0])
        .iloc[:, ::-1]
    )
    # Have column order work for table.
    return res[reversed_list(DI_PCTCHG_BIN_LABELS)]


print(combined_pivot("ei_bin", "pct_chg_bin", "household_weight"))

COLORS = [
    "#004ba0",  # Dark blue.
    "#63a4ff",  # Light blue.
    "#ffc046",  # Light amber.
    "#c56000",
]  # Medium amber.


def dist_plot(income_bin, chg_bin, weight):
    ax = combined_pivot(income_bin, chg_bin, weight).plot.barh(
        stacked=True, color=COLORS, width=0.97, figsize=(11, 8)
    )
    legend = plt.legend(
        bbox_to_anchor=(-0.005, 1.0, 0.96, 0.102),
        loc=3,
        ncol=4,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    plt.setp(plt.gca().get_legend().get_texts(), fontsize=10)
    sns.despine(left=True, bottom=True)
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda y, _: "{:.0%}".format(y))
    )
    ax.set(xlabel="", ylabel="Household income")
    plt.title(
        "Distribution of "
        + ("tax returns" if weight == "s006" else "people")
        + " by "
        + (
            "size of tax change"
            if chg_bin == "tax_chg_bin"
            else "effect on disposable income"
        ),
        loc="left",
        y=1.05,
        fontsize=24,
    )
    return ax


ax = dist_plot("ei_bin", "pct_chg_bin", "household_weight")
plt.show()

# Reform 3 % coming out ahead/behind
df = pd.read_csv("analyses\household_results.csv")
EI_BIN_LABELS = list(map(str, range(10)))
df["ei_bin"] = pd.cut(
    df["baseline_equiv_household_net_income_bhc"].astype("int"),
    pd.Series([0, 212, 307, 396, 495, 596, 704, 839, 1025, 1351, np.inf]),
    labels=EI_BIN_LABELS,
)
df["pct_change"] = (
    df["reform_3_equiv_household_net_income_bhc"]
    - df["baseline_equiv_household_net_income_bhc"]
) / df["baseline_equiv_household_net_income_bhc"]
DI_PCTCHG_BIN_LABELS = [
    "Decrease greater than 5%",
    "Decrease less than 5%",
    "Increase less than 5%",
    "Increase greater than 5%",
]
df["pct_chg_bin"] = pd.cut(
    df["pct_change"],
    [-np.inf, -0.05, 0, 0.05, np.inf],
    include_lowest=True,  # For -np.inf.
    labels=DI_PCTCHG_BIN_LABELS,
).astype(
    str
)  # Groupby screws up categoricals.


def reversed_list(l):
    return l[::-1]


def combined_pivot(group_bin, chg_bin, weight):
    pivot = df.pivot_table(
        index=group_bin,
        columns=chg_bin,
        values=weight,
        aggfunc=sum,
        fill_value=0,
    )
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0)
    pivot_total = df.pivot_table(
        columns=chg_bin, values=weight, aggfunc=sum, fill_value=0
    )
    pivot_total_pct = pivot_total.div(pivot_total.sum(axis=1), axis=0)
    pivot_total_pct.index = ["Total"]
    # Create empty row to distinguish total row.
    pivot_empty = pivot_total_pct.copy()
    pivot_empty.loc[:] = None
    pivot_empty.index = [""]
    # Can't concat in the correct order:
    # TypeError: cannot append a non-category item to a CategoricalIndex
    # Instead reorder in a separate step.
    pivot_combined_pct = pd.concat([pivot_total_pct, pivot_pct, pivot_empty])
    res = (
        pivot_combined_pct.iloc[1:]
        .append(pivot_combined_pct.iloc[0])
        .iloc[:, ::-1]
    )
    # Have column order work for table.
    return res[reversed_list(DI_PCTCHG_BIN_LABELS)]


print(combined_pivot("ei_bin", "pct_chg_bin", "household_weight"))

COLORS = [
    "#004ba0",  # Dark blue.
    "#63a4ff",  # Light blue.
    "#ffc046",  # Light amber.
    "#c56000",
]  # Medium amber.


def dist_plot(income_bin, chg_bin, weight):
    ax = combined_pivot(income_bin, chg_bin, weight).plot.barh(
        stacked=True, color=COLORS, width=0.97, figsize=(11, 8)
    )
    legend = plt.legend(
        bbox_to_anchor=(-0.005, 1.0, 0.96, 0.102),
        loc=3,
        ncol=4,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    plt.setp(plt.gca().get_legend().get_texts(), fontsize=10)
    sns.despine(left=True, bottom=True)
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda y, _: "{:.0%}".format(y))
    )
    ax.set(xlabel="", ylabel="Household income")
    plt.title(
        "Distribution of "
        + ("tax returns" if weight == "s006" else "people")
        + " by "
        + (
            "size of tax change"
            if chg_bin == "tax_chg_bin"
            else "effect on disposable income"
        ),
        loc="left",
        y=1.05,
        fontsize=24,
    )
    return ax


ax = dist_plot("ei_bin", "pct_chg_bin", "household_weight")
plt.show()

# Reform 4 % coming out ahead/behind
df = pd.read_csv("analyses\household_results.csv")
EI_BIN_LABELS = list(map(str, range(10)))
df["ei_bin"] = pd.cut(
    df["baseline_equiv_household_net_income_bhc"].astype("int"),
    pd.Series([0, 212, 307, 396, 495, 596, 704, 839, 1025, 1351, np.inf]),
    labels=EI_BIN_LABELS,
)
df["pct_change"] = (
    df["reform_4_equiv_household_net_income_bhc"]
    - df["baseline_equiv_household_net_income_bhc"]
) / df["baseline_equiv_household_net_income_bhc"]
DI_PCTCHG_BIN_LABELS = [
    "Decrease greater than 5%",
    "Decrease less than 5%",
    "Increase less than 5%",
    "Increase greater than 5%",
]
df["pct_chg_bin"] = pd.cut(
    df["pct_change"],
    [-np.inf, -0.05, 0, 0.05, np.inf],
    include_lowest=True,  # For -np.inf.
    labels=DI_PCTCHG_BIN_LABELS,
).astype(
    str
)  # Groupby screws up categoricals.


def reversed_list(l):
    return l[::-1]


def combined_pivot(group_bin, chg_bin, weight):
    pivot = df.pivot_table(
        index=group_bin,
        columns=chg_bin,
        values=weight,
        aggfunc=sum,
        fill_value=0,
    )
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0)
    pivot_total = df.pivot_table(
        columns=chg_bin, values=weight, aggfunc=sum, fill_value=0
    )
    pivot_total_pct = pivot_total.div(pivot_total.sum(axis=1), axis=0)
    pivot_total_pct.index = ["Total"]
    # Create empty row to distinguish total row.
    pivot_empty = pivot_total_pct.copy()
    pivot_empty.loc[:] = None
    pivot_empty.index = [""]
    # Can't concat in the correct order:
    # TypeError: cannot append a non-category item to a CategoricalIndex
    # Instead reorder in a separate step.
    pivot_combined_pct = pd.concat([pivot_total_pct, pivot_pct, pivot_empty])
    res = (
        pivot_combined_pct.iloc[1:]
        .append(pivot_combined_pct.iloc[0])
        .iloc[:, ::-1]
    )
    # Have column order work for table.
    return res[reversed_list(DI_PCTCHG_BIN_LABELS)]


print(combined_pivot("ei_bin", "pct_chg_bin", "household_weight"))

COLORS = [
    "#004ba0",  # Dark blue.
    "#63a4ff",  # Light blue.
    "#ffc046",  # Light amber.
    "#c56000",
]  # Medium amber.


def dist_plot(income_bin, chg_bin, weight):
    ax = combined_pivot(income_bin, chg_bin, weight).plot.barh(
        stacked=True, color=COLORS, width=0.97, figsize=(11, 8)
    )
    legend = plt.legend(
        bbox_to_anchor=(-0.005, 1.0, 0.96, 0.102),
        loc=3,
        ncol=4,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    plt.setp(plt.gca().get_legend().get_texts(), fontsize=10)
    sns.despine(left=True, bottom=True)
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda y, _: "{:.0%}".format(y))
    )
    ax.set(xlabel="", ylabel="Household income")
    plt.title(
        "Distribution of "
        + ("tax returns" if weight == "s006" else "people")
        + " by "
        + (
            "size of tax change"
            if chg_bin == "tax_chg_bin"
            else "effect on disposable income"
        ),
        loc="left",
        y=1.05,
        fontsize=24,
    )
    return ax


ax = dist_plot("ei_bin", "pct_chg_bin", "household_weight")
plt.show()

# Reform 1 Quantile % change to disposable income
mdf.quantile_pct_chg_plot(
    df1=df,
    df2=df,
    col1="baseline_equiv_household_net_income_bhc",
    col2="reform_1_equiv_household_net_income_bhc",
    w1="household_weight",
    w2="household_weight",
)

# Note: Must set `loc='left'`, otherwise two titles will overlap.
plt.title("Reform 1: Change to disposable income percentiles", loc="left")
plt.xlabel("Disposable income percentile")
plt.ylabel("Change to disposable income at the percentile boundary")
plt.show()

# Reform 2 Quantile % change to disposable income
mdf.quantile_pct_chg_plot(
    df1=df,
    df2=df,
    col1="baseline_equiv_household_net_income_bhc",
    col2="reform_2_equiv_household_net_income_bhc",
    w1="household_weight",
    w2="household_weight",
)

# Note: Must set `loc='left'`, otherwise two titles will overlap.
plt.title("Reform 2: Change to disposable income percentiles", loc="left")
plt.xlabel("Disposable income percentile")
plt.ylabel("Change to disposable income at the percentile boundary")
plt.show()

# Reform 3 Quantile % change to disposable income
mdf.quantile_pct_chg_plot(
    df1=df,
    df2=df,
    col1="baseline_equiv_household_net_income_bhc",
    col2="reform_3_equiv_household_net_income_bhc",
    w1="household_weight",
    w2="household_weight",
)

# Note: Must set `loc='left'`, otherwise two titles will overlap.
plt.title("Reform 3: Change to disposable income percentiles", loc="left")
plt.xlabel("Disposable income percentile")
plt.ylabel("Change to disposable income at the percentile boundary")
plt.show()

# Reform 4 Quantile % change to disposable income
mdf.quantile_pct_chg_plot(
    df1=df,
    df2=df,
    col1="baseline_equiv_household_net_income_bhc",
    col2="reform_4_equiv_household_net_income_bhc",
    w1="household_weight",
    w2="household_weight",
)

# Note: Must set `loc='left'`, otherwise two titles will overlap.
plt.title("Reform 4: Change to disposable income percentiles", loc="left")
plt.xlabel("Disposable income percentile")
plt.ylabel("Change to disposable income at the percentile boundary")
plt.show()
