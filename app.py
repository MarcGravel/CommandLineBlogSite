import mariadb
import dbcreds

conn = None
cursor = None

usr_name = input("Please type in your username: ")
usr_pass = input("Please enter your password: ")

try:
    conn = mariadb.connect(
                            user=dbcreds.user,
                            password=dbcreds.password,
                            host=dbcreds.host,
                            port=dbcreds.port,
                            database=dbcreds.database
                            )
    cursor = conn.cursor()

    #gets the password from the row with the matching username. Username is UNIQUE key in DB, so only one can match
    cursor.execute("SELECT password FROM users WHERE username=?", [usr_name])
    #fetchone will return a tuple with one element that can be selected with [0], else db_pass will be set as the complete tuple ('foo', )
    db_pass = cursor.fetchone()[0]

    if db_pass == usr_pass:
        while True:
            #blank prints for spacing and readability
            print()
            print("Which option would you like?")
            print("1. Write a new post")
            print("2. View all posts")
            
            usr_choice = input("What is your choice: ")

            try:
                conn = mariadb.connect(
                                    user=dbcreds.user,
                                    password=dbcreds.password,
                                    host=dbcreds.host,
                                    port=dbcreds.port,
                                    database=dbcreds.database
                                    )
                cursor = conn.cursor()

                if usr_choice == "1":
                    print()
                    print("Please write your new post")
                    new_post = input()
                    cursor.execute("INSERT INTO blog_post(username, content) VALUES(?,?)", [usr_name, new_post])
                    conn.commit()
                    print()
                    print("Submitted!")
                elif usr_choice == "2":
                    cursor.execute("SELECT username, content FROM blog_post")
                    #gets all data from the cursor which has received username and content from all rows in the table
                    all_posts = cursor.fetchall()
                    for post in all_posts:
                        print(post)
                else:
                    print("That is an incorrect choice")

            except mariadb.DataError:
                print("Something is wrong with your data")
            except mariadb.OperationalError:
                print("Something is wrong with your connection")
            except mariadb.ProgrammingError:
                print("Code error, check the code")
            except mariadb.IntegrityError:
                print("Your query would have broken the database and we stopped it")
            except:
                print("Something went wrong")
            
            # will close the cursor and connection if they have been active
            finally:
                if (cursor != None):
                    cursor.close()
                else:
                    print("There was never a curser to begin with")
                if (conn != None):
                    conn.rollback()
                    conn.close()
                else:
                    print("The connection never opened, nothing to close")

            #options to restart from top of while loop.
            print()
            print("Would you like to pick your options again?")
            usr_cont = input("Y/N: ")

            if(usr_cont == "Y" or usr_cont == "y"):
                pass
            elif(usr_cont == "N" or usr_cont == "n"):
                print("GoodBye!")
                break
            else: 
                print("I didnt understand that.. goodbye.")
                break
    else: 
        print("Incorrect credentials. Closing program")

except mariadb.DataError:
    print("Something is wrong with your data")
except mariadb.OperationalError:
    print("Something is wrong with your connection")
except mariadb.ProgrammingError:
    print("Code error, check the code")
except mariadb.IntegrityError:
    print("Your query would have broken the database and we stopped it")
except:
    print("There was an error")
