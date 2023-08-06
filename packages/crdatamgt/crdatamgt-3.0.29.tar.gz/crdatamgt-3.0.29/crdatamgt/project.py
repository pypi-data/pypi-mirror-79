import datetime
import os
import re

import crdatamgt.topic as topic
from crdatamgt.formulations import (
    formulations_for_log_file,
    update_formulation_table,
)
from crdatamgt.helpers import (
    topic_directories,
    workbook_load_file,
    workbook_save,
    rename_dictionary,
)
from xloaderx.loading import loading
from crdatamgt.offlinestats import *

log = logger()


def project_load_from_workbooks(workbooks, **kwargs):
    result_wb = workbooks
    project_sheets = []
    formulation_sheets = []
    formatting = {}
    acquisition_sheets = []
    results_sheets = []
    load_indicator = loading(len(result_wb))
    if kwargs.get("OUTPUT DIRECTORY"):
        output_path = kwargs.get("OUTPUT DIRECTORY")
    else:
        output_path = os.path.split(kwargs.get("RESULTS DIRECTORY"))[0]
    for result in result_wb:
        next(load_indicator)
        result_data = topic.read_topic(result)
        formulation_data = result_data.pop("Formulation", pd.DataFrame())
        if not formulation_data.dropna(how="all").empty:
            try:
                formulation_data.loc[:, "Topic ID"] = (
                    result_data.get("Summary").get("Topic ID").values[0]
                )
                formulation_sheets.append(formulation_data)
            except ValueError as VE:
                raise VE
        else:
            try:
                log.debug(
                    f"No Formulation data for Topic ID:{result_data.get('Summary').get('Topic ID').values}"
                )
            except AttributeError:
                log.debug(f"Strange data set here: {str(result_data)}")
        acq_data = result_data.get("Aquisition set up").copy()
        if not acq_data.dropna(how="all").empty:
            acq_data.loc[:, "Topic ID"] = (
                result_data.get("Summary").get("Topic ID").values
            )
            acquisition_sheets.append(acq_data)
        results_for_later = result_data.get("Results").copy()
        if not results_for_later.dropna(how="all").empty:
            try:
                results_for_later.loc[:, "Topic ID"] = (
                    result_data.get("Summary").get("Topic ID").values
                )
            except ValueError:
                topic_id = result_data.get("Summary").get("Topic ID").values[0]
                results_for_later.loc[:, "Topic ID"] = topic_id
            results_sheets.append(results_for_later)
        normal_sheets = pd.concat(result_data.values(), axis=1, sort=False)
        project_sheets.append(normal_sheets)
    try:
        compiled = (
            pd.concat(project_sheets[::-1], sort=False)
            .set_index("Topic ID")
            .sort_index()
            .reset_index()
            .drop(columns=["Test"], errors="ignore")
        )
    except ValueError as e:
        # This is often due to a duplication in one of the topics.
        for df in project_sheets:
            if df.columns.duplicated().any():
                log.info(
                    f"Suspected duplication event: {df.columns.duplicated()} : {df['Topic ID']}"
                )

    cleaned_formulations = formulation_work(formulation_sheets)
    update_formulation_table(
        cleaned_formulations.drop(columns="topic id", errors="ignore"),
        kwargs.get("FORMULATION DIRECTORY"),
    )
    updated_formulations = formulations_for_log_file(cleaned_formulations)
    compiled = compiled.merge(updated_formulations, how="outer")
    # Hopefully this is sufficient to filter

    formatting["header"] = {
        "bold": True,
        "text_wrap": False,
        "valign": "top",
        "fg_color": "#D7E4BC",
        "border": 1,
        "font_size": 16,
    }

    # Write the column headers with the defined format.

    project_name = re.search(r"\\(Project .*)\\", kwargs.get("RESULTS DIRECTORY"))[1]
    dt = datetime.datetime.now().strftime("%d_%m_%Y")
    excel_name = f"{project_name}_{dt}"
    report_path = os.path.join(output_path, "Reports")
    archive_path = os.path.join(report_path, "archives")
    mkdir_or_pass(report_path)
    mkdir_or_pass(archive_path)

    if compiled.keys().isin(["Denuder type"]).any():
        compiled = denuder(compiled, acquisition_sheets, results_sheets)
        cross = cross_topic(compiled, acquisition_sheets, results_sheets)
        stats_path = os.path.join(report_path, "stats")
        mkdir_or_pass(stats_path)
        workbook_save(
            f"{project_name} stats", stats_path, cross, project_name, **formatting
        )

    workbook_save(excel_name, archive_path, compiled, project_name, **formatting)
    workbook_save(project_name, report_path, compiled, project_name, **formatting)


def mkdir_or_pass(stats_path):
    try:
        os.mkdir(stats_path)
    except FileExistsError:
        pass


def project_load(**kwargs):
    if kwargs.get("TOPIC STRUCTURED"):
        topic_name, topic_path = topic_directories(kwargs.get("PROJECT DIRECTORY"))
        workbooks = [topic.load_topic(t_path) for t_path in topic_path]
        project_load_from_workbooks(workbooks, **kwargs)
    else:
        workbooks = workbook_load_file(kwargs.get("RESULTS DIRECTORY"))
        project_load_from_workbooks(workbooks, **kwargs)


def formulation_work(data_frame_list):
    cleaned = [sheet.dropna(how="all") for sheet in data_frame_list]
    cleaned = list(
        map(
            lambda sheet: sheet.rename(str.lower, axis="columns").rename(
                columns=rename_dictionary()
            ),
            cleaned,
        )
    )
    clean_frame = pd.concat(cleaned)
    clean_frame.drop_duplicates(inplace=True)
    clean_frame.reset_index(inplace=True)
    clean_frame.drop(
        columns=["index", "units", "formulation"], errors="ignore", inplace=True
    )
    clean_frame.dropna(how="all", inplace=True)
    return clean_frame
