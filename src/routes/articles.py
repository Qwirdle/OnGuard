from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *

from __main__ import app, Users

# Keeps track of article/section names for generation
titles = {
    "1.0 Introduction to Cybersecurity": [
        "1.1 Importance of Cybersecurity in the Workplace",
        "1.2 Overview of Common Threats",
        "1.3 Quiz 1: Introduction to Cybersecurity"
    ],
    "2.0 Types of Cyber Threats": [
        "2.1 Phishing and Social Engineering",
        "2.2 Malware, Ransomware, and Viruses",
        "2.3 Insider Threats",
        "2.4 Quiz 2: Types of Cyber Threats"
    ],
    "3.0 Safe Internet Practices": [
        "3.1 Recognizing Suspicious Emails and Links",
        "3.2 Secure Browsing Habits",
        "3.3 Using Strong, Unique Passwords",
        "3.4 Quiz 3: Safe Internet Practices"
    ],
    "4.0 Device Security": [
        "4.1 Securing Mobile Devices and Laptops",
        "4.2 Importance of Software Updates",
        "4.3 Safe Use of Public Wi-Fi",
        "4.4 Quiz 4: Device Security"
    ],
    "5.0 Data Protection": [
        "5.1 Understanding Data Classification and Handling",
        "5.2 Importance of Encryption",
        "5.3 Best Practices for Data Storage and Sharing",
        "5.4 Quiz 5: Data Protection"
    ],
    "6.0 Incident Reporting": [
        "6.1 How to Report a Cybersecurity Incident",
        "6.2 Understanding the Escalation Process",
        "6.3 Importance of Timely Reporting",
        "6.4 Quiz 6: Incident Reporting"
    ],
    "7.0 Social Media and Cybersecurity": [
        "7.1 Risks Associated with Social Media",
        "7.2 Privacy Settings and Personal Information Management",
        "7.3 Quiz 7: Social Media and Cybersecurity"
    ],
    "8.0 Compliance and Regulations": [
        "8.1 Overview of Relevant Regulations (e.g., GDPR, HIPAA)",
        "8.2 Organizational Policies and Procedures",
        "8.3 Quiz 8: Compliance and Regulations"
    ],
    "9.0 Physical Security": [
        "9.1 Securing the Workplace (e.g., Locking Devices, Visitor Protocols)",
        "9.2 Importance of Access Control",
        "9.3 Quiz 9: Physical Security"
    ],
    "10.0 Best Practices for Remote Work": [
        "10.1 Secure Remote Access Protocols",
        "10.2 Maintaining Cybersecurity While Working from Home",
        "10.3 Quiz 10: Best Practices for Remote Work"
    ],
    "11.0 Cyber Hygiene": [
        "11.1 Regular Security Practices and Behaviors",
        "11.2 Importance of Security Awareness and Continuous Learning",
        "11.3 Quiz 11: Cyber Hygiene"
    ],
    "12.0 Conclusion and Resources": [
        "12.1 Summary of Key Points",
        "12.2 Resources for Further Learning and Support",
        "12.3 Final Test: Overall Cybersecurity Awareness"
    ]
}

def genChapterCompletion(user):
    """Takes in a user class from flask, and returns all their chapter completion progress in a list"""
    user = user.__dict__
    out = []
    
    idx = 0
    for articles in list(titles.values()):
        temp = []
        artIdx = 0
        for article in articles:
            temp.append(user[f"article_{idx+1}_{artIdx+1}"])
            artIdx += 1

        if all(entry == 0 for entry in temp):
            out.append("unstarted")
            continue
        elif all(entry == 2 for entry in temp):
            out.append("complete")
            continue
        elif 1 in temp or 2 in temp:
            out.append("in-progress")
        
        idx += 1
    
    return out


def genProgressData(user):
    """Takes in a user class from flask, and returns all their course progress in a list"""
    user = user.__dict__
    out = []

    idx = 0
    for chapter in list(titles.keys()):
        out.append([])
        artIdx = 0
        for article in titles[chapter]:
            if user[f"article_{idx+1}_{artIdx+1}"] == 0:
                out[idx].append("unstarted")
            elif user[f"article_{idx+1}_{artIdx+1}"] == 1:
                out[idx].append("in-progress")
            else:
                out[idx].append("complete")
        idx += 1

    return out

@app.route('/articles/<int:chapter>/<int:article>')
@login_required
def viewArticle(chapter, article):
    # Convert titles to list for ease of access
    listTitles = list(titles.values())
    
    # Translate into just the length of each chapter
    idx = 0
    for x in listTitles:
        listTitles[idx] = len(x)
        idx += 1
    
    # Check if next is going to next chapter, and if so increment
    if listTitles[chapter - 1] < article:
        article = 1
        chapter +=1
    try: # Try in order to handle accessing false articles (especially over URLs)
        if listTitles[chapter-1] < article:
            return render_template(f'articles/{chapter}/{article}.html', article=article+1, chapter=1, titles = titles, titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()))
        else:
            return render_template(f'articles/{chapter}/{article}.html', article=article, chapter=chapter, titles = titles, titles_keys = list(titles.keys()), progress_data = genProgressData(Users.query.filter_by(username=current_user.username).first()), completion_data = genChapterCompletion(Users.query.filter_by(username=current_user.username).first()))
    except:
        return render_template('error.html', message="Oops! Article not found."), 404