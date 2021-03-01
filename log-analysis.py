import re

file_name = ["gat.log", "sage.log"]
with open("log-analysis.out", "w") as output:
    for file in file_name:
        with open(file) as f:
            data = f.read()
            param_number = re.findall(r"(?<=num. trained: )\d+", data)
            val_loss = re.findall(r"(?<=epoch \d{3} \| loss )[\d.]+", data)
            output.write(file + "\n")
            output.writelines(param_number + ["\n"])
            for i in val_loss:
                output.write(i + " ")
            output.write("\n")
