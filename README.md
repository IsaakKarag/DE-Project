Welcome to my data engineering project - an end-to-end automated pipeline for analyzing electricity prices! 🚀

# Project Title " Analyzing Electricity Prices Through Online Data" 

# Project Overview
In this project, I've constructed a robust data pipeline that seamlessly collects, transforms, and analyzes electricity price data sourced directly from online sources. 
Leveraging Python's Beautiful Soup, I've crafted a powerful web scraper that diligently fetches daily electricity prices across Europe from 2022-01-01 until today.


# Infrastructure
Behind the scenes, I've engineered a cutting-edge infrastructure that orchestrates this data journey flawlessly. Nestled within my trusty Ubuntu machine, two Docker containers work tirelessly to handle the heavy lifting. The first container houses a PostgreSQL database where our precious data finds its home. Meanwhile, the second container hosts Airflow, our automation maestro, orchestrating daily runs of our DAG at precisely 18:00.


![Screenshot from 2024-02-02 12-01-13](https://github.com/IsaakKarag/DE-Project/assets/93320620/1fa11ee9-90ce-45c6-88f3-0d14193f8c04)


# Data Transformation
But wait, there's more! Within our Airflow DAG lies a treasure trove of data transformation and cleaning scripts. These scripts ensure our data is pristine and ready for analysis before gracefully loading it into our PostgreSQL database.

![Screenshot from 2024-02-02 12-02-42](https://github.com/IsaakKarag/DE-Project/assets/93320620/8504e414-94ec-4567-a284-d0ce1cf7ad72)



![Screenshot from 2024-02-02 12-04-38](https://github.com/IsaakKarag/DE-Project/assets/93320620/4c4eab42-6f61-4876-b2d1-ff382408b2c0)



# Insightful Visualizations
Once our data is snugly tucked away in PostgreSQL, it's time to unleash the power of insights! Using PowerBI, I've crafted a series of interactive dashboards that paint a vivid picture of electricity price trends, helping stakeholders glean actionable insights at a glance.


# Predictive Analytics
But why stop there? I've taken this project to the next level by implementing sophisticated time-series predictive models. By forecasting tomorrow's electricity prices, we empower decision-makers with foresight, allowing them to stay ahead of the curve in an ever-evolving energy landscape (ARIMA model wins).


![Screenshot from 2024-02-02 12-03-43](https://github.com/IsaakKarag/DE-Project/assets/93320620/6c83a54b-89b4-4938-8ccf-f2a4f85c4774)


# Why This Project Shines
This isn't just a project - it's a testament to my prowess as a data engineer. By seamlessly integrating cutting-edge technologies and methodologies, I've crafted a comprehensive end-to-end solution that not only automates data processing but also delivers actionable insights and predictive capabilities. From web scraping to predictive modeling, this project showcases my ability to tackle complex challenges head-on and deliver tangible value.


# Infrastructure Choice
You might wonder why I opted not to utilize a cloud provider's virtual machine. The reason lies in the scale of our data. With less than a million rows to manage so far, I chose to leverage the computational power of my local machine and Ubuntu setup to minimize project costs. Additionally, this decision positions us for easy migration to the cloud in the future, ensuring scalability without sacrificing efficiency.
