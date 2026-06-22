from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import pymysql
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import io
import base64


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})


def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html', {})


def Register(request):
    if request.method == 'GET':
        return render(request, 'Register.html', {})


def UserLoginAction(request):

    if request.method == 'POST':

        username = request.POST.get('t1')
        password = request.POST.get('t2')

        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='tumorDB',
            charset='utf8'
        )

        with con:

            cur = con.cursor()

            cur.execute(
                "SELECT * FROM register WHERE username=%s AND password=%s",
                (username, password)
            )

            row = cur.fetchone()

        if row:

            file = open('session.txt', 'w')
            file.write(username)
            file.close()

            return render(
                request,
                'UserScreen.html',
                {'data': 'Welcome : ' + username}
            )

        return render(
            request,
            'UserLogin.html',
            {'data': 'Invalid login details'}
        )
def runOSTU(request):
    if request.method == 'GET':
        return render(request, 'runOSTU.html', {})


def runDBIM(request):
    if request.method == 'GET':
        return render(request, 'runDBIM.html', {})


def runOSTUAction(request):
    if request.method == 'POST':
        myfile = request.FILES['t1']

        if os.path.exists("TumorApp/static/test.png"):
            os.remove("TumorApp/static/test.png")

        fs = FileSystemStorage()
        fs.save('TumorApp/static/test.png', myfile)

        image = cv2.imread("TumorApp/static/test.png")
        image = cv2.resize(image, (250, 250))

        enhanced = cv2.detailEnhance(image, sigma_s=5, sigma_r=0.05)
        gray_img = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray_img, 155, 200, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        otsu = cv2.bitwise_and(image, image, mask=thresh)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        otsu = cv2.cvtColor(otsu, cv2.COLOR_BGR2RGB)

        fig, axs = plt.subplots(1, 2, figsize=(8, 4))
        axs[0].imshow(image)
        axs[1].imshow(otsu)
        axs[0].set_title("Original Image")
        axs[1].set_title("OTSU Segmentation")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()

        img_b64 = base64.b64encode(buf.getvalue()).decode()
        return render(request, 'runOSTU.html', {'data': img_b64})


def dbim(img, sigma_value=0.33):
    median = np.median(img)
    lower_value = int(max(0, (1.0 - sigma_value) * median))
    upper_value = int(min(255, (1.0 + sigma_value) * median))
    return cv2.Canny(img, lower_value, upper_value)


def runDBIMAction(request):
    if request.method == 'POST':
        myfile = request.FILES['t1']

        if os.path.exists("TumorApp/static/test.png"):
            os.remove("TumorApp/static/test.png")

        fs = FileSystemStorage()
        fs.save('TumorApp/static/test.png', myfile)

        image = cv2.imread("TumorApp/static/test.png")
        image = cv2.resize(image, (250, 250))

        enhance = cv2.detailEnhance(image, sigma_s=5, sigma_r=0.05)
        enhanced = cv2.detailEnhance(image, sigma_s=5, sigma_r=0.05)

        tumor_image = np.zeros((250, 250, 3), np.uint8)
        tumor_image[:] = (110, 50, 50)

        gray_img = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

        _, thresh_value = cv2.threshold(gray_img, 170, 220, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
        process_img = cv2.morphologyEx(thresh_value, cv2.MORPH_CLOSE, kernel)
        process_img = cv2.erode(process_img, None, iterations=14)
        process_img = cv2.dilate(process_img, None, iterations=13)

        dbim_image = dbim(process_img)

        contours, _ = cv2.findContours(dbim_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x, y, w, h = cv2.boundingRect(contours[0])

        roi = enhanced[y:y + h, x:x + w]
        tumor_image[y:y + h, x:x + w] = roi

        cv2.drawContours(enhanced, contours, -1, (0, 0, 255), 2)

        fig, axs = plt.subplots(1, 4, figsize=(10, 5))

        axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axs[1].imshow(cv2.cvtColor(enhance, cv2.COLOR_BGR2RGB))
        axs[2].imshow(cv2.cvtColor(tumor_image, cv2.COLOR_BGR2RGB))
        axs[3].imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))

        axs[0].set_title("Original Image")
        axs[1].set_title("Enhanced Image")
        axs[2].set_title("Tumor Image")
        axs[3].set_title("Segmented Image")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()

        img_b64 = base64.b64encode(buf.getvalue()).decode()
        return render(request, 'runDBIM.html', {'data': img_b64})


def Signup(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        address = request.POST.get('address')

        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='tumorDB',
            charset='utf8'
        )

        with con:

            cur = con.cursor()

            query = """
            INSERT INTO register
            (username,password,contact,email,address)
            VALUES (%s,%s,%s,%s,%s)
            """

            cur.execute(
                query,
                (username, password, contact, email, address)
            )

            con.commit()

        return render(
            request,
            'Register.html',
            {'data': 'Signup Process Completed'}
        )