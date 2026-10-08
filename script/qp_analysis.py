import subprocess
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import xlsxwriter

qp_values = range(0, 52)   # full range 0–51
input_file = "foreman-cif.yuv"
resolution = "352x288"

results = []

for qp in qp_values:
    output_file = f"output_qp{qp}.264"
    cmd = [
        ".\\x264.exe",
        "--qp", str(qp),
        "--qpmin", "0",
        "--input-res", resolution,
        "-o", output_file,
        input_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    log = process.stdout + process.stderr

    print("RETURN CODE:", process.returncode)
    print("X264 OUTPUT:")
    print(log)
    
    fps_val, bitrate_val = None, None
    for line in log.splitlines():
        if "encoded" in line.lower():
            fps_match = re.search(r"([\d.]+)\s+fps", line)
            br_match = re.search(r"([\d.]+)\s+kb/s", line)
            if fps_match:
                fps_val = float(fps_match.group(1))
            if br_match:
                bitrate_val = float(br_match.group(1))
            
            # fallback: frames / seconds
            frames_match = re.search(r"encoded\s+(\d+)\s+frames\s+in\s+([\d\.]+)s", line)
            if frames_match and not fps_val:
                frames = int(frames_match.group(1))
                seconds = float(frames_match.group(2))
                if seconds > 0:
                    fps_val = frames / seconds
    
    # File size in KB 
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        size_kb = os.path.getsize(output_file) / 1024
    else:
        size_kb = None
    
    results.append({
        "QP": qp,
        "FileSize_KB": round(size_kb, 2) if size_kb else None,
        "FPS": round(fps_val, 2) if fps_val else None,
        "Bitrate": round(bitrate_val, 2) if bitrate_val else None
    })

# Save results to CSV
with open("qp_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["QP", "FileSize_KB", "FPS", "Bitrate"])
    writer.writeheader()
    writer.writerows(results)

print("Results saved to qp_results.csv")

# Load CSV
df = pd.read_csv("qp_results.csv")

# Chart 1: QP vs File Size
plt.figure(figsize=(8,5))
plt.plot(df["QP"], df["FileSize_KB"], marker="o", color="blue")
plt.title("QP vs File Size")
plt.xlabel("QP value")
plt.ylabel("File Size (KB)")
plt.grid(True)
plt.savefig("qp_vs_filesize.png", bbox_inches="tight")
plt.close()

# Chart 2: QP vs FPS
plt.figure(figsize=(8,5))
plt.plot(df["QP"], df["FPS"], marker="o", color="green")
plt.title("QP vs FPS")
plt.xlabel("QP value")
plt.ylabel("Encoding Speed (FPS)")
plt.grid(True)
plt.savefig("qp_vs_fps.png", bbox_inches="tight")
plt.close()

# Excel report
with pd.ExcelWriter("qp_report.xlsx", engine="xlsxwriter") as writer:
    # Sheet 1 – Data
    df.to_excel(writer, sheet_name="Data", index=False)

    workbook  = writer.book
    worksheet = writer.sheets["Data"]

    # Chart 1: QP vs File Size
    chart1 = workbook.add_chart({"type": "line"})
    chart1.add_series({
        "name": "File Size (KB)",
        "categories": ["Data", 1, 0, len(df), 0],
        "values":     ["Data", 1, 1, len(df), 1],
    })
    chart1.set_title({"name": "QP vs File Size"})
    worksheet.insert_chart("F2", chart1)

    # Chart 2: QP vs FPS
    chart2 = workbook.add_chart({"type": "line"})
    chart2.add_series({
        "name": "FPS",
        "categories": ["Data", 1, 0, len(df), 0],
        "values":     ["Data", 1, 2, len(df), 2],
    })
    chart2.set_title({"name": "QP vs FPS"})
    worksheet.insert_chart("F20", chart2)

    # Chart 3: QP vs Bitrate
    chart3 = workbook.add_chart({"type": "line"})
    chart3.add_series({
        "name": "Bitrate (kb/s)",
        "categories": ["Data", 1, 0, len(df), 0],
        "values":     ["Data", 1, 3, len(df), 3],
    })
    chart3.set_title({"name": "QP vs Bitrate"})
    worksheet.insert_chart("F38", chart3)

