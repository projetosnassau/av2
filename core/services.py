from decimal import Decimal

class CalculadoraFolha:
    def __init__(self, salario_base):
        self.salario_base = Decimal(str(salario_base))

    def calcular(self, horas_extras=0, faltas=0, bonus=0, deducoes_manuais=0):
        qtd_he = Decimal(str(horas_extras))
        qtd_faltas = Decimal(str(faltas))
        val_bonus = Decimal(str(bonus))
        val_deducoes_manuais = Decimal(str(deducoes_manuais))

        valor_hora = self.salario_base / Decimal(220)
        valor_he = (valor_hora * Decimal(1.5)) * qtd_he
        
        valor_dia = self.salario_base / Decimal(30)
        valor_faltas_total = valor_dia * qtd_faltas
        
        bruto = self.salario_base + valor_he + val_bonus - valor_faltas_total
        if bruto < 0: bruto = Decimal(0)

        inss = self._calcular_inss(bruto)
        
        base_irrf = bruto - inss
        if base_irrf < 0: base_irrf = Decimal(0)
        irrf = self._calcular_irrf(base_irrf)
        
        liquido = bruto - inss - irrf - val_deducoes_manuais
        
        return {
            "salario_bruto": round(bruto, 2),
            "salario_liquido": round(liquido, 2),
            "inss": round(inss, 2),
            "irrf": round(irrf, 2),
            "valor_horas_extras": round(valor_he, 2),
            "valor_faltas": round(valor_faltas_total, 2)
        }

    def _calcular_inss(self, bruto):
        teto = Decimal('8157.41')
        if bruto > teto: return Decimal('951.62')
        
        if bruto <= 1518.00: return bruto * Decimal('0.075')
        if bruto <= 2793.88: return (bruto * Decimal('0.09')) - Decimal('22.77')
        if bruto <= 4190.83: return (bruto * Decimal('0.12')) - Decimal('106.60')
        return (bruto * Decimal('0.14')) - Decimal('190.42')

    def _calcular_irrf(self, base):
        if base <= 2428.80: return Decimal(0)
        if base <= 2826.65: return (base * Decimal('0.075')) - Decimal('182.16')
        if base <= 3751.05: return (base * Decimal('0.15')) - Decimal('394.16')
        if base <= 4664.68: return (base * Decimal('0.225')) - Decimal('675.49')
        return (base * Decimal('0.275')) - Decimal('908.73')