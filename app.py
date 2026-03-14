# ########################################
# ########## SETUP



from flask import Flask, render_template, request, redirect
import database.db_connector as db

PORT = 8089

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


# -----------------------------------------------------------------------------------------
# Reset Route
# -----------------------------------------------------------------------------------------
@app.route("/reset-db", methods=["POST"])
def reset_database():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # Call your reset procedure
        cursor.execute("CALL sp_load_front_range_data();")
        while cursor.nextset():
            pass
        dbConnection.commit()
        
        print("Database reset successful!")
        return redirect("/skiers") # Redirect back to see the fresh data

    except Exception as e:
        print(f"Error resetting database: {e}")
        return "An error occurred during database reset.", 500

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

    
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
        cursor.nextset()
        # store the generated skier id for the last inserted row. this will be the pk for the new inserted row
        cursor.execute("SELECT @new_id;")
        new_id = cursor.fetchone()[0] # id is index 0 of the row
        # cursor.nextset() # Move the the next result. Assuming this to move to the next row?
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
        return ("An error occurred while executing skiers/create this database queries. ", 500,) # ProgError, OpsError, DBError? can be more specific
    finally:
        # Close the DB Conneciton, if it exists:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route('/skiers/update', methods=['POST'])
def update_skier():
    try:
        # 1. Connect to the DB and create a cursor
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # 2. Capture data from form 'name' attributes
        # Ensure these keys match the 'name' attributes in your skiers.j2 file
        s_id = request.form['update_skier_id']
        s_name = request.form['update_skier_name']
        s_address = request.form['update_skier_address']
        s_phone = request.form['update_skier_phone']
        s_email = request.form['update_skier_email']
        s_ability = request.form['update_skier_ability']

        # 3. Call the Stored Procedure using the project's parameter syntax
        # Order: s_id, s_name, s_address, s_phone, s_email, s_ability
        query = "CALL sp_UpdateSkier(%s, %s, %s, %s, %s, %s);"
        params = (s_id, s_name, s_address, s_phone, s_email, s_ability)
        
        cursor.execute(query, params)
        dbConnection.commit()
        
        print(f"UPDATE skier successful. ID: {s_id}")

        # 4. Redirect back to the skiers table
        return redirect("/skiers")

    except Exception as e:
        print(f"Error updating skier: {e}")
        return "An error occurred while updating the skier.", 500

    finally:
        # 5. Clean up connection
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# delete pass
@app.route("/passes/delete", methods=["POST"])
def delete_passes():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        pass_id = request.form["delete_pass_id"]

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeletePass(%s);"
        cursor.execute(query1, (pass_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE pass. ID: {pass_id} Name: {pass_id}")

        # Redirect the user to the updated webpage
        return redirect("/passes")

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


# delete Lifts
@app.route("/lifts/delete", methods=["POST"])
def delete_lifts():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        lift_id = request.form["delete_lift_id"]
        

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteLifts(%s);"
        cursor.execute(query1, (lift_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE lifts. ID: {lift_id}")

        # Redirect the user to the updated webpage
        return redirect("/lifts")

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

# Lifts update

@app.route('/lifts/update', methods=['POST'])
def update_lifts():
    try:
        # 1. Connect to the DB and create a cursor
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # 2. Capture data from form 'name' attributes
        # Ensure these keys match the 'name' attributes in your skiers.j2 file
        l_id = request.form['update_lift_id']
        l_status = request.form['update_lift_status']

        # 3. Call the Stored Procedure using the project's parameter syntax
        # Order: s_id, s_name, s_address, s_phone, s_email, s_ability
        query = "CALL sp_UpdateLifts(%s, %s);"
        params = (l_id, l_status)
        
        cursor.execute(query, params)
        dbConnection.commit()
        
        print(f"UPDATE lifts successful. ID: {l_id}")

        # 4. Redirect back to the skiers table
        return redirect("/lifts")

    except Exception as e:
        print(f"Error updating skier: {e}")
        return "An error occurred while updating the lifts.", 500

    finally:
        # 5. Clean up connection
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

        query2 = "SELECT SkierID, Name FROM Skiers;"
        skiers = db.query(dbConnection, query2).fetchall()

        query3 = "SELECT LiftID, LiftName FROM Lifts;"
        lifts = db.query(dbConnection, query3).fetchall()

        # Render the lifts.j2 file, and also send the renderer
        # a couple objects that contains lifts information
        return render_template(
            "skierslifts.j2", skierslifts=skierslifts, skiers=skiers, lifts=lifts
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# create skierslifts
@app.route("/skierslifts/create", methods=["POST"])
def create_skierslifts():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        Skiers_SkierID = int(request.form["create_skier_skierId"])
        Lifts_LiftID = int(request.form["create_lift_liftId"])

        cursor.execute(
            "CALL sp_CreateSkiersLifts(%s,%s,@new_id);",
            (Skiers_SkierID, Lifts_LiftID)
        )

        cursor.nextset()

        cursor.execute("SELECT @new_id;")
        new_id = cursor.fetchone()[0]

        dbConnection.commit()

        return redirect("/skierslifts")

    except Exception as e:
        print("REAL ERROR:", e)
        return ("Create skierslifts failed", 500)

    finally:
        if "dbConnection" in locals():
            dbConnection.close()

# delete skierslifts
@app.route("/skierslifts/delete", methods=["POST"])
def delete_skierslifts():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        skierslifts_id = request.form["delete_skierslifts_id"]
        

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteSkiersLifts(%s);"
        cursor.execute(query1, (skierslifts_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE skierslifts. ID: {skierslifts_id}")

        # Redirect the user to the updated webpage
        return redirect("/skierslifts")

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




################ delete skierstrails ###########
@app.route("/skierstrails/delete", methods=["POST"])
def delete_skierstrails():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        st_id = request.form["delete_skierstrails_id"]

        cursor.execute("CALL sp_DeleteSkiersTrails(%s);", (st_id,))
        dbConnection.commit()

        print(f"DELETE skierstrails. ID: {st_id}")

        return redirect("/skierstrails")

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()
# --------------------------------------------------------------------------------------------------
# Passes CRD
# only need Create, Read, and Delete
# --------------------------------------------------------------------------------------------------



@app.route("/passes", methods=["GET"])
def passes():
    try:
        dbConnection = db.connectDB()

        passes_query = """SELECT 
        PassID, 
        Type, 
        DATE(PurchaseDate) AS PurchaseDate, 
        DATE(ExpirationDate) AS ExpirationDate, 
        Skiers_SkierID,
        Skiers.Name AS SkierName 
    FROM Passes 
    INNER JOIN Skiers ON Passes.Skiers_SkierID = Skiers.SkierID;  
        """

        
        passes = db.query(dbConnection, passes_query).fetchall()

        skiers_query = "SELECT SkierID, Name FROM Skiers;"
        skiers = db.query(dbConnection, skiers_query).fetchall()

        return render_template(
            "passes.j2",
            passes=passes,
            skiers=skiers
        )

    finally:
        if "dbConnection" in locals():
            dbConnection.close()

# create pass
@app.route("/passes/create", methods=["POST"])
def create_passes():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # 1. Collect only the essential info
        p_type = request.form["create_pass_type"]
        p_purchase_date = request.form["create_purchase_date"].replace("T"," ") + ":00"
        skier_id = int(request.form["create_skier_skierId"])

        # 2. Call procedure (Notice only 3 input params now + the OUT param)
        cursor.execute(
            "CALL sp_CreatePass(%s, %s, %s, @new_id);",
            (p_type, p_purchase_date, skier_id)
        )

        # 3. Get the ID generated by the DB
        cursor.execute("SELECT @new_id;")
        new_id = cursor.fetchone()[0]

        dbConnection.commit()
        return redirect("/passes")

    except Exception as e:
        print("DB ERROR:", e)
        return ("Create pass failed", 500)
    finally:
        if "dbConnection" in locals():
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

# create rental inventory item
@app.route("/rentalinventory/create", methods=["POST"])
def create_rentalinventory():
    dbConnection = None
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        Type = request.form["create_rental_type"]

        # 1. Execute the procedure
        cursor.execute("CALL sp_CreateRentalInventory(%s, @new_id);", (Type,))
        
        # 2. Skip the SP's internal result set (the SELECT ... AS p_new_id)
        while cursor.nextset():
            try:
                cursor.fetchone()  # Attempt to fetch from the current result set
            except:
                pass  # If there's an error, it likely means there are no more result sets to process

        # 3. Fetch the OUT parameter
        cursor.execute("SELECT @new_id;")
        row = cursor.fetchone()
        new_id = row[0] if row else None

        dbConnection.commit()
        
        print(f"Created ID: {new_id}")
        return redirect("/rentalinventory")

    except Exception as e:
        if dbConnection:
            dbConnection.rollback() # Important for data integrity
        print(f"Error: {e}")
        return "An error occurred during creation.", 500
    finally:
        if dbConnection:
            cursor.close() # Clean up the cursor too
            dbConnection.close()

@app.route("/rentalinventory/delete", methods=["POST"])
def delete_rentalinventory():
    try:
        dbConnection = db.connectDB()  # Open our database connection
        cursor = dbConnection.cursor()

        # Get form data
        rental_id = request.form["delete_rental_id"]
        

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteRentalInventory(%s);"
        cursor.execute(query1, (rental_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE rental inventory item. ID: {rental_id}")

        # Redirect the user to the updated webpage
        return redirect("/rentalinventory")

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


# create trail

@app.route("/trails/create", methods=["POST"])
def create_trails():
    try:
        dbConnection = db.connectDB() # this opens skiers db connection
        cursor = dbConnection.cursor()

        # Get form data. will do data cleansing try/catch blocks later since we don't have int input for the following attributes:
        Name = request.form["create_trail_name"]
        Difficulty = request.form["create_trail_difficulty"]
        TrailLength = request.form["create_trail_trailLength"]
        Status = request.form["create_trail_status"]


        # call create trails sp method
        query1 = "CALL sp_CreateTrail(%s, %s, %s, %s, @t_new_id);"
        cursor.execute(query1, (Name, Difficulty, TrailLength, Status))
        cursor.nextset()
        # store the generated trail id for the last inserted row. 
        cursor.execute("SELECT @new_id;")
        new_id = cursor.fetchone()[0] # id is index 0 of the row
        # cursor.nextset() # Move the the next result. Assuming this to move to the next row?
        dbConnection.commit() #commit transaction
        print(f"""Create skiers. 
        ID: {new_id} 
        Name: {Name} 
        Difficulty {Difficulty} 
        TrailLength {TrailLength} 
        Status {Status} 
        """)
        # Redirect to the updated webpage by add the path /skiers
        return redirect("/trails")
    except Exception as e:
        print(f"Error executing quereis: {e}")
        return ("An error occurred while executing trails/create this database queries. ", 500,) # ProgError, OpsError, DBError? can be more specific
    finally:
        # Close the DB Conneciton, if it exists:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# --------------------------------------------------------------------------------------------------
# SkiersRentals CRUD
# --------------------------------------------------------------------------------------------------
@app.route("/skiersrentals", methods=["GET"])
def skiersrentals():
    dbConnection = None
    try:
        dbConnection = db.connectDB()
        
        # 1. Standard queries for the table and dropdowns
        query_main = """
            SELECT SkiersRentals.SkiersRentalsID, Skiers.Name AS SkierName, RentalInventory.Type AS ItemType 
            FROM SkiersRentals 
            JOIN Skiers ON Skiers_SkierID = SkierID 
            JOIN RentalInventory ON RentalInventory_RentalID = RentalID;
        """
        results = db.query(dbConnection, query_main).fetchall()
        skiers_list = db.query(dbConnection, "SELECT SkierID, Name FROM Skiers;").fetchall()
        items_list = db.query(dbConnection, "SELECT RentalID, Type FROM RentalInventory;").fetchall()
        
        # 2. Check if a specific ID was passed for updating (e.g., /skiersrentals?id=5)
        rental_to_update = None
        target_id = request.args.get('id')
        
        if target_id:
            # Fetch the specific record to pre-fill the update form
            query_single = "SELECT * FROM SkiersRentals WHERE SkiersRentalsID = %s;"
            rental_to_update = db.query(dbConnection, query_single, (target_id,)).fetchone()

        return render_template("skiersrentals.j2", 
                               skiersrentals=results, 
                               skiers=skiers_list, 
                               rentals=items_list,
                               rental=rental_to_update) # This prevents the 'undefined' error
    finally:
        if dbConnection:
            dbConnection.close()


# --- CREATE ROUTE ---
@app.route("/skiersrentals/create", methods=["POST"])
def create_skiersrentals():
    dbConnection = None
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        s_id = request.form["create_skier_skierId"]
        r_id = request.form["create_rental_rentalId"]

        # Call procedure with OUT parameter
        cursor.execute("CALL sp_CreateSkiersRentals(%s, %s, @sr_id);", (s_id, r_id))
        
        # Clear cursor to prevent "Commands out of sync" error
        while cursor.nextset():
            pass

        dbConnection.commit()
        return redirect("/skiersrentals")
    except Exception as e:
        print(f"CREATE ERROR: {e}")
        return "Failed to create rental.", 500
    finally:
        if dbConnection:
            dbConnection.close()


@app.route("/skiersrentals/update", methods=["POST"])
def update_skiersrentals():
    dbConnection = None
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # 1. Capture the IDs from the form
        # 'update_rental_id' is usually a hidden input in your edit form
        rental_id = request.form["update_rental_id"]
        skier_id = request.form["update_skier_id"]
        item_id = request.form["update_item_id"]

        # 2. Call the Update Stored Procedure
        cursor.execute(
            "CALL sp_UpdateSkiersRentals(%s, %s, %s);", 
            (rental_id, skier_id, item_id)
        )
        
        # Clear cursor and commit
        while cursor.nextset():
            pass
        dbConnection.commit()
        
        print(f"Successfully updated Rental ID: {rental_id}")
        return redirect("/skiersrentals")

    except Exception as e:
        print(f"UPDATE ERROR: {e}")
        return f"Update failed: {e}", 500
        
    finally:
        if dbConnection:
            dbConnection.close()





################ delete skiersrentals ###########
@app.route("/skiersrentals/delete", methods=["POST"])
def delete_skiersrentals():
    try:
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        sr_id = request.form["delete_skiersrentals_id"]

        cursor.execute("CALL sp_DeleteSkiersRentals(%s);", (sr_id,))
        dbConnection.commit()

        print(f"DELETE skiersrentals. ID: {sr_id}")

        return redirect("/skiersrentals")

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


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

@app.route('/trails/update', methods=['POST'])
def update_trails():
    try:
        # 1. Connect to the DB and create a cursor
        dbConnection = db.connectDB()
        cursor = dbConnection.cursor()

        # 2. Capture data from form 'name' attributes
        # Ensure these keys match the 'name' attributes in your skiers.j2 file
        t_id = request.form['update_trail_id']
        t_status = request.form['update_trail_status']

        # 3. Call the Stored Procedure using the project's parameter syntax
        # Order: s_id, s_name, s_address, s_phone, s_email, s_ability
        query = "CALL sp_UpdateTrails(%s, %s);"
        params = (t_id, t_status)
        
        cursor.execute(query, params)
        dbConnection.commit()
        
        print(f"UPDATE trails successful. ID: {t_id}")

        # 4. Redirect back to the skiers table
        return redirect("/trails")

    except Exception as e:
        print(f"Error updating trails: {e}")
        return "An error occurred while updating the trails.", 500

    finally:
        # 5. Clean up connection
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