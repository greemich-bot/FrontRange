
# Most code is based on and adapted from the CS 340 starter code including:
1. app routes and app.py
    adapted to fit our needs 
2. tempates 
    adapted to improve UX
3. style.css
    copied
4. Stored Procedures to handle CRUD
    adapted to fit our needs

# Citation for use of AI Tools:

# Date: 3/01/2026
3      # Prompts used to create a button that opens a form to edit skiers
4      # Help me add a button that shows a form to edit a skier row.
       # Then provided my route and skiers.j2
       # Date 3/9/2026
       # Provided the form to gemini and asked me to declutter. Then asked it to isolate each piece of the form.
7      # AI Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 

#

# Date: 2/15/2026
3      # Prompts used to add functionality to SkiersRentals Update button
4      # Help me add a button that updates skiers rentals by building a route.
       # Returned a route with all of the PL embedded, and the code for another j2 page where the information can be edited. 
       # This route was adjusted after we learned about SPs but we kept the queries because they were functional.
7      # AI Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 

# Date: 3/9/2026
3      # Prompts used to add logic for to Lifts Update button
4      # provided sp and route, asked gemini to create a toggle switch. 
       # It produced a checkbox system that wasnt very user friendly, so I prompted it to make a toggle that changes color when selected.
       # Logic was copied and then adapted for changing the color of the actual status. Also applied to trials. 

7      # AI Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 

# Date: 3/10/2026
3      # Prompts used to add logic for to passes create button
4      # provided gemini my current stored procedure and asked it to calculate my expiration date based on pass type. First iteration gave me an trigger and an 
       #error, I then provided my route and it suggested updating my stored procedure instead.
       # 
7      # I Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 

# Date: 3/13/26 
       # Prompts used to add logic for to update rentals button
4      # I provided my route and asked for an update form that only appears after the button is pressed and is automatically filled with the row ID 
       # Gemini provided a route update to my get method which I used and an if statement containing a form that I copied directly.
7      # I Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 

# Date: 3/13/26 
       # Prompts used to limit input on skiers button
       # Provided gemini my varchar limit and my current route, and asked it to show me how to slice an input that is too long. Implemented to safeguard invalid inputs on multiple routes. 
7      # I Source URL: https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb
Links to an external site. 


