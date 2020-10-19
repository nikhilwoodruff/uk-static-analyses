from openfisca_uk.tools.simulation import model, entity_df, derivative_of
import plotly.graph_objects as go
from plotly.subplots import make_subplots

components = [
    "benunit_income_tax",
    "benunit_NI",
    "JSA_income",
    "income_support",
    "pension_credit",
    "working_tax_credit",
    "child_tax_credit",
    "housing_benefit",
    "universal_credit"
]

sim = model()
benunits = entity_df(sim)

for var in components:
    benunits["d_" + var] = derivative_of(var)
    fig = make_subplots(rows=1, cols=2, start_cell="top-left", subplot_titles=("Amount by family income", "Rate of change w.r.t family income"))
    fig.add_trace(go.Scatter(x=benunits["benunit_income"], y=benunits[var], mode="markers"), row=1, col=1)
    fig.add_trace(go.Scatter(x=benunits["benunit_income"], y=benunits["d_" + var], mode="markers"), row=1, col=2)
    fig.update_xaxes(title_text="Family income", range=[-100, 1100], row=1, col=1)
    fig.update_xaxes(title_text="Family income", range=[-100, 1100], row=1, col=2)
    fig.update_yaxes(title_text="Amount per week", range=[-100, 500], row=1, col=1)
    fig.update_yaxes(title_text="Rate of change", range=[-1.5, 1.5], row=1, col=2)
    fig.update_layout(title_text=var)
    fig.show()