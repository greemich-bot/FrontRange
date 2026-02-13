# ########################################
# ########## SETUP

from flask import Flask, render_template, request, redirect
import database.db_connector as db

PORT = 12198

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


@app.route("/bsg-people", methods=["GET"])
def bsg_people():
    try:
        dbConnection = db.connectDB()  # Open our database connection

        # Create and execute our queries
        # In query1, we use a JOIN clause to display the names of the homeworlds,
        #       instead of just ID values
        query1 = "SELECT bsg_people.id, bsg_people.fname, bsg_people.lname, \
            bsg_planets.name AS 'homeworld', bsg_people.age FROM bsg_people \
            LEFT JOIN bsg_planets ON bsg_people.homeworld = bsg_planets.id;"
        query2 = "SELECT * FROM bsg_planets;"
        people = db.query(dbConnection, query1).fetchall()
        homeworlds = db.query(dbConnection, query2).fetchall()

        # Render the bsg-people.j2 file, and also send the renderer
        # a couple objects that contains bsg_people and bsg_homeworld information
        return render_template(
            "bsg-people.j2", people=people, homeworlds=homeworlds
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

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
# ########################################
# ########## LISTENER

if __name__ == "__main__":
    app.run(
        port=PORT, debug=True
    )  # debug is an optional parameter. Behaves like nodemon in Node.