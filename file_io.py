# file_io.py
def write_result_to_file(features, result):
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write("输入特征：" + ",".join(features) + "\n")
        f.write("推理结果：" + result + "\n\n")
