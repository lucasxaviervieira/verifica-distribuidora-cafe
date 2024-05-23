import urllib.request
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_password():
    with open('SECRET.txt', 'r') as file:
        password = file.read().strip()
    return password


def send_email(user, program, price):
    msg = MIMEMultipart()
    message = (
        f"O café no plano {program} está disponível para a compra no valor de {price}"
    )
    password = get_password()
    msg["From"] = "python.message.to.tasks@gmail.com"
    msg["To"] = user
    msg["Subject"] = "CAFÉ - CAFÉ - CAFÉ"
    msg.attach(MIMEText(message, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()


def get_price(page_text):
    s = page_text.find(">$") + 2
    e = page_text.find("<", s)
    price = float(page_text[s:e])
    return price


def is_ok_buy_coffe(price, price_to_buy):
    result = True if price < price_to_buy else False
    return result


def loop_to_get_right_price(url, user, program, max_price):
    while True:
        coffe_site = urllib.request.urlopen(url)
        text = coffe_site.read().decode("utf8")
        coffe_price = get_price(text)
        print(f"\nPreço do café: ", coffe_price)
        is_ok = is_ok_buy_coffe(coffe_price, max_price)
        if is_ok:
            send_email(user, program, coffe_price)
            print("\npode comprar\n")
        else:
            print("\ncompra não, tá mt caro :P\n")
        time.sleep(900)


def have_number(input):
    for i in input:
        if i.isalpha():
            continue
        else:
            return True
    return False


def format_input_price(input_price):
    max_price = []
    for i in input_price:
        if i.isalpha():
            continue
        else:
            max_price.append(i)
    max_price = "".join(max_price)
    max_price = max_price.replace(",", ".")
    return float(max_price)


def main():
    user = input(
        "\nPara receber notificações sobre a compra do café\nDigite seu email: "
    )
    case = "0"
    while case not in ["1", "2"]:
        case = input(
            "\nDigite o número de qual café você irá comprar.\n"
            + "\n 1: Café para todos clientes"
            + "\n 2: Café para clientes no programa de fidelidade\n"
            + "\nSelecione: "
        )
    if case == "1":
        url = "http://beans.itcarlow.ie/prices.html"
        program = "normal"
    else:
        url = "http://beans.itcarlow.ie/prices-loyalty.html"
        program = "para clientes no programa de fidelidade"

    while True:
        price_wanted = input("\nPreço máximo para à compra do café: ")
        if len(price_wanted) > 0 and have_number(price_wanted):
            max_price = format_input_price(price_wanted)
            print("\nPreço máximo:", max_price)
            break

    awnser = ""
    while awnser not in ["s", "n"]:
        awnser = input("\nIniciar loop? (s/n) ").lower()
    if awnser == "s":
        loop_to_get_right_price(url, user, program, max_price)
    else:
        main()


if __name__ == "__main__":
    main()
