"""Simple Shiny app to explore gnomAD v4.1 summary statistics."""

import plotly.graph_objects as go
from plotly.graph_objs import FigureWidget
from shared import POP_NAMES, app_dir, color_map, df, gen_anc_order_mapped, metrics
from shiny import reactive
from shiny import ui as sui
from shiny.express import input, render, ui
from shinywidgets import render_widget

ui.include_css(app_dir / "styles.css")
ui.page_opts(
    title=sui.row(
        sui.column(4, ui.img(src="gnomad_logo.png", height="75")),
        sui.column(
            8,
            ui.div(
                {"style": "font-weight: bold; font-size: 30px;"},
                ui.p("      v4.1 summary stats"),
            ),
        ),
    ),
    # full_width=True,
    fillable=True,
)

with ui.sidebar(title="Filter controls"):
    ui.input_selectize(
        "select_metric", "Select Metric", choices=metrics, selected="n_non_ref"
    )
    ui.input_switch("variant_qc_pass", "Pass variant QC", True)
    ui.input_selectize(
        "sex_chr_nonpar_group",
        "Select autosome/PAR or non-PAR",
        choices=["autosome_or_par", "x_nonpar", "y_nonpar"],
        selected="autosome_or_par",
    )
    ui.input_selectize(
        "capture",
        "Filter by capture intervals",
        choices=["", "ukb_broad_union", "broad", "ukb", "ukb_broad_intersect"],
        selected="",
    )
    ui.input_selectize(
        "csq_set",
        "Filter by CSQ set",
        choices=["", "non-coding", "coding", "lof"],
        selected="",
    )
    ui.input_selectize(
        "csq",
        "Filter by CSQ",
        choices=[
            "",
            "missense_variant",
            "synonymous_variant",
            "frameshift_variant",
            "intergenic_variant",
            "intron_variant",
            "splice_region_variant",
            "stop_gained",
            "splice_donor_variant",
            "splice_acceptor_variant",
        ],
        selected="",
    )
    ui.input_selectize(
        "loftee_label", "Filter by LOFTEE label", choices=["", "HC", "LC"], selected=""
    )
    ui.input_selectize(
        "loftee_flags",
        "Filter by LOFTEE flags",
        choices=["", "no_flags", "with_flags"],
        selected="",
    )
    ui.input_selectize(
        "max_af",
        "Filter by max AF",
        choices=["", "0.0001", "0.001", "0.01"],
        selected="",
    )

with ui.layout_column_wrap(fill=False):
    with ui.value_box():
        "Number of rows"

        @render.text
        def count():
            """Get the number of rows in the filtered dataframe."""
            return filtered_df().shape[0]

    with ui.value_box():
        "Full dataset mean"

        @render.text
        def bill_length():
            """Get the global mean of the selected metric."""
            return f"{filtered_df_global_mean():.1f}"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Per-sample summary statistics distributions")

        # @output(suspend_when_hidden=False)
        @render_widget
        def length_depth():
            """Create a boxplot of the selected metric."""
            filt_df = filtered_df()
            return create_boxplot_figure(filt_df)

    with ui.card(full_screen=True):
        ui.card_header("")

        @render.data_frame
        def summary_statistics():
            """Show the summary statistics."""
            cols = [
                "subset",
                "gen_anc",
                "sex_chr_nonpar_group",
                "variable",
                "value",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


@reactive.calc
def metric_filtered_df():
    """Filter the dataframe based on the selected metric and other filters."""
    metric = input.select_metric()
    variant_qc_pass = "pass" if input.variant_qc_pass() else ""
    sex_chr_nonpar_group = input.sex_chr_nonpar_group()
    capture = input.capture()
    csq_set = input.csq_set()
    csq = input.csq()
    loftee_label = input.loftee_label()
    loftee_flags = input.loftee_flags()
    max_af = input.max_af()
    filt_df = df[
        (df["sex_chr_nonpar_group"] == sex_chr_nonpar_group)
        & (df["variant_qc"] == variant_qc_pass)
        & (df["capture"] == capture)
        & (df["csq_set"] == csq_set)
        & (df["csq"] == csq)
        & (df["loftee_label"] == loftee_label)
        & (df["loftee_flags"] == loftee_flags)
        & (df["max_af"] == max_af)
    ]
    rename_map = {
        "min": "Minimum",
        "q25": "Q1",
        "q50": "Median",
        "q75": "Q3",
        "max": "Maximum",
        "mean": "Mean",
    }
    filt_df = filt_df.rename(
        columns={f"{metric}_{k}": v for k, v in rename_map.items()}
    )

    id_vars = [
        "subset",
        "gen_anc",
        "sex_chr_nonpar_group",
        "variant_qc",
        "capture",
        "csq_set",
        "csq",
        "loftee_label",
        "loftee_flags",
        "max_af",
    ]
    filt_df = filt_df[id_vars + ["Minimum", "Q1", "Median", "Q3", "Maximum", "Mean"]]

    return filt_df


@reactive.calc
def filtered_df():
    """Filter the dataframe based on the selected metric and other filters."""
    # gen_ancs = input.gen_anc()
    filt_df = metric_filtered_df()
    filt_df = filt_df.replace({"gen_anc": POP_NAMES})
    # filt_df = filt_df[filt_df["gen_anc"].isin(gen_ancs)]
    id_vars = [
        "subset",
        "gen_anc",
        "sex_chr_nonpar_group",
        "variant_qc",
        "capture",
        "csq_set",
        "csq",
        "loftee_label",
        "loftee_flags",
        "max_af",
    ]
    filt_df = filt_df.drop(columns=["Mean"])
    filt_df = filt_df.melt(id_vars=id_vars, value_name="value")

    return filt_df


def filtered_df_global_mean():
    """Get the global mean of the selected metric."""
    filt_df = metric_filtered_df()
    filt_df = filt_df[
        (filt_df["gen_anc"] == "global") & (filt_df["subset"] == "gnomad")
    ]
    filt_df = filt_df.reset_index()
    return filt_df.at[0, "Mean"]


# Function to create the Plotly FigureWidget.
def create_boxplot_figure(data):
    """Create a boxplot figure."""
    fig = go.Figure()

    for gen_anc in gen_anc_order_mapped:
        fig.add_trace(
            go.Box(
                x=data[data["gen_anc"] == gen_anc]["subset"],
                y=data[data["gen_anc"] == gen_anc]["value"],
                name=gen_anc,
                marker_color=color_map[gen_anc],
                quartilemethod="exclusive",
            )
        )
    fig.update_layout(
        template="simple_white",
        legend_title="Genetic Ancestry",
        xaxis_title="Subset",
        yaxis_title="Value",
        showlegend=True,
        # group together boxes of the different traces for each value of x
        boxmode="group",
    )
    return FigureWidget(fig)
