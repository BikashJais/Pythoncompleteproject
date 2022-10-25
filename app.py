from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen as uReq
import logging_file
import mongodb_conn
import mysql_conn


app = Flask(__name__)



@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    logging_file.config()
    #mysql_conn.sql_config()
    return render_template("index.html")

@app.route('/review', methods=['POST','GET']) # route to show the details of product  in a web UI
@cross_origin()
def index():
    '''
    this function is used to fetch all the top product details like product name, product rating,price
    percentage offer,number of ratings and reviews given, image url and product_url
                                                                                    '''
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            searchString = searchString + "phones"
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            product= flipkart_html.findAll("div",{"class": "_2kHMtA"})

            reviews = []
            for i in range(len(flipkart_html.findAll("div", {"class": "_2kHMtA"}))):
                try:
                    product_name = flipkart_html.findAll("div",{"class":"_4rR01T"})[i].text
                except:
                    name = 'No Name'
                    logging_file.error(f"Name not present for {i}th product")

                try:
                    product_rating = flipkart_html.findAll("div",{"class":"_3LWZlK"})[i].text
                except:
                    rating = 'No Rating'
                    logging_file.error(f"Rating not present for {i}th product")

                try:
                    price = flipkart_html.findAll("div",{"class":"_30jeq3 _1_WHN1"})[i].text
                except:
                    price = 'No price'
                    logging_file.error(f"Price not present for {i}th product")
                try:
                    percentage_off=flipkart_html.findAll("div",{"class":"_3Ay6Sb"})[i].text
                except:
                    percentage_off ='not available'
                    logging_file.error(f"Percentage_off not present for {i}th product")

                try:
                    ratingreviews=product[i].find("span",{"class":"_2_R_DZ"}).text
                except:
                    ratings= 'not available'
                    logging_file.error(f"Number of rating and review  not present for {i}th product")

                try:
                    img_url=product[i].find("img",{"class":"_396cs4 _3exPp9"}).get('src')
                except:
                    ratings= 'not available'
                    logging_file.error(f"Image not present for {i}th product")

                try:
                    com_url="https://www.flipkart.com" + product[i].find("a",{"class":"_1fQZEK"}).get('href')
                except:
                    ratings = 'not available'
                    logging_file.error(f"Comment_url not present for {i}th product")

                logging_file.info(f" product details successfully fetched for {i}th product")

                mydict = {"prod_description": product_name,"product_price": price,"product_Rating": product_rating,"num_of_ratings": ratingreviews,"perc_off": percentage_off,
                          "image_url":img_url,"comment_url":com_url}

                reviews.append(mydict)

            try:
                fetch_detail= mysql_conn.save_to_sql(reviews)
            except:
                logging_file.error("failed to connect to sql from function")
            return render_template('results.html', product_details=fetch_detail)
        except Exception as e:
            logging_file.error(f"{e} error in product details fetching")
            return 'something went wrong'

    else:
        return render_template('index.html')

@app.route('/comment',methods=['POST','GET']) # route to show the customer review dteails in a web UI
@cross_origin()
def comments():
    '''
        this funtion is used to fetch all the details of particular product when clicked on comments button .
        Details are fetched like customer name, customer given rating, comment header, and comment provide
                                                                                                      '''
    try:
        if request.method == 'GET':
            return render_template("index.html")

        else:    
            product_url= request.form.get('product_url')
            uClient = uReq(product_url)
            commentpage = uClient.read()
            uClient.close()
            prod_html = bs(commentpage, "html.parser")
            reviews1=[]

            for i in range(len(prod_html.findAll("p",{"class":"_2sc7ZR _2V5EHH"}))):
                try:
                    customer_name = prod_html.findAll("p", {"class": "_2sc7ZR _2V5EHH"})[i].text
                except:
                    customer_name = 'No Name'
                    logging_file.error(f"customer name is not present for {i}th review")

                try:
                    customer_rating = prod_html.findAll ("div",{"class":"_3LWZlK _1BLPMq"})[i].text
                except:
                    customer_rating = 'No Rating'
                    logging_file.error(f"customer rating is not present {i}th review")

                try:
                    comment_head = prod_html.findAll ("p",{"class":"_2-N8zT"})[i].text
                except:
                    customer_head = 'No header'
                    logging_file.error(f"customer header  comment is not present {i}th review")

                try:
                    customer_comment = prod_html.findAll ("div",{"class":"t-ZTKy"})[i].text
                except:
                    customer_comment = 'No comment'
                    logging_file.error(f"customer comment is not present {i}th review")

                logging_file.info(f"review details successfully fetched from {i}th customer ")

                mydict1 = {"cust_name": customer_name, "cust_rating": customer_rating, "comm_head": comment_head,
                          "cust_commnt": customer_comment}
                reviews1.append(mydict1)


            try:
                record= mongodb_conn.save_to_mongodb(reviews1)
            except:
                logging_file.error("failed to connect to sql from function")

            return render_template('response.html', customer_reviews=record )
    except Exception as e:
        logging_file.error(f"{e} error in review fetching")
        return 'Something went wrong'





if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
