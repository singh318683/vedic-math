from flask import Flask, jsonify, send_from_directory
import os, random

app = Flask(__name__, static_folder="../public", static_url_path="")

SUTRAS = [
    {
        "id": 0,
        "name": "Ekadhikena Purvena",
        "sanskrit": "एकाधिकेन पूर्वेण",
        "meaning": "By one more than the previous",
        "color": "#EEEDFE", "textColor": "#3C3489", "dot": "#7F77DD",
        "desc": "Square numbers ending in 5, or multiply numbers whose tens digits are equal and units digits sum to 10.",
        "steps": [
            "Take the tens digit of the number (ignore the 5).",
            "Multiply it by (itself + 1).",
            "Append 25 at the end — that's your answer."
        ],
        "examples": [
            {"q": "35²", "steps": ["Tens digit: 3", "3 × (3+1) = 3 × 4 = 12", "Append 25 → 1225"]},
            {"q": "75²", "steps": ["Tens digit: 7", "7 × 8 = 56", "Append 25 → 5625"]}
        ],
        "questions": [
            {"q": "35²", "a": 1225, "o": [1025, 1225, 1325, 1125]},
            {"q": "45²", "a": 2025, "o": [2025, 2225, 1925, 2125]},
            {"q": "25²", "a": 625,  "o": [525, 725, 625, 825]},
            {"q": "65²", "a": 4225, "o": [4025, 4225, 4425, 4625]},
            {"q": "95²", "a": 9025, "o": [8925, 9025, 9125, 9225]},
            {"q": "15²", "a": 225,  "o": [125, 225, 325, 215]},
            {"q": "55²", "a": 3025, "o": [2925, 3025, 3125, 3015]},
            {"q": "85²", "a": 7225, "o": [7125, 7325, 7225, 7215]},
        ]
    },
    {
        "id": 1,
        "name": "Nikhilam",
        "sanskrit": "निखिलम्",
        "meaning": "All from 9, last from 10",
        "color": "#E1F5EE", "textColor": "#085041", "dot": "#1D9E75",
        "desc": "Subtract each digit from 9, and the last digit from 10. Perfect for subtracting from any power of 10.",
        "steps": [
            "Identify the power of 10 you're subtracting from (100, 1000, 10000…).",
            "For each digit of the number, subtract it from 9.",
            "For the last digit only, subtract from 10 instead."
        ],
        "examples": [
            {"q": "1000 − 764", "steps": ["Digits: 7, 6, 4", "9−7=2, 9−6=3, 10−4=6", "Answer: 236"]},
            {"q": "100 − 73",   "steps": ["Digits: 7, 3", "9−7=2, 10−3=7", "Answer: 27"]}
        ],
        "questions": [
            {"q": "1000 − 764",   "a": 236,  "o": [236, 246, 226, 256]},
            {"q": "1000 − 537",   "a": 463,  "o": [453, 463, 473, 443]},
            {"q": "100 − 73",     "a": 27,   "o": [17, 37, 27, 47]},
            {"q": "1000 − 291",   "a": 709,  "o": [799, 709, 719, 699]},
            {"q": "10000 − 3821", "a": 6179, "o": [6179, 6279, 6079, 6189]},
            {"q": "100 − 48",     "a": 52,   "o": [42, 52, 62, 58]},
            {"q": "1000 − 109",   "a": 891,  "o": [881, 901, 891, 911]},
            {"q": "10000 − 5672", "a": 4328, "o": [4228, 4428, 4338, 4328]},
        ]
    },
    {
        "id": 2,
        "name": "Urdhva Tiryak",
        "sanskrit": "ऊर्ध्व तिर्यक्",
        "meaning": "Vertically and crosswise",
        "color": "#FAEEDA", "textColor": "#633806", "dot": "#EF9F27",
        "desc": "The general multiplication sutra. Multiply any two 2-digit numbers using vertical and crosswise products.",
        "steps": [
            "Write AB × CD. Right column: B×D (write units digit, carry the tens).",
            "Cross multiply: A×D + B×C, add any carry (write units, carry tens).",
            "Left column: A×C plus any carry.",
            "Read the three results left to right."
        ],
        "examples": [
            {"q": "23 × 14", "steps": ["Right: 3×4=12 → write 2, carry 1", "Cross: 2×4+3×1+1=12 → write 2, carry 1", "Left: 2×1+1=3", "Answer: 322"]},
            {"q": "32 × 21", "steps": ["Right: 2×1=2", "Cross: 3×1+2×2=7", "Left: 3×2=6", "Answer: 672"]}
        ],
        "questions": [
            {"q": "23 × 14", "a": 322,  "o": [322, 332, 312, 342]},
            {"q": "32 × 21", "a": 672,  "o": [652, 682, 672, 662]},
            {"q": "13 × 12", "a": 156,  "o": [146, 166, 156, 136]},
            {"q": "41 × 32", "a": 1312, "o": [1302, 1322, 1312, 1332]},
            {"q": "22 × 31", "a": 682,  "o": [672, 692, 682, 662]},
            {"q": "24 × 13", "a": 312,  "o": [302, 312, 322, 332]},
            {"q": "33 × 11", "a": 363,  "o": [353, 363, 373, 343]},
            {"q": "42 × 21", "a": 882,  "o": [872, 892, 882, 862]},
        ]
    },
    {
        "id": 3,
        "name": "Anurupyena",
        "sanskrit": "अनुरूप्येण",
        "meaning": "Proportionality",
        "color": "#FAECE7", "textColor": "#712B13", "dot": "#D85A30",
        "desc": "Scale to a round number, compute, then adjust. Makes ×99, ×101, ×9, ×11 trivially fast.",
        "steps": [
            "Round the multiplier to the nearest 10 or 100 (e.g. 99 → 100, 101 → 100).",
            "Multiply by that round number.",
            "Subtract (if rounded up) or add (if rounded down) the difference times the other number."
        ],
        "examples": [
            {"q": "47 × 99",  "steps": ["47 × 100 = 4700", "Subtract 47 × 1 = 47", "Answer: 4653"]},
            {"q": "25 × 101", "steps": ["25 × 100 = 2500", "Add 25 × 1 = 25", "Answer: 2525"]}
        ],
        "questions": [
            {"q": "47 × 99",  "a": 4653, "o": [4653, 4753, 4553, 4643]},
            {"q": "36 × 99",  "a": 3564, "o": [3464, 3664, 3564, 3574]},
            {"q": "25 × 101", "a": 2525, "o": [2625, 2425, 2515, 2525]},
            {"q": "53 × 99",  "a": 5247, "o": [5247, 5347, 5147, 5257]},
            {"q": "18 × 101", "a": 1818, "o": [1818, 1918, 1718, 1828]},
            {"q": "62 × 99",  "a": 6138, "o": [6038, 6238, 6138, 6148]},
            {"q": "44 × 101", "a": 4444, "o": [4344, 4544, 4444, 4434]},
            {"q": "77 × 99",  "a": 7623, "o": [7523, 7723, 7613, 7623]},
        ]
    },
    {
        "id": 4,
        "name": "Vilokanam",
        "sanskrit": "विलोकनम्",
        "meaning": "By mere observation",
        "color": "#EEEDFE", "textColor": "#3C3489", "dot": "#534AB7",
        "desc": "Spot algebraic patterns like (a+b)(a−b) = a²−b² instantly. Solve by pattern recognition, not calculation.",
        "steps": [
            "Check if both numbers are equidistant from a round number.",
            "That round number is 'a'. The equal distance is 'b'.",
            "Answer = a² − b². Both values are easy to compute mentally."
        ],
        "examples": [
            {"q": "63 × 57", "steps": ["Both are 3 away from 60", "a=60, b=3", "60²−3² = 3600−9 = 3591"]},
            {"q": "84 × 76", "steps": ["Both are 4 away from 80", "a=80, b=4", "6400−16 = 6384"]}
        ],
        "questions": [
            {"q": "63 × 57", "a": 3591, "o": [3591, 3691, 3491, 3581]},
            {"q": "84 × 76", "a": 6384, "o": [6284, 6484, 6384, 6374]},
            {"q": "45 × 35", "a": 1575, "o": [1475, 1675, 1565, 1575]},
            {"q": "93 × 87", "a": 8091, "o": [8091, 8191, 7991, 8081]},
            {"q": "72 × 68", "a": 4896, "o": [4796, 4996, 4886, 4896]},
            {"q": "51 × 49", "a": 2499, "o": [2399, 2599, 2499, 2489]},
            {"q": "102 × 98","a": 9996, "o": [9896, 10096, 9986, 9996]},
            {"q": "65 × 55", "a": 3575, "o": [3475, 3675, 3565, 3575]},
        ]
    },
    {
        "id": 5,
        "name": "Sankalana Vyavakalanabhyam",
        "sanskrit": "सङ्कलन व्यवकलनाभ्यां",
        "meaning": "By addition and subtraction",
        "color": "#E1F5EE", "textColor": "#085041", "dot": "#1D9E75",
        "desc": "Solve simultaneous equations by adding or subtracting them to eliminate one variable instantly.",
        "steps": [
            "Add both equations together — one variable cancels out.",
            "Or subtract one from the other — the other variable cancels.",
            "Solve the resulting simple single-variable equation.",
            "Back-substitute to find the second variable."
        ],
        "examples": [
            {"q": "x+y=7, x−y=3", "steps": ["Add: 2x=10 → x=5", "Subtract: 2y=4 → y=2", "Answer: x=5, y=2"]},
            {"q": "x+y=9, x−y=1", "steps": ["Add: 2x=10 → x=5", "y = 9−5 = 4", "Answer: x=5, y=4"]}
        ],
        "questions": [
            {"q": "x+y=10, x−y=4 → x=?", "a": 7,  "o": [5, 6, 7, 8]},
            {"q": "x+y=9,  x−y=1 → x=?", "a": 5,  "o": [4, 5, 6, 7]},
            {"q": "x+y=12, x−y=2 → x=?", "a": 7,  "o": [5, 6, 7, 8]},
            {"q": "x+y=8,  x−y=2 → y=?", "a": 3,  "o": [2, 3, 4, 5]},
            {"q": "x+y=15, x−y=5 → y=?", "a": 5,  "o": [4, 5, 6, 7]},
            {"q": "x+y=20, x−y=4 → x=?", "a": 12, "o": [10, 11, 12, 13]},
            {"q": "x+y=14, x−y=6 → y=?", "a": 4,  "o": [3, 4, 5, 6]},
            {"q": "x+y=18, x−y=2 → x=?", "a": 10, "o": [8, 9, 10, 11]},
        ]
    },
    {
        "id": 6,
        "name": "Anurupye Shunyam",
        "sanskrit": "आनुरूप्ये शून्यम्",
        "meaning": "If proportionate, then zero",
        "color": "#FAEEDA", "textColor": "#633806", "dot": "#EF9F27",
        "desc": "When coefficients of one variable are proportional across equations, that variable can be zeroed out to find the other.",
        "steps": [
            "Write both equations side by side.",
            "Check if one variable's coefficients share a common ratio.",
            "If yes, set that variable to zero and solve for the other.",
            "Verify by substituting back."
        ],
        "examples": [
            {"q": "2x+3y=6 & 4x+6y=12", "steps": ["Notice 4/2=2, 6/3=2, 12/6=2 — all proportional", "Equations are identical scaled — infinite solutions", "Set x=0: 3y=6 → y=2"]},
            {"q": "3x=15", "steps": ["Isolate x", "x = 15/3", "x = 5"]}
        ],
        "questions": [
            {"q": "If 2x = 6, find x",   "a": 3, "o": [2, 3, 4, 6]},
            {"q": "If 3y = 12, find y",  "a": 4, "o": [3, 4, 6, 9]},
            {"q": "If 5x = 25, find x",  "a": 5, "o": [4, 5, 6, 7]},
            {"q": "If 4y = 20, find y",  "a": 5, "o": [4, 5, 6, 8]},
            {"q": "If 6x = 18, find x",  "a": 3, "o": [2, 3, 4, 6]},
            {"q": "If 7y = 49, find y",  "a": 7, "o": [6, 7, 8, 9]},
            {"q": "If 9x = 81, find x",  "a": 9, "o": [7, 8, 9, 10]},
            {"q": "If 8y = 64, find y",  "a": 8, "o": [6, 7, 8, 9]},
        ]
    },
    {
        "id": 7,
        "name": "Yavadunam",
        "sanskrit": "यावदूनम्",
        "meaning": "By the deficiency",
        "color": "#FAECE7", "textColor": "#712B13", "dot": "#D85A30",
        "desc": "Square numbers near a base (10, 100, 1000) by computing the deficiency and applying a simple two-part formula.",
        "steps": [
            "Find the deficiency: how far is the number below the base? (e.g. 98 is 2 below 100)",
            "Left part: subtract the deficiency from the number (98−2=96).",
            "Right part: square the deficiency (2²=04, use as many digits as zeros in base).",
            "Concatenate: 9604."
        ],
        "examples": [
            {"q": "98²", "steps": ["Deficiency: 100−98=2", "Left: 98−2=96", "Right: 2²=04", "Answer: 9604"]},
            {"q": "97²", "steps": ["Deficiency: 100−97=3", "Left: 97−3=94", "Right: 3²=09", "Answer: 9409"]}
        ],
        "questions": [
            {"q": "98²",  "a": 9604,  "o": [9604, 9504, 9704, 9614]},
            {"q": "97²",  "a": 9409,  "o": [9309, 9509, 9409, 9419]},
            {"q": "96²",  "a": 9216,  "o": [9116, 9316, 9216, 9206]},
            {"q": "99²",  "a": 9801,  "o": [9701, 9901, 9801, 9811]},
            {"q": "995²", "a": 990025,"o": [990025, 989025, 991025, 990035]},
            {"q": "94²",  "a": 8836,  "o": [8736, 8936, 8836, 8826]},
            {"q": "93²",  "a": 8649,  "o": [8549, 8749, 8649, 8639]},
            {"q": "995²", "a": 990025,"o": [990025, 990125, 989925, 990015]},
        ]
    },
]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/sutras")
def get_sutras():
    safe = []
    for s in SUTRAS:
        safe.append({k: v for k, v in s.items() if k != "questions"})
    return jsonify(safe)


@app.route("/api/sutras/<int:sutra_id>")
def get_sutra(sutra_id):
    for s in SUTRAS:
        if s["id"] == sutra_id:
            return jsonify(s)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/quiz/<int:sutra_id>")
def get_quiz(sutra_id):
    for s in SUTRAS:
        if s["id"] == sutra_id:
            qs = random.sample(s["questions"], min(5, len(s["questions"])))
            for q in qs:
                q["o"] = random.sample(q["o"], len(q["o"]))
            return jsonify({"sutra": s["name"], "questions": qs})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/quiz/mixed")
def get_mixed_quiz():
    pool = []
    for s in SUTRAS:
        for q in s["questions"]:
            pool.append({**q, "sutraName": s["name"], "sutraId": s["id"]})
    selected = random.sample(pool, min(10, len(pool)))
    for q in selected:
        q["o"] = random.sample(q["o"], len(q["o"]))
    return jsonify(selected)


if __name__ == "__main__":
    app.run(debug=True)
