"""
Sistema de Pedidos de Cafeteria
Demonstração de 4 Padrões de Projeto: Decorator, Factory Method, Strategy e Observer
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ============================================================
# CONSTANTES
# ============================================================

class Precos:
    """Constantes de preços para facilitar manutenção"""
    ESPRESSO = 5.00
    CAPPUCCINO = 8.00
    LATTE = 7.50
    LEITE = 1.50
    CHOCOLATE = 2.00
    CHANTILLY = 2.50

# ============================================================
# PADRÃO 1: DECORATOR - Ingredientes extras nas bebidas
# ============================================================

class Bebida(ABC):
    """Component - Interface base para todas as bebidas"""
    @abstractmethod
    def descricao(self) -> str:
        pass

    @abstractmethod
    def preco(self) -> float:
        pass

class Espresso(Bebida):
    """ConcreteComponent - Bebida base"""
    def descricao(self) -> str:
        return "Espresso"

    def preco(self) -> float:
        return Precos.ESPRESSO

class Cappuccino(Bebida):
    def descricao(self) -> str:
        return "Cappuccino"

    def preco(self) -> float:
        return Precos.CAPPUCCINO

class Latte(Bebida):
    def descricao(self) -> str:
        return "Latte"

    def preco(self) -> float:
        return Precos.LATTE

class IngredienteDecorator(Bebida):
    """Decorator - Classe base para ingredientes extras"""
    def __init__(self, bebida: Bebida) -> None:
        if not isinstance(bebida, Bebida):
            raise TypeError("O parâmetro deve ser uma instância de Bebida")
        self._bebida = bebida

class Leite(IngredienteDecorator):
    """ConcreteDecorator"""
    def descricao(self) -> str:
        return f"{self._bebida.descricao()} + Leite"

    def preco(self) -> float:
        return self._bebida.preco() + Precos.LEITE

class Chocolate(IngredienteDecorator):
    def descricao(self) -> str:
        return f"{self._bebida.descricao()} + Chocolate"

    def preco(self) -> float:
        return self._bebida.preco() + Precos.CHOCOLATE

class Chantilly(IngredienteDecorator):
    def descricao(self) -> str:
        return f"{self._bebida.descricao()} + Chantilly"

    def preco(self) -> float:
        return self._bebida.preco() + Precos.CHANTILLY

# ============================================================
# PADRÃO 2: FACTORY METHOD - Criação de bebidas
# ============================================================

class BebidaFactory(ABC):
    """Creator - Fábrica abstrata de bebidas"""
    @abstractmethod
    def criar_bebida(self) -> Bebida:
        pass

    def preparar_pedido(self) -> Bebida:
        bebida = self.criar_bebida()
        self._log_preparacao(bebida)
        return bebida

    def _log_preparacao(self, bebida: Bebida) -> None:
        """Método auxiliar para logging - pode ser sobrescrito"""
        print(f"Preparando: {bebida.descricao()}")

class EspressoFactory(BebidaFactory):
    """ConcreteCreator"""
    def criar_bebida(self) -> Bebida:
        return Espresso()

class CappuccinoFactory(BebidaFactory):
    def criar_bebida(self) -> Bebida:
        return Cappuccino()

class LatteFactory(BebidaFactory):
    def criar_bebida(self) -> Bebida:
        return Latte()

class FabricaBebidas:
    """Simple Factory - Centraliza criação por tipo"""
    _fabricas = {
        "espresso": EspressoFactory(),
        "cappuccino": CappuccinoFactory(),
        "latte": LatteFactory()
    }

    @classmethod
    def criar(cls, tipo: str) -> Bebida:
        if not tipo or not tipo.strip():
            raise ValueError("Tipo de bebida não pode ser vazio")

        tipo_normalizado = tipo.lower().strip()
        fabrica = cls._fabricas.get(tipo_normalizado)

        if not fabrica:
            tipos_validos = ", ".join(cls._fabricas.keys())
            raise ValueError(
                f"Tipo de bebida desconhecido: '{tipo}'. "
                f"Tipos válidos: {tipos_validos}"
            )
        return fabrica.preparar_pedido()

    @classmethod
    def tipos_disponiveis(cls) -> List[str]:
        """Retorna lista de tipos de bebidas disponíveis"""
        return list(cls._fabricas.keys())

# ============================================================
# PADRÃO 3: STRATEGY - Formas de pagamento
# ============================================================

class PagamentoStrategy(ABC):
    """Strategy - Interface para estratégias de pagamento"""
    @abstractmethod
    def pagar(self, valor: float) -> bool:
        pass

    @abstractmethod
    def nome(self) -> str:
        pass

    @abstractmethod
    def _log_pagamento(self, mensagem: str) -> None:
        """Método auxiliar para logging"""
        pass

class PagamentoCartao(PagamentoStrategy):
    """ConcreteStrategy"""
    def __init__(self, numero_cartao: str) -> None:
        if not numero_cartao or len(numero_cartao) < 4:
            raise ValueError("Número do cartão inválido")
        self._numero = numero_cartao

    def pagar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("Valor de pagamento deve ser positivo")

        self._log_pagamento(
            f"Processando pagamento de R${valor:.2f} no cartão **{self._numero[-4:]}"
        )
        return True

    def nome(self) -> str:
        return "Cartão de Crédito"

    def _log_pagamento(self, mensagem: str) -> None:
        print(mensagem)

class PagamentoPix(PagamentoStrategy):
    def __init__(self, chave_pix: str) -> None:
        if not chave_pix or not chave_pix.strip():
            raise ValueError("Chave PIX não pode ser vazia")
        self._chave = chave_pix.strip()

    def pagar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("Valor de pagamento deve ser positivo")

        self._log_pagamento(f"PIX de R${valor:.2f} enviado para {self._chave}")
        self._log_pagamento("QR Code gerado! Aguardando confirmação...")
        return True

    def nome(self) -> str:
        return "PIX"

    def _log_pagamento(self, mensagem: str) -> None:
        print(mensagem)

class PagamentoDinheiro(PagamentoStrategy):
    def __init__(self, valor_entregue: float) -> None:
        if valor_entregue <= 0:
            raise ValueError("Valor entregue deve ser positivo")
        self._valor_entregue = valor_entregue

    def pagar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("Valor de pagamento deve ser positivo")

        if self._valor_entregue >= valor:
            troco = self._valor_entregue - valor
            self._log_pagamento(f"Pagamento em dinheiro: R${self._valor_entregue:.2f}")
            if troco > 0:
                self._log_pagamento(f"Troco: R${troco:.2f}")
            return True

        self._log_pagamento(
            f"Valor insuficiente! Faltam R${valor - self._valor_entregue:.2f}"
        )
        return False

    def nome(self) -> str:
        return "Dinheiro"

    def _log_pagamento(self, mensagem: str) -> None:
        print(mensagem)

# ============================================================
# PADRÃO 4: OBSERVER - Notificações de status do pedido
# ============================================================

class StatusPedido(Enum):
    RECEBIDO = "Recebido"
    PREPARANDO = "Preparando"
    PRONTO = "Pronto"
    ENTREGUE = "Entregue"

class ObservadorPedido(ABC):
    """Observer - Interface para observadores"""
    @abstractmethod
    def atualizar(self, pedido: 'Pedido') -> None:
        pass

    def __eq__(self, other: object) -> bool:
        """Permite comparação para evitar duplicatas"""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Permite uso em sets para evitar duplicatas"""
        return hash(tuple(sorted(self.__dict__.items())))

class NotificadorCliente(ObservadorPedido):
    """ConcreteObserver - Notifica o cliente"""
    def __init__(self, nome_cliente: str) -> None:
        if not nome_cliente or not nome_cliente.strip():
            raise ValueError("Nome do cliente não pode ser vazio")
        self._nome = nome_cliente.strip()

    def atualizar(self, pedido: 'Pedido') -> None:
        if pedido.status == StatusPedido.PRONTO:
            self._enviar_notificacao(
                f"📱 SMS para {self._nome}: Seu pedido #{pedido.id} está PRONTO!"
            )
        elif pedido.status == StatusPedido.PREPARANDO:
            self._enviar_notificacao(
                f"📱 SMS para {self._nome}: Seu pedido #{pedido.id} está sendo preparado"
            )

    def _enviar_notificacao(self, mensagem: str) -> None:
        """Método auxiliar para envio de notificações"""
        print(mensagem)

class PainelPedidos(ObservadorPedido):
    """ConcreteObserver - Atualiza painel da loja"""
    def atualizar(self, pedido: 'Pedido') -> None:
        self._atualizar_painel(
            f"📺 Painel atualizado: Pedido #{pedido.id} -> {pedido.status.value}"
        )

    def _atualizar_painel(self, mensagem: str) -> None:
        """Método auxiliar para atualização do painel"""
        print(mensagem)

class SistemaMetricas(ObservadorPedido):
    """ConcreteObserver - Registra métricas"""
    def atualizar(self, pedido: 'Pedido') -> None:
        if pedido.status == StatusPedido.ENTREGUE:
            timestamp = datetime.now().strftime('%H:%M:%S')
            self._registrar_metrica(
                f"📊 Métrica registrada: Pedido #{pedido.id} concluído às {timestamp}"
            )

    def _registrar_metrica(self, mensagem: str) -> None:
        """Método auxiliar para registro de métricas"""
        print(mensagem)

# ============================================================
# CLASSE PEDIDO - Subject do Observer + Context do Strategy
# ============================================================

class Pedido:
    """Subject (Observable) - Gerencia pedido e notifica observers"""
    _contador = 0

    def __init__(self, cliente: str) -> None:
        if not cliente or not cliente.strip():
            raise ValueError("Nome do cliente não pode ser vazio")

        Pedido._contador += 1
        self.id = Pedido._contador
        self.cliente = cliente.strip()
        self.itens: List[Bebida] = []
        self._status = StatusPedido.RECEBIDO
        self._observers: List[ObservadorPedido] = []
        self._pagamento: Optional[PagamentoStrategy] = None

    @property
    def status(self) -> StatusPedido:
        return self._status

    @status.setter
    def status(self, novo_status: StatusPedido) -> None:
        if not isinstance(novo_status, StatusPedido):
            raise TypeError("Status deve ser uma instância de StatusPedido")
        self._status = novo_status
        self._notificar()

    def adicionar_observer(self, observer: ObservadorPedido) -> None:
        if not isinstance(observer, ObservadorPedido):
            raise TypeError("Observer deve implementar ObservadorPedido")

        # Evita duplicatas
        if observer not in self._observers:
            self._observers.append(observer)

    def remover_observer(self, observer: ObservadorPedido) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notificar(self) -> None:
        for observer in self._observers:
            observer.atualizar(self)

    def adicionar_item(self, bebida: Bebida) -> None:
        if not isinstance(bebida, Bebida):
            raise TypeError("Item deve ser uma instância de Bebida")
        self.itens.append(bebida)

    def total(self) -> float:
        return sum(item.preco() for item in self.itens)

    def definir_pagamento(self, estrategia: PagamentoStrategy) -> None:
        if not isinstance(estrategia, PagamentoStrategy):
            raise TypeError("Estratégia deve implementar PagamentoStrategy")
        self._pagamento = estrategia

    def processar_pagamento(self) -> bool:
        if not self._pagamento:
            raise RuntimeError("Nenhuma forma de pagamento definida!")

        if not self.itens:
            raise RuntimeError("Pedido vazio! Adicione itens antes de pagar.")

        return self._pagamento.pagar(self.total())

    def resumo(self) -> str:
        linhas = [
            f"\n{'='*50}",
            f"PEDIDO #{self.id} - Cliente: {self.cliente}",
            f"Status: {self.status.value}",
            "-"*50
        ]

        if not self.itens:
            linhas.append("  (Nenhum item adicionado)")
        else:
            for i, item in enumerate(self.itens, 1):
                linhas.append(f"  {i}. {item.descricao()} - R${item.preco():.2f}")

        linhas.extend([
            "-"*50,
            f"TOTAL: R${self.total():.2f}",
            "="*50
        ])
        return "\n".join(linhas)

# ============================================================
# DEMONSTRAÇÃO DO SISTEMA
# ============================================================

def main() -> None:
    print("\n" + "🔷"*25)
    print("   CAFETERIA DESIGN PATTERNS - SISTEMA DE PEDIDOS")
    print("🔷"*25 + "\n")

    try:
        # Criar pedido
        pedido = Pedido("Maria Silva")

        # Registrar observers (OBSERVER PATTERN)
        pedido.adicionar_observer(NotificadorCliente("Maria Silva"))
        pedido.adicionar_observer(PainelPedidos())
        pedido.adicionar_observer(SistemaMetricas())

        print("📝 CRIANDO PEDIDO...")
        print("-" * 40)

        # Criar bebidas usando Factory (FACTORY PATTERN)
        bebida1 = FabricaBebidas.criar("espresso")

        # Adicionar ingredientes extras (DECORATOR PATTERN)
        bebida2 = FabricaBebidas.criar("latte")
        bebida2 = Leite(bebida2)
        bebida2 = Chocolate(bebida2)

        bebida3 = FabricaBebidas.criar("cappuccino")
        bebida3 = Chantilly(bebida3)

        # Adicionar ao pedido
        pedido.adicionar_item(bebida1)
        pedido.adicionar_item(bebida2)
        pedido.adicionar_item(bebida3)

        # Mostrar resumo
        print(pedido.resumo())

        # Definir pagamento (STRATEGY PATTERN)
        print("\n💳 PROCESSANDO PAGAMENTO...")
        print("-" * 40)
        pagamento = PagamentoPix("cafeteria@pix.com")
        pedido.definir_pagamento(pagamento)

        if pedido.processar_pagamento():
            print("✅ Pagamento confirmado!\n")

            # Atualizar status (dispara OBSERVER PATTERN)
            print("📢 ATUALIZAÇÕES DE STATUS:")
            print("-" * 40)
            pedido.status = StatusPedido.PREPARANDO
            print()
            pedido.status = StatusPedido.PRONTO
            print()
            pedido.status = StatusPedido.ENTREGUE

        print("\n" + "🔷"*25)
        print("   FIM DA DEMONSTRAÇÃO")
        print("🔷"*25 + "\n")

    except (ValueError, TypeError, RuntimeError) as e:
        print(f"\n❌ ERRO: {e}\n")
        raise

if __name__ == "__main__":
    main()
