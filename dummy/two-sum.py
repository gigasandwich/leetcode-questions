import requests

def get_leetcode_problem(slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/",
        "User-Agent": "Mozilla/5.0"
    }
    
    query = {
        "query": """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            content
          }
        }
        """,
        "variables": {"titleSlug": slug}
    }

    response = requests.post(url, json=query, headers=headers)

    if response.status_code == 200:
        data = response.json()
        question = data["data"]["question"]
        return question["title"], question["content"]
    else:
        return None, None

title, content = get_leetcode_problem("two-sum")

if title:
    print(f"Title: {title}\n")
    print(f"Content:\n{content}")
else:
    print("Failed to fetch problem data.")
