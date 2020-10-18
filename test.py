from flask import Flask, redirect, render_template, request, url_for
from urllib.parse import urlparse
import psycopg2
import datetime
app = Flask(__name__)

def open_db():
    conn = psycopg2.connect(database="d3a2adjcs5cen6", user = "wsnyuonotffabi",
         password = "329f2a580b108bc8368bded869db33860ee6dd9e450985a5313331850be29693",
         host = "ec2-34-251-118-151.eu-west-1.compute.amazonaws.com", port = "5432")
    print("Opened database successfully")
    cur = conn.cursor()
    return (cur, conn)


def close_db(conn):
    conn.close()

def get_all_domains(cur):
    """
    return all domains currently in database
    """
    cur.execute("SELECT * from domains")
    records = cur.fetchall()
    print(records)
    records = [record[1] for record in records]
    print(records)
    return records



@app.route("/scrape/", methods=["POST", "GET"])
def scrape():
    # open database and get cursor and connection object
    cur, conn = open_db()
    all_domains = get_all_domains(cur)
    domains = cur.execute("SELECT * FROM domains")
    print(domains)
    print(cur)
    # If post
    if request.method == "POST":
        domain = request.form["domain"]
        url = urlparse(domain)
        domain = url.scheme + "://" + url.netloc
        print(domain)
        if domain not in all_domains:
            all_domains.append(domain)
            cur.execute("INSERT INTO domains (domain, created_on) VALUES ('{}', '{}')".format(domain, datetime.datetime.now()))
            conn.commit()
            return render_template(template_name_or_list="home.html",
                    status="{} added to our database and will be scraped regularly".format(domain), all_domains=all_domains)
                    
        else:
            return render_template(template_name_or_list="home.html",
                    status="{} already being scraped".format(domain), all_domains=all_domains)
    
    #If get
    else:
        return render_template("scrape.html")

@app.route("/")
def home():
    all_domains = get_all_domains()
    return render_template("home.html", all_domains=all_domains)

if __name__ == "__main__":
    app.run(debug=True)