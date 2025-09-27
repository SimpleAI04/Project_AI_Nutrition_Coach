from google import genai
import os
from dotenv import load_dotenv
import re
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import tempfile

load_dotenv()

client = genai.Client(api_key=os.getenv(key="GOOGLE_API_KEY"))

app = Flask(import_name=__name__)


def format_response(response_text: str) -> str:
    response_text = re.sub(
        pattern=r"\*\*(.*?)\*\*", repl=r"<strong>\1</strong>", string=response_text
    )

    response_text = re.sub(
        pattern=r"(?m)^\s*[\*\-]\s+(.*)", repl=r"<li>\1</li>", string=response_text
    )

    response_text = re.sub(
        pattern=r"(<li>.*?</li>\s*)+",
        repl=lambda match: f"<ul>{match.group(0)}</ul>",
        string=response_text,
        flags=re.DOTALL,
    )

    response_text = re.sub(pattern=r"\s*:\s*", repl=": ", string=response_text)

    response_text = re.sub(
        pattern=r"(?m)^(\d+\.)", repl=r"<br><strong>\1</strong>", string=response_text
    )

    response_text = response_text.replace("\n", "<br>")

    return response_text


def generate_model_response(uploaded_file, user_query, assistant_prompt) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            uploaded_file.save(tmp.name)
            tmp_path = tmp.name

        my_file = client.files.upload(file=tmp_path)

        raw_response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=[
                my_file,
                assistant_prompt + "\n\n" + user_query,
            ],
        )

        os.remove(path=tmp_path)

        return format_response(response_text=raw_response.text)

    except Exception as e:
        print(f"Error in generating response: {e}")
        return "<p>An error occurred while generating the response.</p>"


@app.route(rule="/", methods=["GET", "POST"])
def index() -> Response | str:
    if request.method == "POST":
        user_query = request.form.get(key="user_query")
        uploaded_file = request.files.get(key="file")
        if uploaded_file:
            assistant_prompt = """
            You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment using the following format:
            1. **Identification**: List each identified food item clearly, one per line.
            2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points with the following structure:
            - **[Food Item]**: [Portion Size], [Number of Calories] calories
            Example:
            *   **Salmon**: 6 ounces, 210 calories
            *   **Asparagus**: 3 spears, 25 calories
            3. **Total Calories**: Provide the total number of calories for all food items.
            Example:
            Total Calories: [Number of Calories]
            4. **Nutrient Breakdown**: Include a breakdown of key nutrients such as **Protein**, **Carbohydrates**, **Fats**, **Vitamins**, and **Minerals**. Use bullet points, and for each nutrient provide details about the contribution of each food item.
            Example:
            *   **Protein**: Salmon (35g), Asparagus (3g), Tomatoes (1g) = [Total Protein]
            5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.
            6. **Disclaimer**: Include the following exact text as a disclaimer:
            The nutritional information and calorie estimates provided are approximate and are based on general food data. 
            Actual values may vary depending on factors such as portion size, specific ingredients, preparation methods, and individual variations. 
            For precise dietary advice or medical guidance, consult a qualified nutritionist or healthcare provider.
            Format your response exactly like the template above to ensure consistency.
            """

            response = generate_model_response(
                uploaded_file=uploaded_file,
                user_query=user_query,
                assistant_prompt=assistant_prompt,
            )

            return render_template(
                template_name_or_list="index.html",
                user_query=user_query,
                response=response,
            )
        else:
            flash(message="Please upload an image file.", category="danger")
            return redirect(location=url_for(endpoint="index"))
    return render_template(template_name_or_list="index.html")


if __name__ == "__main__":
    app.run(debug=True)
