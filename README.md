# Project README  

## Overview  

This project is divided into two scenarios: **Scenario 1** and **Scenario 2**, each with its own set of dependencies and requirements.  

The purpose of this project is to implement a solution for GovTech's take-home test.  

I won't be including or describing the exact scenario and question.  

Each scenario is self-contained but follows a common methodology of **ETL (Extract, Transform, Load)**:  

- **Extract**: Fetching data.  
- **Transform**: Joining, normalizing, and cleaning.  
- **Load**: Presenting the data in a DataFrame for download or search.  

---

## Scenarios  

### **Scenario 1**: Streamlit Web App  

A **Streamlit web app** that can be deployed locally or on **Streamlit Cloud**.  

It has also been deployed to Streamlit Cloud and can be accessed via:  
🔗 **[CLICK HERE](https://tanjiahaoisaac-takehometestgt2025-scenario1streamlit-wm0nh2.streamlit.app/)**  

### **Scenario 2**: Command-Line Interface (CLI)  

A **Python CLI application** that runs through the terminal.  

---

## A. Instructions to Run the Code Locally  

### **1. Clone the Repository**  

Clone the repository to your local machine:  
```bash
git clone https://github.com/tanjiahaoisaac/takehometestGT2025.git
```
### FOR SCENARIO 1
### **2. Install Python and Dependencies**
Navigate to the scenario1 folder:
```bash
cd scenario1
```
(OPTIONAL)Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate #FOR WINDOWS

```
Install the required libraries:
```bash
pip install -r requirements.txt
```
### **3. Run the streamlit application**
3. Run the streamlit application:
```bash
streamlit run streamlit.py
```
### **4. Usage**
The 3 subtask will load once app run.

First: The restaurant details with countries in the given xlsx.

Second: Giltering by month & year. I allowed user input for this filtering.

Third: Analysis of the rating scores and text.

---

### FOR SCENARIO 2
### **2. Install Python and Dependencies**
Navigate to the scenario1 folder:
```bash
cd scenario2
```
(OPTIONAL)Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate #FOR WINDOWS
```
Install the required libraries:
```bash
pip install -r requirements.txt
```
### **3. Run the cli application**
```bash
python main.py  
```
### **4. Usage**
The CLI will load.

  1. Search carpark details by the carpark code. (Case don't matter)
   
  2. "r" for reload of carpark information.
   
  3. "exit" to quit
     
(From a functionality business use case, since it is a real time api to get carpark information for user, I also eliminated stale carpark details when it has not been updated for the past 15 mins at the time of fetch.)


---

## B. Design and Deployment Summary Going forawrd
Scenario 1: 

Platform: Streamlit Cloud offers a simple and efficient platform for deploying Python-based web applications. 

Data Storage: Input data and results are stored in Amazon S3. Could also allow for user input such as the countries mapping file.

Compute: Streamlit Cloud is severless, as it auto-scales and we do not need to provision the servers.

Scalability: Streamlit Cloud auto-scales. We do not need manual resource management, which is essential for applications with varying user loads.

Security: S3’s allow data to be securely stored. The Streamlit app will only interact with S3 using IAM roles with appropriate access policies. Rather than everything stored with the frontend.

![image](https://github.com/user-attachments/assets/88c08817-2d54-46af-a6b6-a83b1e743468)

Assumptions:

1. Minimal computational power needed. 
2. Data size is manageable within the limits of the Streamlit Cloud environment.
3. Users have internet access( as this is about cloud deployment)  
4. API to get data always avaliable

More complex version:

For larger data size, we can seperate the frontend and the data processing into the backend.

For example employ all the autoscaling group, load balancing, if more complex processing needed. 

For anymore complex frontend, we can deploy a webapp such as using frontend frameworks like react or vue.

To further hide restaurant data api we can utilise the backend instance to call it instead.

Seperation of concern allows us to split workload and work in parallel as well.

We may need to cache data just in case API goes down.

---

Scenario 2: 

Platform:  Application frontend allows easier access, in the context of a driver needing carpark info.

Data Storage: Carpark info are stored in Amazon S3.

Compute: Backend could be EC2 instance as carparks in Singapore limited, we can estimate computational power needed to perform such joining and cleaning info on a set interval.

Scalability: In terms of number of users accessing at the same time, we can use cdn to cache.

Security: S3’s allow data to be securely stored. The Streamlit app will only interact with S3 using IAM roles with appropriate access policies. Rather than everything stored with the frontend.

![image](https://github.com/user-attachments/assets/64f3dc61-3f08-414e-8b0c-af0f81167252)

Assumptions:

1. Users have internet access( as this is about cloud deployment)  
2. API to get data always avaliable

More complex version:

Application for user phone could be flutter or react native. 

Can allow for a visual repsentation of carpark detail on actual SG map.

Allow for search by address and/or more fuzzy forms of searching.(not need search via exact matching)

Get info via REST api.

Simple backend to process and deal with api calls.

---


## C. Current key design considerations
Used function based programming and not object-oriented programming (OOP), as this was faster and easier and cause it isn't too complex.

To focus on scaling and extending the system, could have gone for object programming.


Test cases are simplified to the excel sheet labelled testing. To save time. Could have done actual pytest if I spent more time on this.



