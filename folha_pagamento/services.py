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
        total_inss = salario_bruto * 0.10 ## a principio utilizando só 10% como calculo do INSS
        return total_inss

    def calcular_irrf(self, base_irrf): ## base irrf: salario que sobra depois do desconto do INSS
        total_irrf = base_irrf * 0.05
        return total_irrf


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
    calc = CalculadoraFolhaPagamento(2500)
    resultado = calc.processar_folha()
    print(f"""
        salario bruto: {resultado['salario_bruto']}
        salario liquido: {resultado['salario_liquido']}
        desconto inss: {resultado['desconto_inss']}
        desconto irrf: {resultado['desconto_irrf']}
          """)
    pass