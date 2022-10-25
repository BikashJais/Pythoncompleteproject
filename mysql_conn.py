import mysql.connector as conn
import pandas as pd
import logging_file



def save_to_sql(data):
    try:
        mydb = conn.connect(host="localhost", user="root", passwd="Bikoo@1996")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS flipkart_scrapper")
        mycursor.execute("USE flipkart_scrapper")
        mycursor.execute("""CREATE TABLE IF NOT EXISTS flipkart_product (descriptions varchar(100),
                                                                        Prices varchar(10) ,
                                                                        avg_ratings varchar(100), 
                                                                        rating_counts varchar(100),
                                                                        percentage_offs varchar(20), 
                                                                        image_urls varchar(300), 
                                                                        comment_urls varchar(500))""")
        logging_file.info("table creation successful")
        mycursor.execute(f"DELETE FROM flipkart_product")
        mycursor.executemany("""INSERT INTO flipkart_product 
                            (descriptions,Prices,avg_ratings,rating_counts,percentage_offs,image_urls,comment_urls)
                            VALUES (%(prod_description)s, %(product_price)s, %(product_Rating)s, %(num_of_ratings)s,%(perc_off)s, %(image_url)s, %(comment_url)s)
                            """,data)
        logging_file.info("insertion of data successful")
        mydb.commit()
        mycursor.execute("select * from flipkart_scrapper.flipkart_product")
        return mycursor.fetchall()


    except Exception as e:
        logging_file.error(e)
