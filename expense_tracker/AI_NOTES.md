# AI Usage Notes

## AI Tools Used

I used calude and ChatGPT during the development of this project as a learning and productivity tool. It helped me understand some Django REST Framework concepts, review my implementation, improve the project documentation, and suggest better ways to structure parts of the code.

---

## What AI Helped With

- Suggested a project structure for the Django REST API.
- Helped explain how to implement serializers, views, and URL routing.
- Reviewed parts of my code and suggested improvements.
- Helped improve the README and API documentation.
- Answered questions whenever I got stuck during development.

---

## What I Implemented Myself

Although I used AI for guidance, I completed the implementation myself by:

- Setting up the Django project and app.
- Creating the `Expense` model.
- Writing and configuring serializers.
- Implementing the API views and URL routing.
- Running migrations and configuring the SQLite database.
- Writing and running the test cases.
- Fixing errors that came up during development.
- Creating the GitHub repository and preparing the project for submission.

---

## How I Verified the Code

I didn't rely on AI-generated code without checking it.

Before submitting, I:

- Ran all the tests using:

```bash
python manage.py test expenses
```

- Verified that all tests passed successfully.
- Tested every API endpoint manually.
- Checked that validation worked correctly for invalid requests.
- Followed the README setup steps from a clean project to ensure they worked as expected.

---

## Design Choices

I chose **Django REST Framework** because I was already familiar with Django and it provides a clean way to build REST APIs.

I used **SQLite** since it is lightweight, requires no additional setup, and fully meets the assignment requirements.

My main focus was to build a simple, clean, and maintainable solution that satisfies all the required features instead of adding unnecessary complexity.

---

## Final Note

AI was used as a learning assistant throughout this assignment. I reviewed the suggestions, understood the implementation, made changes where needed, and tested the final application myself before submission.