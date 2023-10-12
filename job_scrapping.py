from tkinter import messagebox,simpledialog,Tk #gui
from turtle import position
import requests
import csv
from bs4 import BeautifulSoup #scrape
from requests.models import Response

#function to get the desired position for the search
def get_position(position):
    #simpledialog is the gui that will ask user to input value in string
    position = simpledialog.askstring('Position','What position are you searching for?')
    return position

#function to get the location of the search
def get_location(location):
    #simpledialog is the gui that will ask user to input value in string
    location=simpledialog.askstring('Location','Where are you searching for this position?(city,state,postcode)')
    return location

#function to create the url of the site
def get_url(position,location):
    #q and l are the variable and the value will input by user
    #q is for the postion t hat user want, l is for the location that user want
    url_template = "https://malaysia.indeed.com/jobs?q={}&l={}"
    #input the values of variables into the url and return it
    url = url_template.format(position,location)
    return url

#function to pull the different pieces of jobs data from different listings
def record_collector(slider):
    #pull job title in the h2 jobTitle, title
    job_title = slider.find("h2",'jobTitle', 'title').text.strip()
    #pull company name in the span companyName
    company_name = slider.find('span','companyName').text.strip()
    #pull company_location in the div companyLocation
    company_location=slider.find('div','companyLocation').text.strip()
    #pull job desc in div job-snippet
    job_description=slider.find('div','job-snippet').text.strip()
    #pull job date posted in span date
    job_date=slider.find('span','date').text.strip()
    #job_url= 'https://malaysia.indeed.com'+ slider.find('href')
    #because not every job posted has salary so need to be conditional
    job_pay=slider.find('class','salary-snippet')
    if job_pay:
        salary = job_pay.text
    else:
        salary=''
    record = (job_title,company_name,company_location,salary,job_date,job_description)
    return record


root=Tk()
#main function to run everything
def main(position,location):
        
    #array declared
    records=[]
    #function call
    position=get_position(position)
    location=get_location(location)
    url=get_url(position,location)
    
    #while statement that allows the files to
    while True:
            #used to access data for a specific resource; request for URL
            page=requests.get(url)
            #package for parsing the html
            whole_page = BeautifulSoup(page.text,'html.parser')
            #find_all(); returning all the matches after scanning the entire document
            #all the data for the job is under the div - slider_item
            sliders= whole_page.find_all('div','slider_item')
            
            #goes through each slider and extract the necessary informations
            for slider in sliders:
                #past data from record_collector to record variable
                record=record_collector(slider)
                #add the nodes into the list of records
                records.append(record)
                #output the record
                print(record)
            
            
            try:
                #find record in the next page
                url="https://malaysia.indeed.com" + whole_page.find('a', {'aria-label':'Next'}).get('href')
            except AttributeError:
                break
        #gui for the scrapping finished
    messagebox.showinfo('Progress','Web scrapping finished!')
    
    
    #write everthing into csv
    with open(f'{position + location}.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        #wite the column
        writer.writerow(['JobTitle','Company','Location','Pay','Posted','Description'])
        #wirte all the records in th csv file
        writer.writerows(records)
          
main('','')
#main window which we execute when we want to run our application
root.mainloop()