# AI-Assisted Workflow – x264 QP Analysis

**Note:** The following is a reconstructed transcript of the AI-assisted workflow used while developing and troubleshooting the x264 QP analysis and reporting script. It reflects the actual questions, technical issues, changes, and reasoning used during the assignment.

---

### Me:

I need to generate a report that shows how QP affects file size and encoding speed. The report should be in Excel and include charts and graphs. Can you help me create a Python script for that?

### AI:

Yes. You can extend your Python script to automatically collect the results from each x264 encoding run and generate a report.

The script can:

* Run x264 for the required QP values.
* Extract FPS and bitrate from the x264 console output.
* Calculate the encoded file size in KB.
* Store the results in a structured format.
* Export the results to CSV.
* Generate an Excel report with charts showing the relationship between QP, file size, and encoding speed.

Since the assignment requires QP values from **0 to 51**, I recommend running all 52 values rather than only a small sample.

---

### Me:

How should the data in the report be structured?

### AI:

Keep the data numeric and easy to analyze. A suitable structure is:

|  QP | FileSize (KB) | FPS | Bitrate (kb/s) |
| --: | ------------: | --: | -------------: |
|   0 |           ... | ... |            ... |
|   1 |           ... | ... |            ... |
|   2 |           ... | ... |            ... |
| ... |           ... | ... |            ... |
|  51 |           ... | ... |            ... |

The values can be rounded to two decimal places for readability.

The important part is that the report uses the actual measurements produced by x264.

---

### Me:

Can you provide the Python code that automatically generates this report?

### AI:

Yes. The existing x264 execution loop can be extended so that it:

1. Runs x264 for every QP from 0 to 51.
2. Creates a separate `.264` output file for each QP.
3. Parses the x264 console output to extract FPS and bitrate.
4. Calculates the output file size in KB.
5. Stores the results in a list.
6. Writes the results to a CSV file.
7. Creates an Excel workbook using `xlsxwriter`.
8. Adds charts for file size, FPS, and bitrate.

For parsing the x264 output, a simple regular expression can be used:

```python id="18452"
fps_match = re.search(r"([\d.]+)\s+fps", line)
br_match = re.search(r"([\d.]+)\s+kb/s", line)
```

It is also useful to check explicitly whether the parsed values are `None`.

---

### Me:

I changed the script to run all QP values from 0 to 51, but QP 0–4 are returning empty or zero values. QP 5 and above work correctly. Could this be a problem with my Python code?

### AI:

It may not be a parsing problem. The first thing to check is the x264 process return code and the actual x264 console output.

Add temporary debugging output after `subprocess.run()`:

```python id="52017"
print("RETURN CODE:", process.returncode)
print("X264 OUTPUT:")
print(process.stdout)
print(process.stderr)
```

This will show whether x264 actually completed the encoding.

---

### Me:

I checked the output for QP 0 and received:

```text id="63194"
RETURN CODE: 255
X264 OUTPUT:
yuv [info]: 352x288p 0:0 @ 25/1 fps (cfr)
x264 [error]: Your qp is lower than minimum allowed QP. Set lower --qpmin or increase your QP
x264 [error]: x264_encoder_open failed
```

What does this mean?

### AI:

This confirms that the Python parser is not the problem.

x264 is rejecting QP values below its configured minimum QP. The default minimum QP is higher than the values you are trying to use.

Since the assignment explicitly requires QP values from 0 to 51, the x264 command should explicitly allow QP 0 by setting `--qpmin 0`.

Add this argument to the command:

```python id="30786"
"--qpmin", "0",
```

So the command should contain:

```python id="41529"
cmd = [
    ".\\x264.exe",
    "--qp", str(qp),
    "--qpmin", "0",
    "--input-res", resolution,
    "-o", output_file,
    input_file
]
```

This allows the script to execute the complete required QP range.

---

### Me:

I tested QP 0 again after adding `--qpmin 0`. It now works:

```text id="89241"
RETURN CODE: 0

encoded 300 frames, 51.14 fps, 10848.26 kb/s
```

So QP 0 is now working correctly?

### AI:

Yes. A return code of `0` indicates that x264 completed successfully.

The output also contains valid FPS and bitrate values, so the parser can extract the required metrics.

You can now run the complete QP 0–51 analysis again and generate the report from the new results.

It is also a good idea to remove the previous failed output files and old report files before rerunning the full test, so that the new report contains only results from the successful runs.

---

### Me:

I ran the complete QP 0–51 analysis. The beginning of the results looks like this:

| QP | FileSize (KB) |   FPS | Bitrate (kb/s) |
| -: | ------------: | ----: | -------------: |
|  0 |      15891.00 | 44.38 |       10848.26 |
|  1 |      17297.21 | 30.58 |       11808.23 |
|  2 |      16336.60 | 27.04 |       11152.45 |
|  3 |      15284.05 | 28.86 |       10433.91 |
|  4 |      14316.73 | 32.77 |        9773.55 |
|  5 |      13242.92 | 33.11 |        9040.50 |
|  6 |      12108.71 | 34.05 |        8266.21 |
|  7 |      11026.19 | 34.51 |        7527.22 |
|  8 |       9841.01 | 34.75 |        6718.13 |
|  9 |       8761.74 | 35.25 |        5981.35 |
| 10 |       7723.51 | 29.51 |        5272.59 |

Does the data look reasonable?

### AI:

Yes. The results show a clear overall relationship between QP and the encoded output size.

As QP increases, the file size and bitrate generally decrease substantially.

The FPS values show more variation. They do not increase strictly with every individual QP value, but the results can still be analyzed in terms of the overall trend.

For example, the FPS values for the first QPs are:

* QP 0: 44.38 FPS
* QP 1: 30.58 FPS
* QP 2: 27.04 FPS
* QP 5: 33.11 FPS
* QP 8: 34.75 FPS
* QP 9: 35.25 FPS
* QP 10: 29.51 FPS

This variation is important to preserve in the report rather than modifying or smoothing the measurements.

---

### Me:

Should I use all 52 QP values in the charts?

### AI:

Yes. Since the assignment requires testing QP values from 0 to 51, the charts should use the complete dataset.

I recommend visualizing:

* QP vs. File Size (KB)
* QP vs. Encoding Speed (FPS)
* QP vs. Bitrate (kb/s)

Use QP as the X-axis and the corresponding measurement as the Y-axis.

The charts should display the actual measured values, including any variations between individual QP values.

---

### Me:

The assignment says the report should ideally be generated automatically as soon as the results become available. Does generating the report automatically from the collected results satisfy this requirement?

### AI:

Yes, it addresses the automation aspect of the requirement because the report is generated programmatically from the x264 results rather than being manually created.

If you want to make the workflow even closer to the wording of the assignment, the results could also be written incrementally after each encoding run. However, this is an enhancement rather than a requirement if the complete report is automatically generated from the collected results after the analysis finishes.

The important part is that the report is based on the actual output of the script and does not require manually entering the measurements.

---

### Me:

The assignment also asks me to share the AI conversation. Is this type of transcript sufficient?

### AI:

Yes. The conversation demonstrates how AI was used as part of the development workflow.

It shows the process of:

* planning the reporting approach,
* structuring the collected data,
* creating the reporting logic,
* troubleshooting the x264 QP limitation,
* identifying the `--qpmin 0` configuration,
* validating the successful QP 0 run,
* and interpreting the resulting measurements.

The final report should contain the actual results produced by the script.
