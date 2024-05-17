import re
import mysql.connector
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__, static_url_path='')

# Connect to MySQL DB
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='pll_algorithms', buffered=True)
cursor = conn.cursor()


# Function using regular expressions to count moves in algorithm
def count_moves(algorithm):
    pattern = re.compile(r"([A-Za-z]+)(\d*)")
    matches = pattern.findall(algorithm)
    move_count = 0
    for move, count in matches:
        count = int(count) if count else 1
        move_count += count
    return move_count


# Search PLL
@app.route('/searchPLL', methods=['GET'])
def search_pll():
    search_query = request.args.get('query')
    success_message = request.args.get('success')
    if search_query:
        cursor.execute("SELECT * FROM `pll_algorithms` WHERE name LIKE %s", ['%' + search_query + '%'])
        results = cursor.fetchall()
        if not results:
            return f"Sorry, unable to find results for '{search_query}'"
        return render_template('pll_results.html', results=results, success_message=success_message)
    else:
        return render_template('pll_results.html', success_message=success_message)


# Update PLL Alg
@app.route('/updatePLL', methods=['POST'])
def update_pll():
    pll_name = request.form['pll_name']
    new_algorithm = request.form['new_algorithm']

    # Count the number of moves in updated algorithm
    num_moves = count_moves(new_algorithm)

    cursor.execute("UPDATE `pll_algorithms` SET algorithm = %s, moves = %s WHERE name = %s",
                   [new_algorithm, num_moves, pll_name])
    conn.commit()
    updated_rows = cursor.rowcount
    if updated_rows == 0:
        return f"Failed to update PLL '{pll_name}'"
    else:
        # Redirect to the search page after successful update
        success_message = f"Successfully updated {pll_name}!"
        return redirect(url_for('search_pll', query=pll_name, success=success_message))


# Search and update form
@app.route('/')
def root():
    return render_template('pll_form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
