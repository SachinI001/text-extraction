from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
import logging
logging.basicConfig(filename='output.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)

@app.route('/search/text', methods=['POST'])
def process():
    try:
        data = request.get_json()
        file_name = data.get("file_name", "")
        position = data.get("position", [])
        if file_name and len(position) == 4:
            if not file_name.endswith(".csv"):
                file_name = file_name + ".csv"
            output = ""
            x0_user = int(position[0])
            y0_user = int(position[1])
            x2_user = int(position[2])
            y2_user = int(position[3])

            if os.path.isfile(file_name):
                df = pd.read_csv(file_name)
                matched_data = []
                for idx, item in df.iterrows():
                    if item["x0"] > x0_user and x2_user > item["x0"] and item["y0"] > y0_user and item["y0"] < y2_user:
                        matched_data.append((item["Text"], item["y0"], item["x0"]))
                sorted_data = sorted(matched_data, key=lambda element: (element[1], element[2]))
                list_ = [x[0] for x in sorted_data]
                output = " ".join(list_)
            else:
                output = {"message": "invalid file name"}

        return jsonify({"text": output})
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "something went wrong"})


if __name__ == "__main__":
    app.run()