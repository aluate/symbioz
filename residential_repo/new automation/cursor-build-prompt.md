You are building an automation following our standard method.
Use this repository structure:

/app
/backend
api.py
models.py
db.py
validators.py
/frontend
index.html
script.js
/config
/docs
/tests

Rules:

* Build data model first using data-schema.md
* Then design FastAPI routes
* Then create frontend form
* Then wire everything together
* Use clean functions, no hardcoding
* Generate sample data and test files
* Produce a working build that runs locally or on a phone browser

Primary Requirements:

* Create a simple intake form with fields: name, address, email, phone
* Validate inputs
* Store data persistently
* Display confirmation message
* Use responsive layout for phones

Reference Files:

* project-overview.md
* data-schema.md

First Task:

* Generate file structure and empty files.



At the end of your work, do ALL of the following:



1\. Create or update `README.md` inside the project folder (for this automation) with:

&nbsp;  - A one-paragraph description of what the app/automation does.

&nbsp;  - Exact run instructions (e.g., uvicorn command, ports, etc.).

&nbsp;  - How to access it from a phone on the same network (using local IP + port).

&nbsp;  - Where data is stored on disk (paths to JSON/CSV/XLSX or other stores).

&nbsp;  - Any required dependencies or pip installs.



2\. Update the relevant doc in `docs/` (for this automation) with a short \*\*Current Status\*\* section:

&nbsp;  - What’s implemented

&nbsp;  - What’s NOT implemented yet

&nbsp;  - Obvious next steps



3\. In your final message back to me, print a clear \*\*Summary\*\* section that includes:

&nbsp;  - New or modified files (by path)

&nbsp;  - How to start the app

&nbsp;  - Where to open it in a browser

&nbsp;  - Where the data is being saved



