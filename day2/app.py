from flask import Flask, request, render_template_string
from fallback import recommend

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>AI Travel Recommendation App</title>
<h1>AI Travel Recommendation App</h1>
<form method="POST">
  <input type="text" name="query" placeholder="Describe your trip..." value="{{ query or '' }}" style="width:300px;">
  <button type="submit">Search</button>
</form>

{% if message %}
  <p><em>{{ message }}</em></p>
{% endif %}

{% if results %}
  <ul>
  {% for dest in results %}
    <li>
      <strong>{{ dest.name }}</strong> ({{ dest.country }}) — {{ dest.category }}<br>
      {{ dest.description }}
    </li>
  {% endfor %}
  </ul>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    results = []
    message = None

    if request.method == "POST":
        query = request.form.get("query", "")
        results, used_fallback, message = recommend(query)

    return render_template_string(PAGE, query=query, results=results, message=message)


if __name__ == "__main__":
    app.run(debug=True)