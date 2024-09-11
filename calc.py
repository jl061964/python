import streamlit as st
import math

class HP12C:
    def __init__(self):
        self.stack = []
        self.memory = 0

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return 0

    def add(self):
        if len(self.stack) >= 2:
            self.push(self.pop() + self.pop())

    def subtract(self):
        if len(self.stack) >= 2:
            b = self.pop()
            a = self.pop()
            self.push(a - b)

    def multiply(self):
        if len(self.stack) >= 2:
            self.push(self.pop() * self.pop())

    def divide(self):
        if len(self.stack) >= 2:
            b = self.pop()
            a = self.pop()
            if b != 0:
                self.push(a / b)
            else:
                st.error("Erro: Divisão por zero")

    def pv(self, fv, rate, n):
        pv = fv / ((1 + rate) ** n)
        self.push(pv)

    def fv(self, pv, rate, n):
        fv = pv * ((1 + rate) ** n)
        self.push(fv)

    def pmt(self, pv, rate, n):
        pmt = pv * rate / (1 - (1 + rate) ** -n)
        self.push(pmt)

    def rate(self, pv, fv, n):
        rate = (fv / pv) ** (1 / n) - 1
        self.push(rate)

    def nper(self, pv, fv, rate):
        nper = math.log(fv / pv) / math.log(1 + rate)
        self.push(nper)

    def price(self, face_value, coupon_rate, market_rate, n):
        price = 0
        for t in range(1, n + 1):
            price += (face_value * coupon_rate) / ((1 + market_rate) ** t)
        price += face_value / ((1 + market_rate) ** n)
        self.push(price)

    def amortization(self, principal, rate, n):
        amortization = principal * rate / (1 - (1 + rate) ** -n)
        self.push(amortization)

    def sac(self, principal, rate, n):
        amortization = principal / n
        payments = []
        for i in range(n):
            interest = (principal - i * amortization) * rate
            payment = amortization + interest
            payments.append(payment)
        self.push(payments)

    def sin(self, angle):
        self.push(math.sin(math.radians(angle)))

    def cos(self, angle):
        self.push(math.cos(math.radians(angle)))

    def tan(self, angle):
        self.push(math.tan(math.radians(angle)))

    def clear(self):
        self.stack = []

    def memory_store(self):
        if self.stack:
            self.memory = self.pop()

    def memory_recall(self):
        self.push(self.memory)

    def memory_clear(self):
        self.memory = 0

# Função principal para a interface Streamlit
def main():
    st.set_page_config(page_title="Calculadora HP-12C", layout="centered")
    st.title("Calculadora HP-12C")

    calc = HP12C()

    st.sidebar.title("Operações")
    operacao = st.sidebar.selectbox("Escolha uma operação", ["Adição", "Subtração", "Multiplicação", "Divisão", "Valor Presente (PV)", "Valor Futuro (FV)", "Pagamento (PMT)", "Taxa de Juros (i)", "Número de Períodos (n)", "Preço de Título", "Amortização Constante", "SAC", "Seno", "Cosseno", "Tangente", "Memória (M+)", "Memória (MR)", "Memória (MC)", "Limpar Pilha"])

    st.write("### Entrada de Dados")
    if operacao in ["Adição", "Subtração", "Multiplicação", "Divisão"]:
        a = st.number_input("Digite o primeiro número", format="%.2f")
        b = st.number_input("Digite o segundo número", format="%.2f")
        calc.push(a)
        calc.push(b)
        if st.button("Calcular"):
            if operacao == "Adição":
                calc.add()
            elif operacao == "Subtração":
                calc.subtract()
            elif operacao == "Multiplicação":
                calc.multiply()
            elif operacao == "Divisão":
                calc.divide()
            st.write(f"### Resultado: {calc.pop():.2f}")

    elif operacao == "Valor Presente (PV)":
        fv = st.number_input("Digite o valor futuro (FV)", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular PV"):
            calc.pv(fv, rate, n)
            st.write(f"### Valor Presente (PV): {calc.pop():.2f}")

    elif operacao == "Valor Futuro (FV)":
        pv = st.number_input("Digite o valor presente (PV)", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular FV"):
            calc.fv(pv, rate, n)
            st.write(f"### Valor Futuro (FV): {calc.pop():.2f}")

    elif operacao == "Pagamento (PMT)":
        pv = st.number_input("Digite o valor presente (PV)", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular PMT"):
            calc.pmt(pv, rate, n)
            st.write(f"### Pagamento (PMT): {calc.pop():.2f}")

    elif operacao == "Taxa de Juros (i)":
        pv = st.number_input("Digite o valor presente (PV)", format="%.2f")
        fv = st.number_input("Digite o valor futuro (FV)", format="%.2f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular Taxa de Juros"):
            calc.rate(pv, fv, n)
            st.write(f"### Taxa de Juros (i): {calc.pop():.4f}")

    elif operacao == "Número de Períodos (n)":
        pv = st.number_input("Digite o valor presente (PV)", format="%.2f")
        fv = st.number_input("Digite o valor futuro (FV)", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        if st.button("Calcular Número de Períodos"):
            calc.nper(pv, fv, rate)
            st.write(f"### Número de Períodos (n): {calc.pop():.0f}")

    elif operacao == "Preço de Título":
        face_value = st.number_input("Digite o valor de face", format="%.2f")
        coupon_rate = st.number_input("Digite a taxa de cupom", format="%.4f")
        market_rate = st.number_input("Digite a taxa de mercado", format="%.4f")
        n = st.number_input("Digite o número de períodos", format="%.0f")
        if st.button("Calcular Preço"):
            calc.price(face_value, coupon_rate, market_rate, n)
            st.write(f"### Preço de Título: {calc.pop():.2f}")

    elif operacao == "Amortização Constante":
        principal = st.number_input("Digite o principal", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular Amortização"):
            calc.amortization(principal, rate, n)
            st.write(f"### Amortização Constante: {calc.pop():.2f}")

    elif operacao == "SAC":
        principal = st.number_input("Digite o principal", format="%.2f")
        rate = st.number_input("Digite a taxa de juros (i)", format="%.4f")
        n = st.number_input("Digite o número de períodos (n)", format="%.0f")
        if st.button("Calcular SAC"):
            calc.sac(principal, rate, n)
            payments = calc.pop()
            for i, payment in enumerate(payments, 1):
                st.write(f"### Parcela {i}: {payment:.2f}")

    elif operacao == "Seno":
        angle = st.number_input("Digite o ângulo em graus", format="%.2f")
        if st.button("Calcular Seno"):
            calc.sin(angle)
            st.write(f"### Seno: {calc.pop():.4f}")

if __name__ == "__main__":
    main()
