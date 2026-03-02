# ########################################
# ########## SETUP

from flask import Flask, render_template, request, redirect
import database.db_connector as db

PORT = 8083

app = Flask(__name__)

# ########################################
# ########## ROUTE HANDLERS

# READ ROUTES
@app.route("/", methods=["GET"])
def home():
    try:
        return render_template("home.j2")

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
# ---------------------------------------------------------------------------------------------------------
# Skiers CRUD routes
# ---------------------------------------------------------------------------------------------------------
@app.route("/skiers", methods=["GET"])
def skiers():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT * FROM Skiers;"
        
        skiers = db.query(dbConnection, query1).fetchall()

        # Render the skiers.j2 file, and also send the renderer
        # a couple objects that contains skiers information
        return render_template(
            "skiers.j2", skiers=skiers      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# create skier

@app.route("/skiers/create", methods=["POST"])
def create_skiers():
    try:
        dbConnection = db.connectDB() # this opens skiers db connection
        cursor = dbConnection.cursor()

        # Get form data. will do data cleansing try/catch blocks later since we don't have int input for the following attributes:
        Name = request.form["create_skier_name"]
        Address = request.form["create_skier_address"]
        Phone = request.form["create_skier_phone"]
        Email = request.form["create_skier_email"]
        Ability = request.form["create_skier_ability"]

        # call create skier sp method. use parameterized queries to prevent injuection attacks like drop table or db.
        query1 = "CALL sp_CreateSkier(%s, %s, %s, %s, %s, @s_new_id);"
        cursor.execute(query1, (Name, Address, Phone, Email, Ability))

        # store the generated skier id for the last inserted row. this will be the pk for the new inserted row
        new_id = cursor.fetchone()[0] # id is index 0 of the row
        cursor.nextset() # Move the the next result. Assuming this to move to the next row?
        dbConnection.commit() #commit transaction
        print(f"""Create skiers. 
        ID: {new_id} 
        Name: {Name} 
        Address {Address} 
        Phone {Phone} 
        Email {Email} 
        Ability {Ability}
        """)
        # Redirect to the updated webpage by add the path /skiers
        return redirect("/skiers")
    except Exception as e:
        print(f"Error executing quereis: {e}")
        return ("An error occurred whle executing this database queries. ", 500,) # ProgError, OpsError, DBError? can be more specific
    finally:
        # Close the DB Conneciton, if it exists:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# update skier

@app.route("/skiers/update", methods=["POST"])
def update_skiers():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        skier_id = request.form["update_skier_id"]
        Name = request.form["update_skier_name"]
        Address = request.form["update_skier_address"]
        Phone = request.form["update_skier_phone"]
        Email = request.form["update_skier_email"]
        Ability = request.form["update_skier_ability"]

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateSkier(%s, %s, %s, %s, %s, %s);"
        cursor.execute(query1, (skier_id, Name, Address, Phone, Email, Ability))

        dbConnection.commit()  # commit the transaction

        print(f"""UPDATE skiers. 
        ID: {skier_id} 
        Name: {Name} 
        Address {Address} 
        Phone {Phone} 
        Email {Email} 
        Ability {Ability}
        """)

        # Redirect the user to the updated webpage
        return redirect("/skiers")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# delete skier
@app.route("/skiers/delete", methods=["POST"])
def delete_skiers():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        skier_id = request.form["delete_skier_id"]
        

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteSkier(%s);"
        cursor.execute(query1, (skier_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE skiers. ID: {skier_id}")

        # Redirect the user to the updated webpage
        return redirect("/skiers")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# -------------------------------------------------------------------------------------------------
# Lifts RU
# only need read and update
# -------------------------------------------------------------------------------------------------



@app.route("/lifts", methods=["GET"])
def lifts():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT * FROM Lifts;"
        
        lifts = db.query(dbConnection, query1).fetchall()

        # Render the lifts.j2 file, and also send the renderer
        # a couple objects that contains lifts information
        return render_template(
            "lifts.j2", lifts=lifts      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()



# --------------------------------------------------------------------------------------------------
# SkiersLifts CRD
# no need for update
# --------------------------------------------------------------------------------------------------


@app.route("/skierslifts", methods=["GET"])
def skierslifts():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = """
            SELECT 
                SkiersLifts.SkiersLiftsID, 
                Skiers.Name AS SkierName, 
                Lifts.LiftName AS LiftName
            FROM SkiersLifts
            INNER JOIN Skiers ON SkiersLifts.Skiers_SkierID = Skiers.SkierID
            INNER JOIN Lifts ON SkiersLifts.Lifts_LiftID = Lifts.LiftID;
        """
        
        skierslifts = db.query(dbConnection, query1).fetchall()

        # Render the lifts.j2 file, and also send the renderer
        # a couple objects that contains lifts information
        return render_template(
            "skierslifts.j2", skierslifts=skierslifts      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()




# --------------------------------------------------------------------------------------------------
# Passes CRD
# only need Create, Read, and Delete
# --------------------------------------------------------------------------------------------------



@app.route("/passes", methods=["GET"])
def passes():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT * FROM Passes;"
        
        passes = db.query(dbConnection, query1).fetchall()

        # Render the passes.j2 file, and also send the renderer
        # a couple objects that contains passes information
        return render_template(
            "passes.j2", passes=passes      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# --------------------------------------------------------------------------------------------------
# RentalInventory CRD
# only need Create, Read, and Delete
# --------------------------------------------------------------------------------------------------
@app.route("/rentalinventory", methods=["GET"])
def rentalinventory():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT * FROM RentalInventory;"
        
        rentalinventory = db.query(dbConnection, query1).fetchall()

        # Render the rentalinventory.j2 file, and also send the renderer
        # a couple objects that contains rentalinventory information
        return render_template(
            "rentalinventory.j2", rentalinventory=rentalinventory      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()



# --------------------------------------------------------------------------------------------------
# SkiersRentals CRUD
# --------------------------------------------------------------------------------------------------
@app.route("/skiersrentals", methods=["GET"])
def skiersrentals():
    try:
        dbConnection = db.connectDB()
        # The query MUST match the aliases used in your .j2 template
        query = """
            SELECT 
                SkiersRentals.SkiersRentalsID, 
                Skiers.Name AS SkierName, 
                RentalInventory.Type AS ItemType
            FROM SkiersRentals
            JOIN Skiers ON SkiersRentals.Skiers_SkierID = Skiers.SkierID
            JOIN RentalInventory ON SkiersRentals.RentalInventory_RentalID = RentalInventory.RentalID;
        """
        result = db.query(dbConnection, query).fetchall()
        return render_template("skiersrentals.j2", skiersrentals=result)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while executing the database queries.", 500
    finally:
        if "dbConnection" in locals():
            dbConnection.close()





@app.route('/edit_rental/<int:rental_id>', methods=['GET', 'POST'])
def edit_rental(rental_id):
    dbConnection = db.connectDB()
    
    if request.method == 'GET':
        # Fetch the specific rental to pre-populate the form
        query = "SELECT * FROM SkiersRentals WHERE SkiersRentalsID = %s;"
        rental_data = db.query(dbConnection, query, (rental_id,)).fetchone()
        return render_template('edit_rental.j2', rental=rental_data)

    if request.method == 'POST':
        # Get data from the submitted form
        skier_id = request.form['skier_id']
        inventory_id = request.form['inventory_id']
        
        # Execute the update
        query = "UPDATE SkiersRentals SET Skiers_SkierID = %s, RentalInventory_RentalID = %s WHERE SkiersRentalsID = %s;"
        db.query(dbConnection, query, (skier_id, inventory_id, rental_id))
        
        return redirect("/skiersrentals")


# --------------------------------------------------------------------------------------------------
# SkiersTrails RU 
# only need read and update
# --------------------------------------------------------------------------------------------------
@app.route("/trails", methods=["GET"])
def trails():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT * FROM Trails;"
        
        trails = db.query(dbConnection, query1).fetchall()

        # Render the trails.j2 file, and also send the renderer
        # a couple objects that contains trails information
        return render_template(
            "trails.j2", trails=trails      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# --------------------------------------------------------------------------------------------------
# Skierstrails CRD
# only need read, update, and delete
# --------------------------------------------------------------------------------------------------
@app.route("/skierstrails", methods=["GET"])
def skierstrails():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = """
            SELECT 
                SkiersTrails.SkiersTrailsID, 
                Skiers.Name AS SkierName, 
                Trails.TrailName AS TrailName
            FROM SkiersTrails
            INNER JOIN Skiers ON SkiersTrails.Skiers_SkierID = Skiers.SkierID
            INNER JOIN Trails ON SkiersTrails.Trails_TrailID = Trails.TrailID;
        """
        
        skierstrails = db.query(dbConnection, query1).fetchall()

        # Render the skierstrails.j2 file, and also send the renderer
        # a couple objects that contains skierstrails information
        return render_template(
            "skierstrails.j2", skierstrails=skierstrails      
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()



# ########################################
# ########## LISTENER

if __name__ == "__main__":
    app.run(
        port=PORT, debug=True
    )  # debug is an optional parameter. Behaves like nodemon in Node.