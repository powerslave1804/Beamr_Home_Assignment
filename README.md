# Beamr_Home_Assignment

## Task 1 – Application Testing (JPEGmini Pro)

The test cases and bug reports for the JPEGmini Pro application are available in [Test_cases_MiniMe.xlsx](jm-test/Test_cases_MiniMe.xlsx).

The spreadsheet contains the test cases created for the application, along with the identified bugs and their details.

## Task 2 – QP Analysis with x264

The analysis script runs x264 encoding on the `foreman-cif.yuv` test video using different QP values and collects the resulting file size, encoding speed (FPS), and bitrate.

The results are saved in [qp_results.csv](script/qp_results.csv) and visualized in the following graphs.

### QP vs File Size

![QP vs File Size](script/qp_vs_filesize.png)

### QP vs FPS

![QP vs FPS](script/qp_vs_fps.png)

The results show that file size and bitrate generally decrease as QP increases, while encoding speed varies across QP values.

## Requirements

* Python 3.10+
* matplotlib
* pandas
* xlsxwriter

## How to Run

Run the following commands from the `script` directory.

1. Create a virtual environment:

   
   python -m venv venv
   

2. Activate the virtual environment on Windows:

   
   venv\Scripts\activate
   

3. Install the dependencies:

   
   pip install -r requirements.txt
   

4. Run the analysis:

   
   python qp_analysis.py
   

## Spreadsheet Report

The complete report, including the data, charts, and conclusions, is available in [qp_report.xlsx](script/qp_report.xlsx).

The Excel report contains: `Data` (raw results), `Charts` (visualizations), and `Conclusion` (summary of findings).

## Notes

* The `venv/` folder is excluded through `.gitignore` and should not be committed to the repository.

## AI Conversation

The AI-assisted work and troubleshooting process is documented in [AI_conversation.md](script/AI_conversation.md). The document is a reconstructed summary of the relevant interactions, not a verbatim transcript.

## Additional Task (Optional) – Appium Automation

The optional Appium automation task is available in the [automation](jm-test/automation/) folder.

The folder contains the Page Object Model implementation, test code, and a [README.md](jm-test/automation/README.md) describing the test approach, findings, and the limitations encountered when accessing the Minime window through Appium/WinAppDriver. The complete window-transition flow has not been reliably verified.
