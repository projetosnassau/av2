import statistics

class CalculadoraFolhaPagamento:
    """
    Calculo individual de contracheque com as regras de 2025 aplicadas,
    Conversão para float nos retornos
    """
    def __init__(self, salario_base): 
        self.salario_base = float(salario_base)

    def calcular_valor_hora(self):
        return self.salario_base / 220

    def calcular_horas_extras(self, numero_horas_extra):
        valor_hora_extra = self.calcular_valor_hora() * 1.5
        return float(numero_horas_extra) * valor_hora_extra

    def calcular_desconto_faltas(self, qtd_faltas):
        valor_diaria = self.salario_base / 30
        return valor_diaria * float(qtd_faltas)

    def calcular_inss(self, salario_bruto):
        # Tabela INSS 2025 - Progressiva
        teto_inss = 8157.41
        
        if salario_bruto > teto_inss: 
            return 951.62
            
        if salario_bruto <= 1518.00: 
            return salario_bruto * 0.075
        elif salario_bruto <= 2793.88: 
            return (salario_bruto * 0.09) - 22.77
        elif salario_bruto <= 4190.83: 
            return (salario_bruto * 0.12) - 106.60
        else: 
            return (salario_bruto * 0.14) - 190.42

    def calcular_irrf(self, base_irrf):
        # Tabela IRRF Maio/2025 (Declaração 2026)
        
        if base_irrf <= 2428.80: 
            return 0.0
        elif base_irrf <= 2826.65: 
            return (base_irrf * 0.075) - 182.16
        elif base_irrf <= 3751.05: 
            return (base_irrf * 0.15) - 394.16
        elif base_irrf <= 4664.68: 
            return (base_irrf * 0.225) - 675.49
        else: 
            return (base_irrf * 0.275) - 908.73

    def processar_folha(self, numero_horas_extra=0, qtd_faltas=0):
        valor_extras = self.calcular_horas_extras(numero_horas_extra)
        valor_faltas = self.calcular_desconto_faltas(qtd_faltas)
        
        salario_bruto = self.salario_base + valor_extras - valor_faltas
        
        # Evita cálculo de imposto negativo se as faltas zerarem o salário
        if salario_bruto < 0:
            salario_bruto = 0.0

        valor_inss = self.calcular_inss(salario_bruto)
        base_irrf = salario_bruto - valor_inss
        
        if base_irrf < 0:
            base_irrf = 0.0
            
        valor_irrf = self.calcular_irrf(base_irrf)
        
        salario_liquido = salario_bruto - valor_inss - valor_irrf
        
        return {
            "salario_bruto": round(salario_bruto, 2),
            "salario_liquido": round(salario_liquido, 2),
            "desconto_inss": round(valor_inss, 2),
            "desconto_irrf": round(valor_irrf, 2)
        }

class AnaliseSalarialService:
    """
    Recebe uma lista de funcionarios, calcula todos
    e gera estatísticas (ranking, medias, totais)
    """
    def analisar_lista(self, lista_funcionarios):
        resultados = []
        
        for func in lista_funcionarios:
            # converte tudo para float quando le da lista do serializer
            salario = float(func['salario_base'])
            extras = float(func.get('horas_extras', 0))
            faltas = float(func.get('faltas', 0))
            nome = func.get('nome', 'Não informado')

            calc = CalculadoraFolhaPagamento(salario)
            holerite = calc.processar_folha(extras, faltas)
            
            holerite['nome'] = nome
            resultados.append(holerite)

        # Ordena o ranking (Quem ganha mais primeiro)
        ranking = sorted(resultados, key=lambda x: x['salario_liquido'], reverse=True)

        if ranking:
            lista_liquidos = [r['salario_liquido'] for r in ranking]
            
            estatisticas = {
                "total_funcionarios": len(ranking),
                "maior_salario_liquido": max(lista_liquidos),
                "menor_salario_liquido": min(lista_liquidos),
                "media_salarial": round(statistics.mean(lista_liquidos), 2),
                "folha_total_custo": round(sum(lista_liquidos), 2)
            }
        else:
            estatisticas = {
                "total_funcionarios": 0,
                "msg": "Nenhum dado processado"
            }

        return {
            "relatorio_gerencial": estatisticas,
            "ranking_detalhado": ranking
        }