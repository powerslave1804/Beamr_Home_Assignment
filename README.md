# Beamr_Home_Assignment

## Task 2 – QP Analysis with x264

This script runs x264 encoding on the `foreman-cif.yuv` test video with different QP values and collects results (file size, FPS, bitrate).  
Results are saved in [qp_results.csv](script/qp_results.csv) and visualized in the following graphs:

### QP vs File Size
![QP vs File Size](script/qp_vs_filesize.png)

### QP vs FPS
![QP vs FPS](script/qp_vs_fps.png)

## Requirements
- Python 3.10+
- matplotlib
- pandas
- xlsxwriter

## How to run
1. Create virtual environment:
   
   python -m venv venv
   

2. Activate venv:
   
    venv\Scripts\activate
    

3. Install dependencies:
    
    pip install -r requirements.txt
    

4. Run analysis:
    
    python qp_analysis.py
  

## Spreadsheet Report
The complete report with charts and conclusions is available in [qp_report.xlsx](script/qp_report.xlsx).
The Excel report contains two sheets: Data (raw results), Charts (visualizations), and Conclusion (summary).

## Notes
- The `venv/` folder is excluded via `.gitignore` and should not be pushed to GitHub.  

## AI Conversation
The full conversation with Copilot is available in [AI_conversation.md](AI_conversation.md).
