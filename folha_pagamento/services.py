class CalculadoraFolhaPagamento:

    def __init__(self, salario_base): ## salario base nao tem horas extras nem descontos aplicados a ele
        self.salario_base = salario_base

    def calcular_valor_hora(self):
        valor_hora = self.salario_base/220
        return valor_hora

    def calcular_horas_extras(self, numero_horas_extra):
        valor_hora_extra = self.calcular_valor_hora() * 1.5
        total_horas_extra = numero_horas_extra * valor_hora_extra
        return total_horas_extra

    def calcular_desconto_faltas(self, qtd_faltas):
        valor_diaria = self.salario_base/30
        desconto_faltas = valor_diaria * qtd_faltas
        return desconto_faltas

    def calcular_inss(self, salario_bruto):
        teto_inss = 8157.41  # baseado na tabela inss de 2025
        
        if salario_bruto > teto_inss: # se ganha acima do teto paga valor fixo
            return 951.62  # < valor fixo
            
        if salario_bruto <= 1518.00:
            return salario_bruto * 0.075 # faixa 1: 7,5% de aliquota
        elif salario_bruto <= 2793.88:
            return (salario_bruto * 0.09) - 22.77 # faixa 2: 9% de aliquota
        elif salario_bruto <= 4190.83:
            return (salario_bruto * 0.12) - 106.60 # faixa 3: 12% de aliquota
        else: # faixa 4: 14% de aliquota ate o teto
            return (salario_bruto * 0.14) - 190.42 

    def calcular_irrf(self, base_irrf):
            # com base na tabela irrf maio/2025
            # a base_irrf já eh o (salario bruto - INSS)
            
            if base_irrf <= 2428.80:
                return 0.0 # isento
            elif base_irrf <= 2826.65:
                return (base_irrf * 0.075) - 182.16 # 7,5%
            elif base_irrf <= 3751.05:
                return (base_irrf * 0.15) - 394.16 # 15%
            elif base_irrf <= 4664.68:
                return (base_irrf * 0.225) - 675.49 # 22,5%
            else: # Acima de 4.664,68
                return (base_irrf * 0.275) - 908.73 # 27,5%


    def processar_folha(self, numero_horas_extra=0, qtd_faltas=0):
        valor_extras = self.calcular_horas_extras(numero_horas_extra)
        valor_faltas = self.calcular_desconto_faltas(qtd_faltas)

        salario_bruto = self.salario_base + valor_extras - valor_faltas

        valor_inss = self.calcular_inss(salario_bruto)

        base_irrf = salario_bruto - valor_inss
        valor_irrf = self.calcular_irrf(base_irrf)

        salario_liquido = salario_bruto - valor_inss - valor_irrf
        return {
            "salario_bruto": salario_bruto,
            "salario_liquido": salario_liquido,
            "desconto_inss": valor_inss,
            "desconto_irrf": valor_irrf
        }

if __name__ == "__main__":
    # teste rápido manual
    calc = CalculadoraFolhaPagamento(2500)
    resultado = calc.processar_folha()
    print(f"""
        salario bruto: {resultado['salario_bruto']}
        salario liquido: {resultado['salario_liquido']}
        desconto inss: {resultado['desconto_inss']}
        desconto irrf: {resultado['desconto_irrf']}
          """)
    pass
